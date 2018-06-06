import QtQuick 2.0

Item {
    signal markerSelected

    property real radius: 0
    property bool selected: false
    property string tag: ""

    Rectangle {
        id: background

        color: (mouseArea.containsMouse || selected) ?"black" :"white"
        opacity: 0.5

        radius: parent.radius
        anchors.fill: parent
    }

    Rectangle {
        color: "transparent"
        border.width: 3
        border.color: (parent.tag) ?"#1C70B7" :"#d90202"

        radius: parent.radius
        anchors.fill: parent
    }

    Rectangle {
        id: markerDescription

        width: markerText.width + 2 * 8
        height: markerText.height + 2 * 4
        opacity: 0.6
        color: "white"

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.bottom
    }

    Text {
        id: markerText

        color: "black"
        text: parent.tag

        font.pixelSize: 18
        font.family: "Montserrat"

        anchors.centerIn: markerDescription
    }

    MouseArea {
        id: mouseArea

        hoverEnabled: true
        anchors.fill: parent

        onClicked: {
            parent.markerSelected()
        }
    }
}
