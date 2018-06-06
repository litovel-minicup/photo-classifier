import QtQuick 2.0

Item {
    id: component

    property var imagesData: []
    property alias imageIndex: internal.index
    readonly property alias selectedMarkerId: internal.selectedMarkerId

    onImagesDataChanged: {
        canvas.requestPaint()
        repeater.modelChanged()
    }

    QtObject {
        id: internal

        property int index: -1
        property string selectedMarkerId: ""

        onIndexChanged: {
            canvas.requestPaint()
            selectedMarkerId = ""
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked:internal.selectedMarkerId = ""
    }

    Rectangle {
        id: container

        color: "lightGray"
        anchors.fill: parent
        anchors.bottomMargin: 35
    }

    Image {
        id: image

        fillMode: Image.PreserveAspectFit
        source: (component.imagesData.length && internal.index != -1)
                ?component.imagesData[internal.index].fileUrl :""
        anchors.fill: container
        anchors.bottomMargin: 10

        onHeightChanged: canvas.requestPaint()
        onWidthChanged: canvas.requestPaint()
    }

    Item {
        id: imageOverlay

        readonly property real scale: Math.min(image.width / image.sourceSize.width,
                                              image.height / image.sourceSize.height)

        width: scale * image.sourceSize.width
        height: scale * image.sourceSize.height

        anchors.horizontalCenter: image.horizontalCenter
    }

    Repeater {
        id: repeater

        model: (internal.index != -1) ?Object.keys((imagesData[internal.index].markers)) :[]

        Marker {
            readonly property var markerData: imagesData[internal.index].markers[modelData]

            x: markerData.x * imageOverlay.scale - width / 2 + imageOverlay.x
            y: markerData.y * imageOverlay.scale - height / 2 + imageOverlay.y

            width: 25
            height: width
            radius: width
            selected: internal.selectedMarkerId === markerData.id

            tag: markerData.tag

            onMarkerSelected: internal.selectedMarkerId = markerData.id

        }
    }

    Canvas {
        id: canvas

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: container.bottom
        anchors.bottom: parent.bottom

        onPaint: {
            var ctx = canvas.getContext("2d")

            // DESIGN SHITS
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            ctx.fillStyle = "#262626"
            ctx.fillRect(0, 0, canvas.width, canvas.height)

            ctx.beginPath()
            ctx.fillStyle = "lightGray"
            ctx.moveTo(0, 0)
            ctx.lineTo(canvas.width * 0.5, 0)
            ctx.lineTo(canvas.width * 0.5 - canvas.height, canvas.height)
            ctx.lineTo(0, canvas.height)
            ctx.lineTo(0, 0)
            ctx.fill()
        }

        Text {
            text: "Processed image"
            color: "black"

            font.family: "Montserrat"
            font.pixelSize: 25

            anchors.verticalCenter: parent.verticalCenter
            anchors.leftMargin: 30
            anchors.left: parent.left
        }

        Text {
            text: "Shared tags"
            color: "white"

            font.family: "Montserrat"
            font.pixelSize: 25

            anchors.verticalCenter: parent.verticalCenter
            anchors.rightMargin: 30
            anchors.right: parent.right
        }
    }

    function nextUntaggedImage() {
        if(internal.index >= imagesData.length - 1)
            return

        for(var i = internal.index + 1; i < imagesData.length; i++) {
            var imageData = imagesData[i]
            for(var key in imageData.markers) {
                if(imageData.markers[key].tag == "") {
                    internal.index = i;
                    return
                }
            }
        }

        internal.index = imagesData.length - 1
    }

    function nextImage() {
        if(internal.index < imagesData.length - 1)
        internal.index++;
    }

    function prevImage() {
        if(internal.index > 0)
        internal.index--;
    }
}
