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

    MouseArea {
        id: mouseArea

        hoverEnabled: true
        anchors.fill: parent

        onClicked: {
            parent.markerSelected()
        }
    }
}
