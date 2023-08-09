from PyQt5.QtWidgets import QWidget,QGridLayout , QLabel,QPushButton
from PyQt5.QtCore import pyqtSignal
import csv


class ClassSelectionScreen(QWidget):
    boutonClicked=pyqtSignal(str)
    def __init__(self):
        super().__init__()
        
        
        
###############################Lecture des classes#############################
        with open("listeClasses.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                listeClasses=ligne
###############################################################################       
##################################Grid Layout##################################
        layout=QGridLayout()
        for i in range(len(listeClasses)):
            bouton=QPushButton(listeClasses[i])
            bouton.setStyleSheet('QPushButton {border-radius: 20px; border: 3px solid black;}')

            bouton.clicked.connect(lambda checked, text=bouton.text(): self.boutonClicked.emit(text))
            layout.addWidget(bouton, i//2, i%2)
            print(i%2,i//2)
        self.setLayout(layout)
        
        