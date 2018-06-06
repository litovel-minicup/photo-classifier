import QtQuick 2.0

Rectangle {
    id: component

    signal tagSelectReq(string tag)
    signal tagDisselectReq(string tag)

    property bool selected: false
    property string tag
    property color hoverColor
    property color selectedColor
    property color textColor
    property color selectedTextColor
    property SelectableTagStyle style

    Rectangle {     // select background overlay
        color: component.selectedColor
        opacity: (component.selected) ?1 :0
        anchors.fill: parent

        Behavior on opacity {
            NumberAnimation { duration: 250 }
        }
    }

    Rectangle {     // hover overlay
        color: component.hoverColor
        opacity: (mouseArea.containsMouse) ?0.4 :0
        anchors.fill: parent
    }

    MouseArea {
        id: mouseArea

        hoverEnabled: true
        anchors.fill: parent

        onClicked: {
            if(!component.selected)
               component.tagSelectReq(component.tag)
            else
                component.tagDisselectReq(component.tag)
        }
    }

    Text {
        id: text

        text: component.tag
        color: (component.selected) ?component.selectedTextColor :component.textColor
        wrapMode: Text.WordWrap
        font.pixelSize: component.height * 0.3
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        anchors.margins: 5
        anchors.fill: parent
    }

    onStyleChanged: {
        if(!style)
            return

        component.selectedColor = Qt.binding(function() { return style.selectedColor })
        component.color = Qt.binding(function() { return style.color })
        component.hoverColor = Qt.binding(function() { return style.hoverColor })
        text.font.family = Qt.binding(function() { return style.font.family })
        component.textColor = Qt.binding(function() { return style.textColor })
        component.selectedTextColor = Qt.binding(function() { return style.selectedTextColor })
    }
}
