from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import cv2
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Player")
        self.setGeometry(350, 100, 1000, 700)
        self.setWindowIcon(QIcon("Play.png"))
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        self.UserInterface()
        self.show()
    def UserInterface(self):
        # Creating media player Object........
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # Creating Video Widget Object........
        videoWidget = QVideoWidget()
        faceDetetction = QPushButton("Face Detection")
        faceDetetction.clicked.connect(self.faceDetect)
        openBtn = QPushButton("Open video")  # Creating open Button...
        openBtn.clicked.connect(self.openFile)
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.playVideo)
        # Creating Slider.......
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)
        # Creating label........
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        # Creating hbox Layouts......
        hBoxLayout = QHBoxLayout()
        hBoxLayout.setContentsMargins(0, 0, 0, 0)
        hBoxLayout.addWidget(self.playBtn)
        hBoxLayout.addWidget(self.slider)
        # Creating Vbox layout.......
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(videoWidget)
        vBoxLayout.addLayout(hBoxLayout)
        #vBoxLayout.addWidget(self.label)
        vBoxLayout.addWidget(openBtn)
        vBoxLayout.addWidget(faceDetetction)
        self.setLayout(vBoxLayout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.statechanged)
        self.mediaPlayer.positionChanged.connect(self.PositionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open video", "", "mp4 Video (*.mp4);Movie files (*.mov);All files (*.*)")
        if filename != " ":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
    def playVideo(self):
        if self.mediaPlayer.state() == self.mediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    def faceDetect(self):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        capture = cv2.VideoCapture(0)
        while (True):
            ret, frame = capture.read()
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=5)
            for x, y, w, h in face:
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.imshow("Video", frame)
            if len(face) < 1:
                self.mediaPlayer.pause()
                self.mediaPlayer.stateChanged
                #self.mediaPlayer.stateChanged.connect(self.statechanged)
                self.mediaPlayer.positionChanged.connect(self.PositionChanged)
                self.mediaPlayer.durationChanged.connect(self.durationChanged)
            else:
                self.mediaPlayer.play()
                self.mediaPlayer.stateChanged
            if cv2.waitKey(1) == ord('q'):
                capture.release()
                sys.exit()
                cv2.destroyAllWindows()
                break
    def statechanged(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    def PositionChanged(self, position):
        self.slider.setValue(position)
    def durationChanged(self, duration):
        self.slider.setRange(0, duration)
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
