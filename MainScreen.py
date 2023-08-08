from PyQt5.QtWidgets import QSizePolicy,QWidget,QGridLayout , QLabel,QPushButton,QVBoxLayout,QStackedWidget,QHBoxLayout
import csv
from ScannerScreen import ScannerScreen
from ResultatsScreen import ResultatsScreen

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
            scannerScreen.camera.start()
            scannerScreen.bottomButtonsBar.setCurrentWidget(scannerScreen.buttonDemarrerScan)
        def resultatBoutonClicked():
            subMainScreen.setCurrentWidget(resultatsScreen)
            scannerScreen.camera.stop()
            
        scannerScreen=ScannerScreen(listeElevesResultats,listeQuestions,nomClasse)
        
        subMainScreen=QStackedWidget()
        
        
        resultatsScreen=ResultatsScreen()
        subMainScreen.addWidget(scannerScreen)
        subMainScreen.addWidget(resultatsScreen)
        subMainScreen.setCurrentWidget(scannerScreen)
        
        lowerTabBar=QWidget()
        layoutLowerTabBar=QHBoxLayout()
        scannerBouton=QPushButton('Scanner')
        scannerBouton.clicked.connect(scannerBoutonClicked)
        resultatBouton=QPushButton('Résultats')
        resultatBouton.clicked.connect(resultatBoutonClicked)
        layoutLowerTabBar.addWidget(scannerBouton)
        layoutLowerTabBar.addWidget(resultatBouton)
        lowerTabBar.setLayout(layoutLowerTabBar)
        
        
        layout.addWidget(subMainScreen)
        layout.addWidget(lowerTabBar)
        
        self.setLayout(layout)
    
    
    