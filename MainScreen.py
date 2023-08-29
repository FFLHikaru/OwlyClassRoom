from PyQt5.QtWidgets import QSizePolicy,QWidget,QGridLayout , QLabel,QPushButton,QVBoxLayout,QStackedWidget,QHBoxLayout
import csv
from ScannerScreen import ScannerScreen
from ResultatsScreen import ResultatsScreen
from QuestionGestureScreen import QuestionGestureScreen

class MainScreen(QWidget):
    def __init__(self,nomClasse):
        super().__init__()
        listeElevesResultats=[]
        with open(f"listeEleves{nomClasse}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                listeElevesResultats.append(ligne)
        
        listeQuestions=[]
        with open(f"listeQuestion{nomClasse}.csv",newline="") as fichier : 
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur :
                listeQuestions.append(ligne)
#########################################################################################################

        layout = QVBoxLayout()
        def scannerBoutonClicked():
            subMainScreen.setCurrentWidget(scannerScreen)
            scannerScreen.mainGrid.cameraScreen.camera.start()
            scannerScreen.bottomButtonsBar.setCurrentWidget(scannerScreen.buttonDemarrerScan)
        def resultatBoutonClicked():
            subMainScreen.setCurrentWidget(resultatsScreen)
            scannerScreen.mainGrid.cameraScreen.camera.stop()
        
        def question_gesture_button_on_click():
            if( subMainScreen.currentWidget == scannerScreen ):
                scannerScreen.mainGrid.cameraScreen.camera.stop()
            subMainScreen.setCurrentWidget(question_gesture_screen)
            
        scannerScreen=ScannerScreen(listeElevesResultats,listeQuestions,nomClasse)
        resultatsScreen=ResultatsScreen()
        question_gesture_screen=QuestionGestureScreen()

        subMainScreen=QStackedWidget()
        subMainScreen.addWidget(scannerScreen)
        subMainScreen.addWidget(resultatsScreen)
        subMainScreen.addWidget(question_gesture_screen)
        subMainScreen.setCurrentWidget(scannerScreen)
        
        lowerTabBar=QWidget()
        layoutLowerTabBar=QHBoxLayout()
        scannerBouton=QPushButton('Scanner')
        scannerBouton.clicked.connect(scannerBoutonClicked)
        scannerBouton.setStyleSheet('''
                                              QPushButton{
                                              font:bold;
                                              font-size:20px;
                                              border-radius:100px;
                                              border-color:black;
                                              border-width:2px;
                                              border-style:dotted;
                                              background-color:white;
                                              }

                                              QPushButton:hover{
                                              background-color:#D4E2EF;
                                              }
                                              ''')
        resultatBouton=QPushButton('Résultats')
        resultatBouton.setStyleSheet('''
                                              QPushButton{
                                              font:bold;
                                              font-size:20px;
                                              border-radius:30px;
                                              border-color:black;
                                              border-width:2px;
                                              border-style:dotted;
                                              background-color:white;
                                              }

                                              QPushButton:hover{
                                              background-color:#D4E2EF;
                                              }
                                              ''')
        question_gesture_button=QPushButton('Gérer les questions')
        question_gesture_button.setStyleSheet('''
                                              QPushButton{
                                              font:bold;
                                              font-size:20px;
                                              border-radius:30px;
                                              border-color:black;
                                              border-width:2px;
                                              border-style:dotted;
                                              background-color:white;
                                              }

                                              QPushButton:hover{
                                              background-color:#D4E2EF;
                                              }
                                            ''')


        resultatBouton.clicked.connect(resultatBoutonClicked)
        question_gesture_button.clicked.connect(question_gesture_button_on_click)

        layoutLowerTabBar.addWidget(scannerBouton)
        layoutLowerTabBar.addWidget(resultatBouton)
        layoutLowerTabBar.addWidget(question_gesture_button)
        
        lowerTabBar.setLayout(layoutLowerTabBar)        
        layout.addWidget(subMainScreen)
        layout.addWidget(lowerTabBar)
        
        self.setLayout(layout)
    
    
    