import cv2
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from scanStudentComposants.StudentButton import StudentButton
from scannerScreenComposants.CustomLayout import CustomLayout
from PyQt5.QtMultimedia import QCamera,QCameraImageCapture,QCameraInfo
from PyQt5.QtGui import QImage
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from scannerScreenComposants.RoundedButton import RoundedButton

class ScanStudentScreen( QWidget ):

    def __init__(self, student_list : list ) -> None:
        super().__init__() 

        #### Variable logique ####
        self.student_list = []
        self.scanned_student = []
        self.is_scanning = False

        #### Widgets ####

        self.timer = QTimer()
        self.camera = QCamera() 
        self.recording_object=QCameraImageCapture(self.camera)
        self.viewfinder = QCameraViewfinder()
          
        self.student_button_list = []
        self.grid_layout = CustomLayout()

        self.reset_color_button = RoundedButton( )
    
        

        #### Init logic ####
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.setViewfinder(self.viewfinder)
        

        self.student_list = result_list_to_student_list( student_list )
        self._create_all_student_button()       

        self.setLayout(self.grid_layout)

        self._set_button_on_grid()

        self.reset_color_button.setText(" reset selection ")
        self.grid_layout.addWidget(self.reset_color_button,5,6,1,1)

        #### signals connexion ####

        self.timer.timeout.connect( self.capturer_image )
        self.recording_object.imageCaptured.connect( self._scan_camera_image )
        self.reset_color_button.clicked.connect(self._reset_selection)
        

    #### Signals responses ####

    def capturer_image( self ) -> None : 
        self.recording_object.capture()
        return None
    
    def _reset_selection( self ) -> None : 
        for button in self.student_button_list : 
            button.reset_button()
        return None

    def _scan_camera_image( self, requestId, image ) -> None : 
        convertedImage = self.qimage_to_cvimage(image)
        # Convert the image to grayscale for QR code detection
        blurred_image = cv2.GaussianBlur(convertedImage, (5, 5), 0)
        gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_image = clahe.apply(gray_image)

        cv2.imwrite("gray_image2.jpg", enhanced_image)
        
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters()
        parameters.errorCorrectionRate = 0.6 


        detector = cv2.aruco.ArucoDetector(aruco_dict,parameters)
        markersInclinaison,markerIds,nonMarker=detector.detectMarkers(enhanced_image)

        if len(markersInclinaison)>0:
            for marker_id in markerIds :
                self._marker_detected(marker_id[0]-1)
                
        

        return None


    #### Built in ####

    def resizeEvent( self, event ) -> None:
        self.grid_layout.geometry_changed.emit( self.geometry() )

        return super().resizeEvent( event )


    #### Private Class methods ####

    def _create_all_student_button( self ) -> None :
        i = 0
        j = 0
        for student in self.student_list : 
            self.student_button_list.append( StudentButton( student ) )
        return None
    
    def _set_button_on_grid( self ) -> None : 
        i=0
        for student_button in self.student_button_list : 
            self.grid_layout.addWidget( student_button, i//7 , i%7, 1, 1 )
            i+=1
    
    def _marker_detected( self, id : int ) -> None : 
        self.student_button_list[ id ].marker_detected()

        return None

    #### Public class methods #### 

    def start_scan( self ) -> None : 
        print('camera started')
        self.is_scanning = True
        self.camera.start()
        self.timer.start(500) 
        

        return None
    
    def stop_scan( self ) -> None :
        self.camera.stop()
        self.is_scanning = False
        self.timer.stop()

    def has_camera( self ) -> bool :
        return True   

    def qimage_to_cvimage( self, qimage ):
        # Conversion de QImage à numpy array (OpenCV utilise des numpy arrays pour le traitement d'image)
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)
        return arr  
#### Fonction logique ####

def result_list_to_student_list( result_list : str ) -> list :
        student_list = []
        for student_result in result_list[1:] : 
            student_list.append(student_result[0])

        return student_list

def qimage_to_cvimage( qimage ):
        # Conversion de QImage à numpy array (OpenCV utilise des numpy arrays pour le traitement d'image)
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)
        return arr  




