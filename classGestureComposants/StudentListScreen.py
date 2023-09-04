from PyQt5.QtWidgets import QWidget,QLabel,QGridLayout,QPushButton
import csv 
from PyQt5.QtCore import pyqtSignal
from classGestureComposants.StudentButton import StudentButton

class StudentListScreen(QWidget):
    ####Widgets####
    screen_title=None
    student_button_list=[]
    main_Layout=QGridLayout()

    ####Variable logic####
    class_name = '' 
    comportement_table=[]

    ####Signals####

    student_name_set=pyqtSignal(str)

#### init ####
    def __init__(self, class_name):
        self.class_name = class_name
        with open(f"comportement{class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                self.comportement_table.append(ligne)
            
        super().__init__()
        
        self.set_student_button_list()
        self.set_button_on_grid()
        self.setLayout(self.main_Layout)

    #### signals connection####
        for student_button in self.student_button_list:
            student_button.button_click.connect(self.on_student_button_click)
    
    ####Méthodes de classe####
    def get_student_score( self , student_name) -> int : 
        score = 10
        for i in range(1,len(self.comportement_table)):
            score += int(self.comportement_table[i][self.get_student_column( student_name )])
        return score
            
    
    def get_student_column( self , student_name : str ) -> int : 
        column = 0
        for name in self.comportement_table[0]:
            if name == student_name : 
                return column      
            column+=1
        return 0

    def set_button_on_grid( self ) -> None :
        for i in range (5):
            for j in range (7):
                if i*5+j<len(self.student_button_list):
                    self.main_Layout.addWidget(self.student_button_list[i*7+j],i,j)
        return None
        

    def set_student_button_list( self ) -> None :
        for student in self.comportement_table[0][2:]:
            self.student_button_list.append(StudentButton( student, self.get_student_score( student )))
        return None

    def refresh_colors( self ) -> None : 
        self.comportement_table = []
        with open(f"comportement{self.class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                self.comportement_table.append(ligne)
        for student_button in self.student_button_list : 
            student_score = self.get_student_score( student_button.text() )
            student_button.set_button_color( student_score )
        
    


     #### Signals responses####

    def on_student_button_click( self  , button : StudentButton) -> None :
        button.set_button_color( self.get_student_score( button.text() ) )
        self.student_name_set.emit( button.text() )
        return None
    
    



####Logic####

