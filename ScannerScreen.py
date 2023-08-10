from PyQt5.QtWidgets import QLabel,QFrame,QVBoxLayout,QStackedWidget,QPushButton,QHBoxLayout,QListView,QWidget,QGridLayout
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import QStringListModel,QItemSelectionModel,QTimer,Qt
from PyQt5.QtMultimedia import QCamera, QCameraInfo,QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import random
import csv
from scannerScreenComposants.NeumorphicLabel import NeumorphicLabel
from scannerScreenComposants.QuizzScreen import QuizzScreen

class ScannerScreen(QFrame):
    nomClasse=''
    bonneReponse=''
    reponseScanned=[]
    questionEnCours=[]
    quizzScreen=None
    listeResultats=[]

    def qimage_to_cvimage(self, qimage):
        # Conversion de QImage à numpy array (OpenCV utilise des numpy arrays pour le traitement d'image)
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)
        return arr
    def capturerImage(self):
        if self.scanning:
            self.recordingObject.capture()
    def melangerQuestion(self,question):
        reponse=['A','B','C','D']
        trueAnswer=question[1]
        reponses=question[1:5]
        random.shuffle(reponses)
        questionShuffled=question
        questionShuffled[1:5]=reponses
        i=1
        while questionShuffled[i]!=trueAnswer:
            i+=1
        self.bonneReponse=reponse[i-1]
        return questionShuffled
    def analyserReponses(self):
        
      
        for reponse in self.reponseScanned:
            chaine_sans_crochets = self.listeResultats[reponse[1]][self.questionEnCours[1]].strip('[]')
            valeurs = chaine_sans_crochets.split(', ')
            strConvertedList = [int(valeur) for valeur in valeurs]
            if reponse[0]==self.bonneReponse:
                strConvertedList[0]+=1
            strConvertedList[1]+=1
            elementChained=[str(element) for element in strConvertedList]
            chaine_resultante = '[' + ', '.join(elementChained) + ']'
            self.listeResultats[reponse[1]][self.questionEnCours[1]]=chaine_resultante
            # Enregistrement du tableau dans un fichier CSV
        with open(f"listeEleves{self.nomClasse}.csv", newline="",mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in self.listeResultats:
                writer.writerow(ligne)
    def analyserImage(self, requestId, image):
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
        markersInclinaison,markerIds,nonMarker=detector.detectMarkers(gray_image)
        
        if len(markersInclinaison)>0:
            for j in range(len(markerIds)):
                incl=markersInclinaison[j][0]
                dx=incl[1][0]-incl[0][0]
                dy=incl[1][1]-incl[0][1]
                if abs(dy/(dx+1))<0.5:
                    self.colorierPrenom(markerIds[j][0])
                    if dx>0:
                    
                        if len(self.reponseScanned)>0:
                            existeDeja=False
                            for rep in range(len(self.reponseScanned)):
                                if self.reponseScanned[rep][1]==markerIds[j][0]:
                                    self.reponseScanned[rep][0]='A'
                                    existeDeja=True
                            if  not existeDeja:
                                self.reponseScanned.append(['A',markerIds[j][0]])
                        else:
                            self.reponseScanned.append(['A',markerIds[j][0]])
                            
                        
                    else:
                        if len(self.reponseScanned)>0:
                            existeDeja=False
                            for rep in range(len(self.reponseScanned)):
                                if self.reponseScanned[rep][1]==markerIds[j][0]:
                                    self.reponseScanned[rep][0]='B'
                                    existeDeja=True
                            if not existeDeja:
                                self.reponseScanned.append(['B',markerIds[j][0]])
                        else:
                            self.reponseScanned.append(['B',markerIds[j][0]])
                elif abs(dy/(dx+1))>=0.50:
                    self.colorierPrenom(markerIds[j][0])
                    if dy>0:
                        if len(self.reponseScanned)>0:
                            existeDeja=False
                            for rep in range(len(self.reponseScanned)):
                                if self.reponseScanned[rep][1]==markerIds[j][0]:
                                    self.reponseScanned[rep][0]='C'
                                    existeDeja=True
                            if not existeDeja:
                                self.reponseScanned.append(['C',markerIds[j][0]])
                        else:
                            self.reponseScanned.append(['C',markerIds[j][0]])
                    else:
                        if len(self.reponseScanned)>0:
                            existeDeja=False
                            for rep in range(len(self.reponseScanned)):
                                if self.reponseScanned[rep][1]==markerIds[j][0]:
                                    self.reponseScanned[rep][0]='D'
                                    existeDeja=True
                            if not existeDeja:
                                self.reponseScanned.append(['D',markerIds[j][0]])
                        else:
                            self.reponseScanned.append(['D',markerIds[j][0]])   
    def colorierPrenom(self,id):
        if id>len(self.listePrenomGauche):
            index=self.listeModelDroite.index(id-len(self.listePrenomGauche)-1,0)
            self.selectionModelDroite.select(index,QItemSelectionModel.Select)
        else:
            index = self.list_modelGauche.index(id-1, 0)
            self.selectionModelGauche.select(index, QItemSelectionModel.Select)
    def selectQuestion(self,lQuestions):
        listePoids=[]
        additionner=0
        idFinal =0
        for question in lQuestions[1:]:
            additionner+=float(question[-1])
            listePoids.append(additionner)
        randomNumber=random.uniform(0, listePoids[-1])
        for poid in listePoids:
            if randomNumber<=poid:
                idFinal+=1
        questionMelange=self.melangerQuestion(lQuestions[idFinal])
        self.quizzScreen.setQuestion(questionMelange)
        
        return [questionMelange,idFinal]
    
    def __init__(self,listeElevesResultats,listeQuestions,nomClasse):
        
        self.reponseScanned=[]
        self.nomClasse=nomClasse
        self.listeResultats=listeElevesResultats
        self.scanning=False    
        super().__init__()
        self.quizzScreen=QuizzScreen()
        self.questionEnCours=self.selectQuestion(listeQuestions)
        self.setStyleSheet("QCameraViewfinder {height: 200px; width: 200px; border-style: solid; border-color: yellow; border-width: 20px; border-radius:120;} QPushButton {background-color: blue;}")
        layout=QVBoxLayout()
        questionScannerScreen=QWidget()
        questionScannerLayout=QHBoxLayout()
        
        viewfinder = QCameraViewfinder()
        questionScannerLayout.addWidget(self.quizzScreen,stretch=1)
        questionScannerLayout.addWidget(viewfinder,stretch=1)
        questionScannerScreen.setLayout(questionScannerLayout)
        
        
        middleLayout=QHBoxLayout()
        middleWidget=QFrame()
        
        
        listeGauche=QListView()
        listeGauche.setEditTriggers(QListView.NoEditTriggers)
        listeGauche.setSelectionMode(QListView.NoSelection)
       
        listeDroite=QListView()
        listeDroite.setEditTriggers(QListView.NoEditTriggers)
        listeDroite.setSelectionMode(QListView.NoSelection)
        
        
        self.listePrenomGauche=[ligne[0] for ligne in listeElevesResultats[1:(len(listeElevesResultats)-1)//2+1]]
        self.list_modelGauche=QStringListModel()
        self.list_modelGauche.setStringList(self.listePrenomGauche)
        listeGauche.setModel(self.list_modelGauche)
        
        listePrenomDroite=[ligne[0] for ligne in listeElevesResultats[(len(listeElevesResultats)-1)//2+1:]]
        self.listeModelDroite=QStringListModel()
        self.listeModelDroite.setStringList(listePrenomDroite)
        listeDroite.setModel(self.listeModelDroite)
        
        self.selectionModelGauche = QItemSelectionModel(self.list_modelGauche)
        self.selectionModelDroite=QItemSelectionModel(self.listeModelDroite)
        
        listeDroite.setSelectionModel(self.selectionModelDroite)
        listeGauche.setSelectionModel(self.selectionModelGauche)
        
        
        
        
        middleLayout.addWidget(listeGauche)
        middleLayout.addWidget(questionScannerScreen)
        middleLayout.addWidget(listeDroite)
        middleWidget.setLayout(middleLayout)
        layout.addWidget(middleWidget)
        
        self.camera = QCamera()
        self.recordingObject=QCameraImageCapture(self.camera)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        
        self.camera.setViewfinder(viewfinder)
        self.camera.start()  # Start the camera 
        self.bottomButtonsBar=QStackedWidget()
        
        self.buttonDemarrerScan=QPushButton("Démarrer le scan")
        self.bottomButtonsBar.addWidget(self.buttonDemarrerScan)
        
        self.buttonsPostScan=QFrame()
        buttonsPostScanLayout=QHBoxLayout()
        self.sendButton=QPushButton("enregistrer")
        self.cancelButton=QPushButton("cancel")
        buttonsPostScanLayout.addWidget(self.sendButton)
        buttonsPostScanLayout.addWidget(self.cancelButton)
        self.buttonsPostScan.setLayout(buttonsPostScanLayout)
        
        self.bottomButtonsBar.addWidget(self.buttonsPostScan)
        
        
        
        def DemarrerScan():
            self.bottomButtonsBar.setCurrentWidget(self.buttonsPostScan)
            self.scanning=True
            
        def AnnulerScan():
            self.bottomButtonsBar.setCurrentWidget(self.buttonDemarrerScan)
            self.scanning=False
            self.selectionModelGauche.clearSelection()
            self.selectionModelDroite.clearSelection()
            self.reponseScanned=[]
        def EnvoyerResultats():
            print(self.reponseScanned)
            self.bottomButtonsBar.setCurrentWidget(self.buttonDemarrerScan)
            self.scanning=False
            self.selectionModelGauche.clearSelection()
            self.selectionModelDroite.clearSelection()
            self.selectQuestion(listeQuestions)
            
            self.analyserReponses()
        
            
            
            
            
            
        timer = QTimer(self)
        timer.timeout.connect(self.capturerImage)
        timer.start(500)    
        
        
        self.buttonDemarrerScan.clicked.connect(DemarrerScan)
        self.cancelButton.clicked.connect(AnnulerScan)
        self.sendButton.clicked.connect(EnvoyerResultats)
        self.recordingObject.imageCaptured.connect(self.analyserImage)
        
        layout.addWidget(self.bottomButtonsBar)
        
        self.setLayout(layout)
        