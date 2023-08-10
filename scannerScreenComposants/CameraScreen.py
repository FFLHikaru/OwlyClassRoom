
from PyQt5.QtWidgets import QWidget,QSizePolicy,QHBoxLayout
from PyQt5.QtMultimedia import QCamera, QCameraInfo,QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
class CameraScreen(QWidget):
    camera=None
    recordingObject=None
    viewfinder=None

    def capturerImage(self,scanning):
        if scanning:
            self.recordingObject.capture()

    def __init__(self):

        super().__init__()
        
        layout=QHBoxLayout()
        self.viewfinder=QCameraViewfinder()
        self.camera = QCamera()
        self.recordingObject=QCameraImageCapture(self.camera)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.setViewfinder(self.viewfinder)
        self.camera.start()  # Start the camera 
        layout.addWidget(self.viewfinder)
        self.setLayout(layout)
