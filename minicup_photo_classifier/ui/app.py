# coding=utf-8
import sys

import sys
# noinspection PyUnresolvedReferences
import ui.resources
from minicup_photo_classifier.ui.wrapper import Wrapper
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import (QSize, QtFatalMsg, QtCriticalMsg, QtWarningMsg, QtInfoMsg,
                          qInstallMessageHandler, QtDebugMsg, QUrl)

try:
    from termcolor import colored
except ImportError:
    def colored(mode, *args, **kwargs):
        return mode

def qt_message_handler(mode, context, message):
    modes = {
        QtInfoMsg: "Info",
        QtWarningMsg: "Warning",
        QtCriticalMsg: "Critical",
        QtFatalMsg: "Fatal",
        QtDebugMsg: "Debug"
    }

    modes_colors = {
        QtInfoMsg: "blue",
        QtWarningMsg: "yellow",
        QtCriticalMsg: "red",
        QtFatalMsg: "red",
        QtDebugMsg: "green"
    }

    mode = colored(modes[mode], modes_colors[mode])

    if context.file is None:
        print('{mode}: {msg}'.format(mode=mode, msg=message))
    else:
        print('{mode}: {msg}\t\t\t\tline: {line}, function: {func}, file: {file}'.format(
            mode=mode, line=context.line, func=context.function, file=context.file, msg=message))


qInstallMessageHandler(qt_message_handler)

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    def run(self):
        engine = QQmlApplicationEngine()
        w = Wrapper()

        engine.rootContext().setContextProperty("manager", w)
        engine.load(QUrl("qrc:/qml/main.qml"))

        self.exec()


if __name__ == "__main__":
    a = App(sys.argv)
    a.run()