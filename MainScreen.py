from PyQt5.QtWidgets import QSizePolicy,QWidget,QGridLayout , QLabel,QPushButton,QVBoxLayout,QStackedWidget,QHBoxLayout
import csv
from ScannerScreen import ScannerScreen
from ResultatsScreen import ResultatsScreen
from QuestionGestureScreen import QuestionGestureScreen
from ClassGestureScreen import ClassGestureScreen
from ScanStudentScreen import ScanStudentScreen
from copy import deepcopy

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
            if subMainScreen.currentWidget == scan_student_screen:
                scan_student_screen.stop_scan()

            subMainScreen.setCurrentWidget(scannerScreen)
            scannerScreen.mainGrid.cameraScreen.camera.start()
            scannerScreen.bottomButtonsBar.setCurrentWidget(scannerScreen.buttonDemarrerScan)
            

        def resultatBoutonClicked():
            if subMainScreen.currentWidget().has_camera() :
                print('caméra stopped')
                subMainScreen.currentWidget().stop_scan()
            subMainScreen.setCurrentWidget(resultatsScreen)

        
        def question_gesture_button_on_click():
            if subMainScreen.currentWidget().has_camera() :
                print('caméra stopped')
                subMainScreen.currentWidget().stop_scan()
            subMainScreen.setCurrentWidget(question_gesture_screen)
        
        def class_gesture_button_on_click():
            if subMainScreen.currentWidget().has_camera() :
                print('caméra stopped')
                subMainScreen.currentWidget().stop_scan()
            subMainScreen.setCurrentWidget(class_gesture_screen)

        def scan_student_button_on_click():
            if subMainScreen.currentWidget().has_camera() :
                print('caméra stopped')
                subMainScreen.currentWidget().stop_scan()
            scan_student_screen.start_scan()
            subMainScreen.setCurrentWidget( scan_student_screen )
            
        scannerScreen=ScannerScreen(listeElevesResultats,listeQuestions,nomClasse)
        resultatsScreen=ResultatsScreen()
        question_gesture_screen=QuestionGestureScreen()
        class_gesture_screen=ClassGestureScreen(nomClasse)
        scan_student_screen = ScanStudentScreen( deepcopy( listeElevesResultats ) )

        subMainScreen=QStackedWidget()
        subMainScreen.addWidget(scannerScreen)
        subMainScreen.addWidget(resultatsScreen)
        subMainScreen.addWidget(question_gesture_screen)
        subMainScreen.addWidget(class_gesture_screen)
        subMainScreen.addWidget( scan_student_screen )

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
        class_gesture_button=QPushButton('Vie de classe')
        class_gesture_button.setStyleSheet('''
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
        
        scan_student_button=QPushButton(' Vérif devoir ')
        scan_student_button.setStyleSheet('''
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
        class_gesture_button.clicked.connect(class_gesture_button_on_click)
        scan_student_button.clicked.connect( scan_student_button_on_click)

        layoutLowerTabBar.addWidget(scannerBouton)
        layoutLowerTabBar.addWidget(resultatBouton)
        layoutLowerTabBar.addWidget(class_gesture_button)
        layoutLowerTabBar.addWidget(question_gesture_button)
        layoutLowerTabBar.addWidget(scan_student_button)
        
        
        lowerTabBar.setLayout(layoutLowerTabBar)        
        layout.addWidget(subMainScreen)
        layout.addWidget(lowerTabBar)
        
        self.setLayout(layout)
    
    
    