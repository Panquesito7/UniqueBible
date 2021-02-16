if not __name__ == "__main__":
    import config
from functools import partial
from PySide2.QtGui import QColor
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QRadioButton, QComboBox, QHBoxLayout, QVBoxLayout, QLabel, QWidget, QPushButton, QColorDialog, QInputDialog, QLineEdit
from BibleVerseParser import BibleVerseParser
from BiblesSqlite import BiblesSqlite
from db.Highlight import Highlight

class HighlightLauncher(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # set title
        self.setWindowTitle("Highlight Editor" if __name__ == "__main__" else config.thisTranslation["highlightEditor"])
        # variables
        bookNo2Abb = BibleVerseParser(config.parserStandarisation).standardAbbreviation
        bookList = BiblesSqlite().getBookList(self.parent.parent.text)
        self.searchList = [config.thisTranslation["filter"], "{0}-{1}".format(bookNo2Abb["1"], bookNo2Abb["66"]), "{0}-{1}".format(bookNo2Abb["1"], bookNo2Abb["39"]), "{0}-{1}".format(bookNo2Abb["40"], bookNo2Abb["66"])] + [bookNo2Abb[str(b)] for b in bookList]
        # setup interface
        self.setupUI()

    # window appearance
    def resizeWindow(self, widthFactor, heightFactor):
        availableGeometry = QGuiApplication.instance().desktop().availableGeometry()
        self.setMinimumWidth(500)
        self.resize(availableGeometry.width() * widthFactor, availableGeometry.height() * heightFactor)

    def setupUI(self):
        codes = Highlight().isHighlighted(self.parent.parent.bibleTab.b, self.parent.parent.bibleTab.b, self.parent.parent.bibleTab.b)
        initialCode = None
        if codes:
            initialCode = codes[0]

        layout = QVBoxLayout()
        
        subLayout = QHBoxLayout()
        radioButton = QRadioButton()
        radioButton.toggled.connect(self.highlightOptionChanged)
        radioButton.setToolTip(config.thisTranslation["selectRemoveHighlight"])
        subLayout.addWidget(radioButton)
        subLayout.addWidget(QLabel(config.thisTranslation["noHightlight"]))
        layout.addLayout(subLayout)

        self.collectionButton1, self.collectionButton2, self.collectionButton3, self.collectionButton4, self.collectionButton5, self.collectionButton6, self.collectionButton7, self.collectionButton8, self.collectionButton9, self.collectionButton10 = QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton()
        self.collectionButtons = (self.collectionButton1, self.collectionButton2, self.collectionButton3, self.collectionButton4, self.collectionButton5, self.collectionButton6, self.collectionButton7, self.collectionButton8, self.collectionButton9, self.collectionButton10)
        self.collectionColourButton1, self.collectionColourButton2, self.collectionColourButton3, self.collectionColourButton4, self.collectionColourButton5, self.collectionColourButton6, self.collectionColourButton7, self.collectionColourButton8, self.collectionColourButton9, self.collectionColourButton10 = QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton(), QPushButton()
        self.collectionColourButtons = (self.collectionColourButton1, self.collectionColourButton2, self.collectionColourButton3, self.collectionColourButton4, self.collectionColourButton5, self.collectionColourButton6, self.collectionColourButton7, self.collectionColourButton8, self.collectionColourButton9, self.collectionColourButton10)
        for index, button in enumerate(self.collectionButtons):
            subLayout = QHBoxLayout()
            
            radioButton = QRadioButton()
            radioButton.setFixedWidth(20)
            radioButton.toggled.connect(lambda checked, option=index: self.highlightOptionChanged(checked, option))
            if initialCode is not None and int(initialCode[-1]) - 1 == index:
                radioButton.setChecked(True)
            radioButton.setToolTip(config.thisTranslation["selectApplyHighlight"])
            subLayout.addWidget(radioButton)

            button.setText("collection" if __name__ == "__main__" else config.highlightCollections[index])
            button.setToolTip(config.thisTranslation["rename"])
            button.clicked.connect(partial(self.rename, index))
            subLayout.addWidget(button)

            button = self.collectionColourButtons[index]
            button.setFixedWidth(50)
            buttonStyle = "QPushButton {0}background-color: {2}; color: {3};{1}".format("{", "}", config.highlightDarkThemeColours[index] if config.theme == "dark" else config.highlightLightThemeColours[index], "white" if config.theme == "dark" else "black")
            button.setStyleSheet(buttonStyle)
            button.setToolTip(config.thisTranslation["changeColour"])
            button.clicked.connect(partial(self.changeColor, index))
            subLayout.addWidget(button)
            combo = QComboBox()
            combo.addItems(self.searchList)
            combo.setFixedWidth(100)
            combo.currentIndexChanged.connect(lambda selectedIndex, index=index: self.searchHighlight(selectedIndex, index))
            subLayout.addWidget(combo)
            layout.addLayout(subLayout)

        self.setLayout(layout)

    def highlightOptionChanged(self, checked, option=None):
        if checked:
            if option is None:
                code = "delete"
            else:
                code = "hl{0}".format(option + 1)
            command = "_HIGHLIGHT:::{0}:::{1}".format(code, self.parent.parent.bibleTab.getSelectedReference())
            self.parent.parent.parent.reloadCurrentRecord()
            self.parent.parent.runTextCommand(command)

    def searchHighlight(self, selectedIndex, code):
        if selectedIndex != 0:
            scopes = {
                1: "all",
                2: "ot",
                3: "nt",
            }
            scope = scopes.get(selectedIndex, self.searchList[selectedIndex])
            command = "SEARCHHIGHLIGHT:::hl{0}:::{1}".format(code + 1, scope)
            self.parent.parent.runTextCommand(command)

    def rename(self, index):
        newName, ok = QInputDialog.getText(self, "QInputDialog.getText()",
                config.thisTranslation["edit"], QLineEdit.Normal,
                config.highlightCollections[index])
        if ok and newName:
            config.highlightCollections[index] = newName
            self.collectionButtons[index].setText(newName)

    def changeColor(self, index):
        color = QColorDialog.getColor(QColor(config.highlightDarkThemeColours[index] if config.theme == "dark" else config.highlightLightThemeColours[index]), self)
        if color.isValid():
            colorName = color.name()
            if config.theme == "dark":
                config.highlightDarkThemeColours[index] = colorName
            else:
                config.highlightLightThemeColours[index] = colorName
            button = self.collectionColourButtons[index]
            buttonStyle = "QPushButton {0}background-color: {2}; color: {3};{1}".format("{", "}", colorName, "white" if config.theme == "dark" else "black")
            button.setStyleSheet(buttonStyle)

if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    ui = HighlightLauncher(None)
    ui.show()
    sys.exit(app.exec_())
