/**************************************************************************
**   Calculator
**   Copyright (C) 2017 /dej/uran/dom team
**   Authors: Son Hai Nguyen
**   Credits: Josef Kolář, Son Hai Nguyen, Martin Omacht, Robert Navrátil
**
**   This program is free software: you can redistribute it and/or modify
**   it under the terms of the GNU General Public License as published by
**   the Free Software Foundation, either version 3 of the License, or
**   (at your option) any later version.
**
**   This program is distributed in the hope that it will be useful,
**   but WITHOUT ANY WARRANTY; without even the implied warranty of
**   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**   GNU General Public License for more details.
**
**   You should have received a copy of the GNU General Public License
**   along with this program.  If not, see <http://www.gnu.org/licenses/>.
**************************************************************************/
import QtQuick 2.0

/**
  Button with label and simple animation
  */
FilledClickable {
    id: component

    /// Label of button
    property alias buttonText: innerText.text;
    /// Text color
    property color textColor

    hoverMaskEnabled: true
    hoverEnabled: true

    Text {
        id: innerText

        color: textColor

        font.family: "Roboto Light"
        font.pixelSize: component.height * 0.55

        anchors.centerIn: parent
    }
}
