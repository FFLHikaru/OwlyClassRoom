from PyQt5.QtWidgets import QLabel,QFrame,QVBoxLayout,QStackedWidget,QPushButton,QHBoxLayout,QListView,QWidget,QGridLayout,QGraphicsDropShadowEffect
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import QStringListModel,QItemSelectionModel,QTimer,Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon,QColor
import cv2
import numpy as np
import random
import csv
import copy
from scannerScreenComposants.NeumorphicLabel import NeumorphicLabel
from scannerScreenComposants.QuizzScreen import QuizzScreen
from scannerScreenComposants.MainGrid import MainGrid
from scannerScreenComposants.ListesScreen import ListesScreen
from scannerScreenComposants.GraphScreen import GraphScreen

class ScannerScreen(QFrame):
    nomClasse=''
    bonneReponse=''
    reponseScanned=[]
    questionEnCours=[]
    quizzScreen=None
    listeResultats=[]
    scanning=False
    mainGrid=None
    liste_questions=[]
    is_responses_showed=False

    def on_afficher_reponses_eleves_clicked(self):
        if not self.is_responses_showed:
            self.mainGrid.listesScreen.set_all_scanned_responses(self.reponseScanned)
            self.is_responses_showed = True
        else : 
            self.mainGrid.listesScreen.delete_all_responses()
            self.is_responses_showed = False

    def destroyCreate(self,afficherGraph):
        if self.mainGrid.visibleGraph:
            self.mainGrid.graphScreen.deleteLater()
            self.mainGrid.visibleGraph=False
        else:
            self.mainGrid.graphScreen=GraphScreen(self.reponseScanned)
            self.mainGrid.layout.addWidget(self.mainGrid.graphScreen,1,1,14,14)
            self.mainGrid.visibleGraph=True

    def melangerQuestion(self,question):
        reponse=['A','B','C','D']
        trueAnswer=question[1]
        reponses=question[1:5]
        random.shuffle(reponses)
        questionShuffled=copy.deepcopy(question)
        questionShuffled[1:5]=reponses
        i=1
        while questionShuffled[i]!=trueAnswer:
            i+=1
        self.bonneReponse=reponse[i-1]

    
        
        return questionShuffled
    
    def analyserReponses(self):
        nombre_reponses=0
        nombre_bonnes_reponses=0
        for reponse in self.reponseScanned:
            chaine_sans_crochets = self.listeResultats[reponse[1]][self.questionEnCours[1]].strip('[]')
            valeurs = chaine_sans_crochets.split(', ')
            strConvertedList = [int(valeur) for valeur in valeurs]
            if reponse[0]==self.bonneReponse:
                nombre_bonnes_reponses+=1
                strConvertedList[0]+=1
            nombre_reponses+=1
            strConvertedList[1]+=1
            elementChained=[str(element) for element in strConvertedList]
            chaine_resultante = '[' + ', '.join(elementChained) + ']'
            self.listeResultats[reponse[1]][self.questionEnCours[1]]=chaine_resultante
            # Enregistrement du tableau dans un fichier CSV
        with open(f"listeEleves{self.nomClasse}.csv", newline="",mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in self.listeResultats:
                writer.writerow(ligne)
        if self.reponseScanned!=[]:
           
            self.liste_questions[self.questionEnCours[-1]][-1]=str(nombre_bonnes_reponses/nombre_reponses)
        with open(f"listeQuestion{self.nomClasse}.csv", newline='', mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in self.liste_questions:
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
                                    if self.is_responses_showed:
                                        self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' A')
                                    existeDeja=True
                            if  not existeDeja:
                                self.reponseScanned.append(['A',markerIds[j][0]])
                                if self.is_responses_showed:
                                    self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' A')
                        else:
                            self.reponseScanned.append(['A',markerIds[j][0]])
                            if self.is_responses_showed:
                                self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' A')
                            
                        
                    else:
                        if len(self.reponseScanned)>0:
                            existeDeja=False
                            for rep in range(len(self.reponseScanned)):
                                if self.reponseScanned[rep][1]==markerIds[j][0]:
                                    self.reponseScanned[rep][0]='B'
                                    existeDeja=True
                                    if self.is_responses_showed:
                                        self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' B')
                            if not existeDeja:
                                self.reponseScanned.append(['B',markerIds[j][0]])
                                if self.is_responses_showed:
                                    self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' B')
                        else:
                            self.reponseScanned.append(['B',markerIds[j][0]])
                            if self.is_responses_showed:
                                self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' B')

                elif abs(dy/(dx+1))>=0.50:
                    self.colorierPrenom(markerIds[j][0])
                    if dy>0:
                        if len(self.reponseScanned)>0:
                            existeDeja=False
                            for rep in range(len(self.reponseScanned)):
                                if self.reponseScanned[rep][1]==markerIds[j][0]:
                                    self.reponseScanned[rep][0]='C'
                                    existeDeja=True
                                    if self.is_responses_showed:
                                        self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' C')
                            if not existeDeja:
                                self.reponseScanned.append(['C',markerIds[j][0]])
                                if self.is_responses_showed:
                                    self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' C')
                        else:
                            self.reponseScanned.append(['C',markerIds[j][0]])
                            if self.is_responses_showed:
                                self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' C')
                    else:
                        if len(self.reponseScanned)>0:
                            existeDeja=False
                            for rep in range(len(self.reponseScanned)):
                                if self.reponseScanned[rep][1]==markerIds[j][0]:
                                    self.reponseScanned[rep][0]='D'
                                    existeDeja=True
                                    if self.is_responses_showed:
                                        self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' D')
                            if not existeDeja:
                                self.reponseScanned.append(['D',markerIds[j][0]])
                                if self.is_responses_showed:
                                    self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' D')
                        else:
                            self.reponseScanned.append(['D',markerIds[j][0]]) 
                            if self.is_responses_showed:
                               self.mainGrid.listesScreen.set_response_to_eleve(markerIds[j][0], ' D')

    
    def qimage_to_cvimage(self, qimage):
        # Conversion de QImage à numpy array (OpenCV utilise des numpy arrays pour le traitement d'image)
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width, height = qimage.width(), qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)
        return arr
    

    def colorierPrenom(self,id):
        if id>len(self.mainGrid.listesScreen.listePrenomGauche):
            index=self.mainGrid.listesScreen.listeModelDroite.index(id-len(self.mainGrid.listesScreen.listePrenomGauche)-1,0)
            self.mainGrid.listesScreen.selectionModelDroite.select(index,QItemSelectionModel.Select)
        else:
            index = self.mainGrid.listesScreen.listModelGauche.index(id-1, 0)
            self.mainGrid.listesScreen.selectionModelGauche.select(index, QItemSelectionModel.Select)

    def selectQuestion(self,lQuestions):
        copy_lQuestion = lQuestions[:]
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
        questionMelange=self.melangerQuestion(copy_lQuestion[idFinal])
        self.mainGrid.quizzScreen.setQuestion(questionMelange)
        

        return [questionMelange,idFinal]
    
    def __init__(self,listeElevesResultats,listeQuestions,nomClasse):
        self.liste_questions=copy.deepcopy(listeQuestions[:])
        self.reponseScanned=[]
        self.nomClasse=nomClasse
        self.listeResultats=listeElevesResultats
        self.scanning=False 
        super().__init__()
        layout=QVBoxLayout()
        self.mainGrid=MainGrid(listeElevesResultats)
        self.questionEnCours=self.selectQuestion(listeQuestions)
     
    
        
        
       
        layout.addWidget(self.mainGrid,stretch=9)


        self.bottomButtonsBar=QStackedWidget()
        
        self.buttonDemarrerScan=QPushButton("Démarrer le scan")
        self.buttonDemarrerScan.setStyleSheet('''
                                              QPushButton{
                                              font:bold;
                                              font-size:30px;
                                              border-radius:30px;
                                              border-color:black;
                                              border-width:2px;
                                              border-style:dotted;
                                              background-color:#E1ECF4;
                                              }

                                              QPushButton:hover{
                                              background-color:#D4E2EF;
                                              }
                                              ''')
        self.bottomButtonsBar.addWidget(self.buttonDemarrerScan)
        

        
        self.buttonsPostScan=QFrame()
        buttonsPostScanLayout=QHBoxLayout()
        self.sendButton=QPushButton("enregistrer")
        self.sendButton.setStyleSheet('font:bold;font-size:20px')
        self.cancelButton=QPushButton("cancel")
        self.cancelButton.setStyleSheet('font:bold;font-size:20px;')
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
            self.mainGrid.listesScreen.selectionModelGauche.clearSelection()
            self.mainGrid.listesScreen.selectionModelDroite.clearSelection()
            self.questionEnCours=self.selectQuestion(listeQuestions)
            self.reponseScanned=[]
            self.mainGrid.listesScreen.delete_all_responses()
            self.is_responses_showed = False
            
        def EnvoyerResultats():
            self.analyserReponses()
            self.bottomButtonsBar.setCurrentWidget(self.buttonDemarrerScan)
            self.scanning=False
            self.mainGrid.listesScreen.selectionModelGauche.clearSelection()
            self.mainGrid.listesScreen.selectionModelDroite.clearSelection()
            self.questionEnCours=self.selectQuestion(listeQuestions)
            self.reponseScanned=[]
            self.mainGrid.listesScreen.delete_all_responses()
            self.is_responses_showed = False
            
            
        
         
        
            
            
            
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.mainGrid.cameraScreen.capturerImage(self.scanning))
        timer.start(500)    
        
        
        self.buttonDemarrerScan.clicked.connect(DemarrerScan)
        self.cancelButton.clicked.connect(AnnulerScan)
        self.sendButton.clicked.connect(EnvoyerResultats)
        self.mainGrid.cameraScreen.recordingObject.imageCaptured.connect(self.analyserImage)
        self.mainGrid.graphiqueButton.clicked.connect(self.destroyCreate)
        self.mainGrid.afficher_reponses_eleves.clicked.connect(self.on_afficher_reponses_eleves_clicked)
        layout.addWidget(self.bottomButtonsBar,stretch=1)
        
        self.setLayout(layout)
        