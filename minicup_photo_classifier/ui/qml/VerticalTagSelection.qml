import QtQuick 2.0
import "items" as Items

Rectangle {
    id: component

    property var tags: []
    property var selectedTags: []
    property color itemColor: "#383838"

    Flickable {
        contentWidth: items.width
        contentHeight: items.height
        boundsBehavior: Flickable.StopAtBounds
        clip: true

        anchors.fill: parent

        // TODO loader?
        Column {
            id: items

            Repeater {
                model: component.tags
                delegate: Items.SelectableTag {
                    width: component.width
                    height: 70
                    selected: (selectedTags.indexOf(tag) !== -1)

                    tag: modelData

                    style: Items.SelectableTagStyle {
                        color: component.itemColor
                        textColor: "lightGray"
                        hoverColor: "white"
                        selectedColor: "#1C70B7"
                        font.family: "Montserrat"
                    }

                    onTagSelectReq: {
                        clearSelection()
                        if(selectedTags.indexOf(tag) === -1)
                            selectedTags.push(tag)
                        selectedTagsChanged()
                    }

                    onTagDisselectReq: {
                        var index = selectedTags.indexOf(tag)
                        if(index !== -1)
                            selectedTags.splice(index, 1)
                        selectedTagsChanged()
                    }
                }
            }
        }
    }

    function clearSelection() {
        component.selectedTags = []
        selectedTagsChanged()
    }
}
