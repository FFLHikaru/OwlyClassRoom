from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton
from paramComposants.studentButton import StudentButton
from scannerScreenComposants.CustomLayout import CustomLayout
import csv

class ClassParamScreen( QWidget ) : 

    #### Signals ####

    student_list_edited = pyqtSignal()


    def __init__( self, students_list, class_name ) -> None:

        #### Logical variables ####

        self.students_list = students_list
        self.class_name = class_name


        #### Widget ####

        self.grid_layout = CustomLayout()
        self.button_list = []
        self.widget = QWidget()

        #### Init Logic ####
        super().__init__()
        self.setMouseTracking(True)
        self.setLayout(self.grid_layout)
        self._create_all_button()
        self._set_buttons_on_grid_layout()
        self._connect_all_buttons()
        self.grid_layout.set_margin(10,10)
        if len(self.button_list) < 30 : 
            self.grid_layout.addWidget(self.widget,4,6,1,1)

        #### Signals connexion ####
        self.button_list[-1].clicked.connect( self._create_new_button )
        for i in range(len(self.button_list) - 1): 
            self.button_list[i].delete_button.clicked.connect(lambda _, index=i: self._delete_student(index))



    #### Signals responses ####

    #### Built In ####
    def resizeEvent( self, event ):
        self.grid_layout.geometry_changed.emit( self.geometry() )
        return super().resizeEvent(event)

    
    #### Private class methods ####
    def _create_all_button( self ) -> None : 
        self.button_list=[]
        for student in self.students_list : 
            self.button_list.append( StudentButton( student ) )
        self.button_list.append( QPushButton('add student') )
        
        return None
    
    def _set_buttons_on_grid_layout( self ) -> None : 
        i=0
        for button in self.button_list:
            self.grid_layout.addWidget( button,i//7,i%7,1,1 )
            i+=1
        return None
    
    def _connect_all_buttons( self )-> None : 
        for button in self.button_list[:-1]:
            button.name_text_changed.connect(self._update_students_list)
        return None
    
    def _create_new_button( self ) -> None : 
        self.students_list.append('Student')
        self._add_csv_student()

        self.grid_layout.delete_all()
        self._create_all_button()
        self._set_buttons_on_grid_layout()

        self._connect_all_buttons()
        for i in range(len(self.button_list) - 1): 
                self.button_list[i].delete_button.clicked.connect(lambda _, index=i: self._delete_student(index))
        self.button_list[-1].clicked.connect( self._create_new_button )
        self.__update_csv_file_value()
        comportement_table=[]

        with open(f"comportement{self.class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                comportement_table.append(ligne)
        for i in range( len( comportement_table[0][2:] ) ):
            comportement_table[0][i+2]=self.button_list[i].label.toPlainText()
        
        with open(f"comportement{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in comportement_table:
                writer.writerow(ligne)
        self.student_list_edited.emit()
        
        
    def _update_students_list( self ) -> None : 
        self.students_list = []
        for button in self.button_list[:-1] :
            self.students_list.append(button.label.toPlainText()) 
        

        comportement_table=[]

        with open(f"comportement{self.class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                comportement_table.append(ligne)
        for i in range( len( comportement_table[0][2:] ) ):
            comportement_table[0][i+2]=self.students_list[i]
        
        with open(f"comportement{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in comportement_table:
                writer.writerow(ligne)


        self.__update_csv_file_value()
        self.student_list_edited.emit()
        return None

    def __update_csv_file_value( self ) -> None : 
        listeElevesResultats=[]
        with open(f"listeEleves{self.class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                listeElevesResultats.append(ligne)
            i=1
        for name in self.students_list : 
            listeElevesResultats[i][0] = name
            for case in listeElevesResultats[i]:
                case = "[0, 0]"
            i+=1
        while i < len(listeElevesResultats) : 
            listeElevesResultats.pop(i)
            i+=1

        with open(f"listeEleves{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in listeElevesResultats:
                writer.writerow(ligne)
        return None

    def _add_csv_student( self ) -> None :
        listeElevesResultats=[]
        with open(f"listeEleves{self.class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                listeElevesResultats.append(ligne)
            i=1
        listeElevesResultats.append([self.students_list[-1]])
        for i in range(len(listeElevesResultats[1])-1):
            listeElevesResultats[-1].append('[0, 0]')
        with open(f"listeEleves{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in listeElevesResultats:
                writer.writerow(ligne)


        comportement_table = []
        with open(f"comportement{self.class_name}.csv", newline='') as fichier : 
            lecteur = csv.reader(fichier, delimiter=";")
            for line in lecteur : 
                comportement_table.append(line)
        comportement_table[0].append('eleve')
        for line in comportement_table[1:] : 
            line.append('0')
        i=0
        for case in comportement_table[0][2:] : 
            case = self.students_list[i]
            i+=1
        with open(f"comportement{self.class_name}.csv", newline="", mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in comportement_table:
                writer.writerow(ligne)

        return None
    
    def _delete_student( self ,index : int ) -> None :
        if len(self.button_list) > 2 : 
            self.grid_layout.delete_all()
            self.students_list.pop( index )

            self._create_all_button()
            self._connect_all_buttons()
            self._set_buttons_on_grid_layout()

            comportement_table=[]

            with open(f"comportement{self.class_name}.csv", newline="") as fichier:
                lecteur = csv.reader(fichier, delimiter=";")
                for ligne in lecteur:
                    comportement_table.append(ligne)

            for line in comportement_table : 
                line.pop(index +2 )
            
            with open(f"comportement{self.class_name}.csv", newline="", mode='w') as fichier:
                writer = csv.writer(fichier,delimiter=";")
                for ligne in comportement_table:
                    writer.writerow(ligne)
            
            
            for i in range(len(self.button_list) - 1): 
                self.button_list[i].delete_button.clicked.connect(lambda _, index=i: self._delete_student(index))
            self.button_list[-1].clicked.connect( self._create_new_button )
            
            self.__update_csv_file_value()
            self.student_list_edited.emit()
            
        return None


    #### Public Class methods ####

    
            

#### Logical functions ####

        

       