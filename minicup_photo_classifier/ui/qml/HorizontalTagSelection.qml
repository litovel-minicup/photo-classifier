import QtQuick 2.0
import "items" as Items

Rectangle {
    id: component

    property var tags: []
    property var selectedTags: []

    Flickable {
        contentWidth: items.width
        contentHeight: items.height
        boundsBehavior: Flickable.StopAtBounds
        clip: true

        anchors.fill: parent

        // TODO loader?
        Row {
            id: items

            Repeater {
                model: component.tags
                delegate: Items.SelectableTag {
                    width: 180
                    height: component.height
                    selected: (selectedTags.indexOf(tag) !== -1)

                    tag: modelData

                    style: Items.SelectableTagStyle {
                        color: "#262626"
                        textColor: "lightGray"
                        hoverColor: "white"
                        selectedColor: "#F8CF00"
                        selectedTextColor: "#262626"
                        font.family: "Montserrat"
                    }

                    onTagSelectReq: {
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
