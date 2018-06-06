import QtQuick 2.5
import QtQuick.Dialogs 1.2
import QtQuick.Controls 1.4
import QtQuick.Window 2.2
import "controls" as Controls

Window {
    width: 1280
    height: 720

    visible: true
    title: qsTr("Photo classifier")

    FontLoader {
        source: "qrc:/qml/fonts/montserrat-light.ttf"
    }

    FontLoader {
        source: "qrc:/qml/fonts/montserrat-regular.ttf"
    }

    QtObject {
        id: wrapper

        // TODO bind
        property var imagesData: []
    }

    FileDialog {
        id: fileDialog

        selectMultiple: true
        onAccepted: {
            console.log("You chose: " + fileDialog.fileUrls)
//            imageBrowser.images = fileDialog.fileUrls
            imageBrowser.imageIndex = -1

        }

//        Component.onCompleted: visible = true
        Component.onCompleted: {
            // TODO change
            var urls = ["file:///C:/Users/Sony/Documents/photo-classifier/photos/test.png", "file:///C:/Users/Sony/Documents/photo-classifier/photos/test1.png",
                    "file:///C:/Users/Sony/Documents/photo-classifier/photos/test2.png"
                    ]
            classifyImages(urls)
        }

        function classifyImages(urls) {
            // TODO use classifier
            for(var key in urls) {
                var imageData = {
                    "origWidth": 1129,
                    "origHeight": 750,
                    "fileUrl": urls[key],
                    "tagsSelection": ["", "sony1", "sony2", "sony3",
                        "sony4 dfsdfdsfsf sdfsfsdffdgfdg", "sony5", "sony6", "sony7", "sony8",
                        "sony9", "sony91", "sony10", "sony11", "sony12"],
                    "sharedTagsSelection": ["Pátek", "Sobotaa", "Neděle"],
                    "markers": {
                        0: {
                            "id": 0,
                            "x": 100,
                            "y": 100,
                            "tag": "sony1"
                        },

                        1: {
                            "id": 1,
                            "x": 400,
                            "y": 150,
                            "tag": "sony1"
                        }
                    }
                }

                if(key == 2) {
                imageData.markers["2"] = {
                    "id": 2,
                    "x": 200,
                    "y": 150,
                    "tag": null
                }
                }

                if(key == 0)
                    imageData["sharedTags"] = ["Pátek"]
                else
                    imageData["sharedTags"] = []

                wrapper.imagesData.push(imageData)
                wrapper.imagesDataChanged()
            }
        }
    }

    Item {
        id: positioner
        anchors.fill: parent
    }

    ImageBrowser {
        id: imageBrowser

        imagesData: wrapper.imagesData

        width: parent.width * 0.8
        height: parent.height * 0.8

        onImageIndexChanged: {
            if(imageIndex == -1)
                return

            if(wrapper.imagesData[imageIndex].sharedTags.length)
                horizontalSelection.selectedTags = wrapper.imagesData[imageIndex].sharedTags
            else {
                if(imageBrowser.imageIndex === -1)
                    return

                wrapper.imagesData[imageBrowser.imageIndex].sharedTags =
                        horizontalSelection.selectedTags
                wrapper.imagesDataChanged()
            }

            horizontalSelection.selectedTagsChanged()
        }

        onSelectedMarkerIdChanged: {
            if(selectedMarkerId == "")
                return

            verticalSelection.selectedTags = []
            verticalSelection.selectedTags.push(wrapper.imagesData[imageIndex]
                                                .markers[selectedMarkerId].tag)
            verticalSelection.selectedTagsChanged()
        }
    }

    VerticalTagSelection {
        id: verticalSelection

        color: "#262626"
        tags: (imageBrowser.selectedMarkerId !== "" && imageBrowser.imageIndex !== -1)
              ?wrapper.imagesData[imageBrowser.imageIndex].tagsSelection :[]

        anchors.top: positioner.top
        anchors.bottom: positioner.bottom
        anchors.left: imageBrowser.right
        anchors.right: positioner.right

        onSelectedTagsChanged: {
            if(imageBrowser.selectedMarkerId == "" || selectedTags.length == 0)
                return

            wrapper.imagesData[imageBrowser.imageIndex]
            .markers[imageBrowser.selectedMarkerId].tag  = selectedTags[0]
            wrapper.imagesDataChanged()
        }
    }

    HorizontalTagSelection {
        id: horizontalSelection

        color: "#262626"
        // TODO on image change change shred selected tags
        tags: (imageBrowser.imageIndex !== -1)
              ?wrapper.imagesData[imageBrowser.imageIndex].sharedTagsSelection :[]

        height: parent.height * 0.1

        anchors.top: imageBrowser.bottom
        anchors.left: positioner.left
        anchors.right: verticalSelection.left

        onSelectedTagsChanged: {
            if(selectedTags.length == 0)
                return

            for(var key in wrapper.imagesData) {
                wrapper.imagesData[key].sharedTags = selectedTags
            }
            wrapper.imagesDataChanged()
        }
    }

    Row {
        id: controls

        height: 40

        anchors.left: positioner.left
        anchors.right: verticalSelection.left
        anchors.bottom: positioner.bottom

        Controls.TextButton {
            buttonText: "Previous"
            textColor: "white"
            color: "gray"
            hoverColor: "white"

            width: parent.width / 3
            height: parent.height

            onClicked: imageBrowser.prevImage()
        }

        Controls.TextButton {
            buttonText: "Next"
            textColor: "white"
            color: "gray"
            hoverColor: "white"

            width: parent.width / 3
            height: parent.height

            onClicked: imageBrowser.nextImage()
        }

        Controls.TextButton {
            buttonText: "Next untagged"
            textColor: "white"
            color: "gray"
            hoverColor: "white"

            width: parent.width / 3
            height: parent.height

            onClicked: imageBrowser.nextUntaggedImage()
        }
    }

    Rectangle {
        color: "lightGray"

        anchors.left: controls.left
        anchors.right: controls.right
        anchors.bottom: controls.top
        anchors.top: horizontalSelection.bottom

        Rectangle {
            height: parent.height
            width:  ((imageBrowser.imageIndex + 1) / wrapper.imagesData.length) * parent.width
            color: "#1C70B7"
        }

        Text {
            text: (imageBrowser.imageIndex + 1) + "/" + wrapper.imagesData.length

            anchors.centerIn: parent
            font.family: "Montserrat"
            font.pixelSize: parent.height * 0.65
        }
    }
}
