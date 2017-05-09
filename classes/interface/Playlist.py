#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the playlist's collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: May 09th 2017
#---------------------------------

import os
import random

from classes.interface import MainWindow
from classes.library.Library import Library
from classes.library.Track import Track
from classes.multimedia.MusicPlayer import MusicPlayer

from PyQt5 import Qt
from PyQt5.QtCore import QFileInfo, QUrl, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QFileDialog, QAbstractItemView, QShortcut, QProgressBar

class Playlist(QWidget):

    def __init__(self,mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.tracks = []
        self.label = ''
        self.musicPlayer = MusicPlayer(mainWindow)

        #Label of the tracklist
        playlistVerticalLayout = QVBoxLayout()
        self.label = QLabel(self.mainWindow.text.localisation('labels','playlistLabel','caption'))
        self.label.setAlignment(Qt.Qt.AlignCenter)
        playlistVerticalLayout.addWidget(self.label)

        #tracklist
        self.trackList = QListWidget()
        self.trackList.itemSelectionChanged.connect(lambda *args: self.toggleSuppressButton())
        self.trackList.setSelectionMode(QAbstractItemView.SingleSelection)
        playlistVerticalLayout.addWidget(self.trackList)

        #Duration bar
        self.durationBar = QProgressBar()
        self.durationBar.setTextVisible(False)
        self.durationBar.setMinimum(0)
        playlistVerticalLayout.addWidget(self.durationBar)

        self.durationTimer = QTimer()
        self.durationTimer.setInterval(1000)
        self.durationTimer.timeout.connect(lambda *args: self.updateDurationBar())

        #Controls of the tracklist
        controlsWidget = QWidget(self)
        genericLayout = QHBoxLayout()

        #play button
        playButton = QPushButton()
        playButton.setIcon(QIcon('ressources/interface/play.png'))
        playButtonShortcut = QShortcut(Qt.Qt.Key_Space,self.mainWindow)
        playButtonShortcut.activated.connect(lambda *args: playButton.animateClick())
        playButton.setMaximumWidth(40)
        playButton.clicked.connect(lambda *args: self.playMusic())
        genericLayout.addWidget(playButton)

        #add button
        addButton = QPushButton(self.mainWindow.text.localisation('buttons','addMusic','caption'))
        addButton.setMaximumWidth(150)
        addButton.clicked.connect(lambda *args: self.addMusicToList())
        addButton.setEnabled(False)
        genericLayout.addWidget(addButton)
        self.addMusicButton = addButton

        #remove button
        removeButton = QPushButton(self.mainWindow.text.localisation('buttons','removeMusic','caption'))
        removeButton.setMaximumWidth(150)
        removeButton.clicked.connect(lambda *args: self.removeMusicFromList())
        removeButton.setEnabled(False)
        genericLayout.addWidget(removeButton)
        self.removeMusicButton = removeButton

        #stop button
        stopButton = QPushButton()
        stopButton.setIcon(QIcon('ressources/interface/stop.png'))
        stopButton.setMaximumWidth(40)
        stopButton.clicked.connect(lambda *args: self.stopMusic())
        genericLayout.addWidget(stopButton)

        controlsWidget.setLayout(genericLayout)
        playlistVerticalLayout.addWidget(controlsWidget)

        self.setLayout(playlistVerticalLayout)

    def setList(self,text:str='', tracks:dict=None):
        """Update the tracklist with the provided list of tracks and
            sets the track list label to specified text. Also plays a track of the theme at random if
            theme selection occurs while the music player is active.
            Takes two parameters:
            - text as string
            - list of tracks as a dictionnary of track objects
        """
        self.label.setText(text)
        self.trackList.clear()
        self.tracks = tracks

        for track in tracks:
            self.trackList.addItem(track.name)

        self.addMusicButton.setEnabled(True)

        #Launch a random track if the music player is active.
        if self.musicPlayer.isPlaying():
            self.playMusicAtRandom()

    def initiateDurationBar(self, duration:int):
        """Set the duration bar and start/restart a timer to display progression.
            Takes one parameter:
            - duration as integer.
        """
        self.durationBar.setMaximum(duration)
        self.durationBar.setValue(0)
        self.durationTimer.start()

    def updateDurationBar(self):
        """Updates the duration bar value.
            Takes no parameter.
        """
        self.durationBar.setValue(self.durationBar.value()+1000)

        if self.durationBar.value() >= self.durationBar.maximum():
            self.durationTimer.stop()
            self.durationTimer.timeout.disconnect()

    def resetDurationBar(self):
        """Set duration bar to 0 and stop the duration timer.
            Takes no parameter.
        """
        self.durationBar.setValue(0)
        self.durationTimer.stop()
        self.durationTimer.timeout.disconnect()

    def addMusicToList(self):
        """Calls a file dialog to choose a music to add to the tracklist.
            Takes no parameter.
        """
        filesList, ok = QFileDialog().getOpenFileNames(self,self.mainWindow.text.localisation('dialogBoxes','addMusic','caption'),os.path.expanduser('~'),"*.mp3 *.wav *.ogg *.flac *.wma *.aiff *.m4a")
        if ok :
            for filePath in filesList :
                name = QFileInfo(filePath).fileName()
                self.tracks.append(Track(name,filePath))
                self.trackList.addItem(name)

    def playNextMedia(self):
        """Select the next media of the list and gives it to the player.
            Takes no parameter.
        """
        nextRow = self.trackList.currentRow()+1
        maxRow = self.trackList.count()

        #Restart at top of the list if the end is reached
        if nextRow >= maxRow :
            nextRow = 0

        self.trackList.setCurrentRow(nextRow)
        self.playMusic()

    def removeMusicFromList(self):
        """Remove the selected music from the tracklist.
            Takes no parameter.
        """
        print('delete')

    def toggleSuppressButton(self):
        """(De)activate the suppress button.
            Takes no parameter.
        """
        if self.trackList.currentItem():
            self.removeMusicButton.setEnabled(True)
        else :
            self.removeMusicButton.setEnabled(False)

    def reset(self):
        """Empty the playlist widget and reset the title label.
            Takes no parameter
        """
        self.label.setText(self.mainWindow.text.localisation('labels','playlistLabel','caption'))
        self.trackList.clear()
        self.addMusicButton.setEnabled(False)

    def playMusic(self):
        """Send the selected file to the music player.
            Takes no parameter.
        """
        if self.trackList.currentItem():
            found = False
            selectedItem = self.trackList.currentItem().text()

            for track in self.tracks :
                if track.name == selectedItem :
                    filepath = track.location
                    found = True

            if found:
                fileUrl = QUrl.fromLocalFile(filepath)
                media = QMediaContent(fileUrl)
                self.musicPlayer.changeMusic(media)

    def playMusicAtRandom(self):
        """Choose randomly a track to play.
            Takes no parameter
        """
        numberOfTracks = len(self.tracks)
        randomTrackNumber = random.randrange(0,numberOfTracks-1)

        self.trackList.setCurrentRow(randomTrackNumber)
        self.playMusic()

    def stopMusic(self):
        """Stop the music player.
            Takes no parameter
        """
        self.musicPlayer.stop()
        self.resetDurationBar()
