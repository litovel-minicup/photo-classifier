# coding=utf-8
from os.path import join, dirname
from typing import List

import numpy as np

from .config import load_config
from .pose_detection.detections import extract_detections
from .pose_detection.mscoco import MSCOCO
from .pose_detection.nnet.predict import setup_pose_prediction, extract_cnn_output
from .pose_detection.predict import SpatialModel, eval_graph, get_person_conf_multicut


class ObjectDetector(object):
    """
    Class for detecting figure parts on image.
    """

    PERSON_CONF_HANDS_SELECTOR = slice(5, 8 + 1 - 2)

    def __init__(self):
        self._config = load_config(join(dirname(__file__), 'config/config.yaml'))
        self._dataset = MSCOCO(self._config)
        self._spatial_model = SpatialModel(self._config)

        self._spatial_model.load()

        self._session, self._model_inputs, self._model_outputs = setup_pose_prediction(self._config)

    def detect_objects(self, image: np.ndarray) -> List[np.ndarray]:
        """
        For each figure on image returns np.array of [Lshoulder, Rshoulder, Lelbow, Relbow].
        Each component has [x, y], for not found parts [0, 0] is placed.
        :param image: image to detect
        :return: all found parts
        """
        image_batch = self._image_to_data(image)

        # Compute prediction with the CNN
        outputs_np = self._session.run(self._model_outputs, feed_dict={self._model_inputs: image_batch})
        sc_map, loc_ref, pairwise_diff = extract_cnn_output(outputs_np, self._config, self._dataset.pairwise_stats)

        detections = extract_detections(self._config, sc_map, loc_ref, pairwise_diff)
        un_label, pos_array, unary_array, p_w_idx_array, pw_array = eval_graph(self._spatial_model, detections)

        return [
            person[self.PERSON_CONF_HANDS_SELECTOR].astype(int)
            for person in
            get_person_conf_multicut(self._spatial_model, un_label, unary_array, pos_array)
        ]

    @staticmethod
    def _image_to_data(image):
        """
        Expands image to data vector.
        :param image: image
        :return: reshaped
        """
        return np.expand_dims(image, axis=0).astype(float)


__all__ = ['ObjectDetector']
