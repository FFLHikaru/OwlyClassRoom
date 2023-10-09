from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget,QComboBox, QPushButton
from scannerScreenComposants.CustomLayout import CustomLayout
from paramComposants.questionPreviewScreen import QuestionPreviewScreen
from paramComposants.multipleEditionScreen import MultipleEditionScreen
import csv

class QuestionParamScreen( QWidget ) : 
    #### Signals ####

    question_edited = pyqtSignal()

    def __init__( self, class_name ) -> None:

        #### variables logics ####
        self.question_text = ''
        self.response1_text = ''
        self.response2_text = ''
        self.response3_text = ''
        self.response4_text = ''

        self.questions_list = []

        self.class_name = class_name
        

        #### Widget ####
        self.combo_box = QComboBox()
        self.grid_layout = CustomLayout()
        self.preview_screen = QuestionPreviewScreen()
        self.text_edit_box = MultipleEditionScreen()

        self.add_question_button = QPushButton('+')
        self.del_question_button = QPushButton('x')

        super().__init__()
        self._load_questions()
        self._set_combo_box()
        self.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.combo_box,0,4,2,8)
        self.grid_layout.addWidget(self.text_edit_box,2,0,10,16)
        self.grid_layout.addWidget(self.preview_screen,12,0,16,16)       
        self.grid_layout.addWidget(self.add_question_button,0,12,1,1)
        self.grid_layout.addWidget(self.del_question_button,1,12,1,1)
        self.grid_layout.set_margin(10,10)

        self._on_item_selected(0)

        #### Signals connexion ####
        self.text_edit_box.edit_text_changed.connect(self._on_text_edited)
        self.combo_box.currentIndexChanged.connect(self._on_item_selected)
        self.add_question_button.clicked.connect(self._create_question)
        self.del_question_button.clicked.connect(self._delete_question)

    
    ####Signals responses ####
    def _on_item_selected( self, index) -> None : 
        self._set_edit_question_text( index )
        return None
    
    def _on_text_edited( self, index )-> None : 
        self._refresh_latex_shown( index )
        self._register_in_csv( index )
        print(index)
        if index == 0 :
            self.combo_box.setItemText(self.combo_box.currentIndex(),self.text_edit_box.text_edit_list[0].toPlainText())
        self.question_edited.emit()
        return None


    #### Builts-in ####

    def resizeEvent( self, event ):
        self.grid_layout.geometry_changed.emit( self.geometry() )
        return super().resizeEvent(event)
    
    #### Private methods ####

    def _refresh_latex_shown( self, index ) -> None : 
        self.preview_screen.preview_list[ index ].setPixmap(self.text_edit_box.text_edit_list[ index ].toPlainText(),16)
        return None

    def _set_combo_box( self ) -> None : 
        for question in self.questions_list[1:]:
            self.combo_box.addItem(question[0])

        return None

    def _register_in_csv( self, index ) -> None :
        self.questions_list[ self.combo_box.currentIndex()+1 ][ index ] = self.text_edit_box.text_edit_list[ index ].toPlainText()
        with open(f"listeQuestion{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in self.questions_list:
                writer.writerow(ligne)
        return None

    def _save_in_csv( self ) -> None : 
        with open(f"listeQuestion{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in self.questions_list:
                writer.writerow(ligne)
        return None
    def _set_edit_question_text( self, index : int ) -> None :
        self.text_edit_box.define_all_text_edit( self.questions_list[ index +1] )
        return None
    
    def _load_questions( self ) -> None : 
        with open(f"listeQuestion{self.class_name}.csv",newline="") as fichier : 
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur :
                self.questions_list.append(ligne)
        return None

    def _create_question( self ) -> None : 
        student_result_list=[]
        self.questions_list.append(["Enonce","Bonne reponse", "Mauvaise reponse", "Mauvaise reponse", "Mauvaise reponse",'0.2'])
        self.combo_box.addItem("new question")
        self._save_in_csv()

        with open(f"listeEleves{self.class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                student_result_list.append(ligne)
        for line in student_result_list[1:] :
            line.append('[0, 0]')
        with open(f"listeEleves{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in student_result_list:
                writer.writerow(ligne)
        self.question_edited.emit()
        return None
    
    def _delete_question( self ) -> None : 
        student_result_list = []
        self.questions_list.pop( self.combo_box.currentIndex()+1 )
        self._save_in_csv()

        with open(f"listeEleves{self.class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                student_result_list.append(ligne)
        for line in student_result_list[1:] :
            line.pop( self.combo_box.currentIndex()+1 )

        with open(f"listeEleves{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in student_result_list:
                writer.writerow(ligne)

        self.combo_box.removeItem( self.combo_box.currentIndex() )
        self._set_edit_question_text( self.combo_box.currentIndex() )
        self.question_edited.emit()

        return None
    

    #### Public methods #####