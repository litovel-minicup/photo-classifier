# coding=utf-8
from os.path import join

from PIL import ImageFile
from keras import Model, Sequential
from keras.activations import relu, sigmoid
from keras.engine import InputLayer
from keras.layers import SeparableConv2D, Activation, MaxPooling2D, Flatten, Dense
from keras.losses import categorical_crossentropy
from keras.models import save_model
from keras.optimizers import Adadelta, SGD
from keras.preprocessing.image import ImageDataGenerator

ImageFile.LOAD_TRUNCATED_IMAGES = True


class NeuralNetwork(object):
    def __init__(self, snapshot_dir):
        self._snapshot_dir = snapshot_dir

    def _preprocess(self, img):
        # print(img.shape)
        return img

    def create_model(self) -> Model:
        model = Sequential()
        model.add(InputLayer(input_shape=(256, 256, 3)))
        # model.add(Lambda(self._preprocess))

        for _ in range(6):
            model.add(SeparableConv2D(64, 7, padding='same'))
            model.add(Activation(relu))
            model.add(MaxPooling2D(2))

        model.add(Flatten())
        model.add(Dense(2048))
        model.add(Activation(relu))
        model.add(Dense(2))
        model.add(Activation(sigmoid))

        model.compile(
            loss=categorical_crossentropy,
            optimizer=SGD(lr=1),
            metrics=['accuracy']
        )
        model.summary()

        return model

    def train(self, train_dir):
        model = self.create_model()

        image_gen = ImageDataGenerator(
            preprocessing_function=self._preprocess,
            rescale=1 / 255.,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            rotation_range=90,
            fill_mode='nearest',
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=(.2, 1.8)
        )

        trainer = image_gen.flow_from_directory(
            train_dir,
            batch_size=8,
            # save_to_dir='aug_out/'
        )

        for _ in range(64):
            model.fit_generator(
                generator=trainer,
                verbose=1,
                use_multiprocessing=True,
                workers=4,
            )
            model.optimizer.lr /= 1.5
            save_model(model, join(self._snapshot_dir, 'model-{:02}.h5'.format(_)))
