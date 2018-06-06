# coding=utf-8
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty, QVariant
from PyQt5.QtQml import QJSValue


class Wrapper(QObject):
    imageDataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._image_data = {
            "FOO": 33,
            "BAR": 33,
        }

    @pyqtSlot(str)
    def confirmImage(self, url):
        pass

    @pyqtSlot(str)
    def deleteImage(self, url):
        pass

    @pyqtSlot(QVariant)
    def classifyImages(self, paths: QJSValue):
        paths = paths.toVariant()
        # TODO
        print(paths)
        pass

    @pyqtProperty(QVariant, notify=imageDataChanged)
    def imagesData(self):
        return self._image_data

    @imagesData.setter
    def imagesData(self, v):
        if not isinstance(v, dict):
            v = v.toVariant()
        if v == self._image_data:
            return
        self._image_data = v
        self.imageDataChanged.emit()
