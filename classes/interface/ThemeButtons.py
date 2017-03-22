#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the theme and its collection of buttons used in the themes widget
#
#Application: DragonShout music sampler
#Last Edited: February 21th 2017
#---------------------------------

from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget, QInputDialog

class ThemeButtons(QWidget):

    def __init__(self, themeName:str, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        layout = QHBoxLayout()

        #Theme button
        themeButton = QPushButton(themeName)
        themeButton.setMaximumWidth(100)
        themeButton.clicked.connect(lambda *args: self.selectTheme(self.sender().text()))
        self.themeButton = themeButton
        layout.addWidget(themeButton)

        #Edit button
        editButton = QPushButton('Edit')
        editButton.setMaximumWidth(50)
        editButton.clicked.connect(lambda *args: self.editThemeName(self.themeButton.text()))
        self.editButton = editButton
        layout.addWidget(editButton)

        #Remove button
        removeButton = QPushButton('X')
        removeButton.setMaximumWidth(20)
        removeButton.clicked.connect(lambda *args: self.mainWindow.themes.deleteTheme(self.themeButton.text(),self))
        self.removeButton = removeButton
        layout.addWidget(removeButton)

        self.setLayout(layout)

    def selectTheme(self,themeName:str):
        """Update the playlist with the music list of the selected theme.
            Takes one parameter:
            - themeName as string
        """
        theme = self.mainWindow.library.get_category(themeName)
        if theme :
            self.mainWindow.playlist.setList(themeName,theme.tracks)

    def editThemeName(self, themeName:str):
        """Change the name of a theme both in the UI and in the library.
            Takes one parameter:
            - themeName as string
        """
        newThemeName, ok = QInputDialog.getText(self,themeName,self.mainWindow.text.localisation('dialogBoxes','newTheme','question'))
        category = self.mainWindow.library.get_category(themeName)

        if ok and category:
            self.themeButton.setText(newThemeName)
            category.name = newThemeName

            if self.mainWindow.playlist.label.text() == themeName:
                self.mainWindow.playlist.label.setText(newThemeName)