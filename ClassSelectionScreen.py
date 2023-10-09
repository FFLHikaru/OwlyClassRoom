from PyQt5.QtWidgets import QWidget,QGridLayout , QLabel,QPushButton, QMessageBox, QVBoxLayout, QLineEdit, QInputDialog
from PyQt5.QtCore import pyqtSignal
import csv


class ClassSelectionScreen(QWidget):
    boutonClicked=pyqtSignal(str)
    def __init__(self):
        super().__init__()
        #### Logic ####
        self.class_name = ""

        #### Widget ####
        self.add_class_button = QPushButton('créer une classe')
        self.add_class_button.clicked.connect(self.show_input_dialog)
        
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
        layout.addWidget(self.add_class_button)

        self.setLayout(layout)
        
    #### Class methods ####

    def has_camera( self ) -> bool :
        return False   
    
    def show_input_dialog(self):
        # Créez une boîte de dialogue d'entrée texte
        text, ok = QInputDialog.getText(self, 'Créer une classe', 'Donner un nom à votre classe.')

        if ok:
            # Vérifiez si l'utilisateur a appuyé sur "OK" dans la boîte de dialogue
            if text.strip():  # Vérifiez si le texte n'est pas vide
                message = f'Vous avez créer la classe : {text}!'
                self.class_name = text
                self.create_resultat_file()
                self.create_question_file()
                self.create_comportement_list()
                self.append_class_list()
                self.boutonClicked.emit(text)
                
            else:
                message = 'Vous n\'avez pas saisi de nom.'
            QMessageBox.information(self, 'Résultat', message)
        # Affichez la boîte de dialogue
        return None
    
    def create_resultat_file( self ):
        with open(f"listeEleves{self.class_name}.csv", mode='w', newline='') as fichier_csv:
        # Créez un objet writer
            writer = csv.writer(fichier_csv)
            # Écrivez une ligne vide (ou rien du tout)
            writer.writerow([])
        return None
    def create_question_file( self ):
        with open(f"listeQuestion{self.class_name}.csv", mode='w', newline='') as fichier_csv:
        # Créez un objet writer
            writer = csv.writer(fichier_csv)
            # Écrivez une ligne vide (ou rien du tout)
            writer.writerow([])
        return None
    def create_comportement_list( self ) -> None : 
        comportement_table = [['','','Eleve 1'],['Comportements', 'Ne travaille pas -3', '0'],['', 'bavardage -1', '0'],['', 'Insolent -10', '0'],['', 'Perturbateur -4', '0'],['Investissement', 'Oubli matériel -1', '0'],['', 'Devoirs non fait -3', '0'],['', 'Devoirs non rendu -5', '0'],['', 'Retard -2', '0'],['Valoriser', 'devoir facultatif +4', '0'],['', 'participation +2', '0'],['', 'autre +1', '0']]
        with open(f"comportement{self.class_name}.csv", mode='w', newline='') as fichier_csv:

        # Créez un objet writer
            writer = csv.writer(fichier_csv,delimiter=";")
            for line in comportement_table : 
                # Écrivez une ligne vide (ou rien du tout)
                writer.writerow(line)
        return None
    
    def append_class_list( self ) -> None : 
        class_liste=[]
        with open(f"listeClasses.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                class_liste.append(ligne)
        class_liste[0].append(self.class_name)
        with open(f"listeClasses.csv", newline='', mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in class_liste:
                writer.writerow(ligne)
        
        return None