from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import pyqtSignal
import csv
from classGestureComposants.CategoryScreen import CategoryScreen
from classGestureComposants.StudentListScreen import StudentListScreen
from classGestureComposants.PunishmentScreen import PunishmentScreen

class ClassGestureScreen(QStackedWidget):

    ####Widgets####
    student_list_screen=None
    categories_screen=None
    punishment_screen=None

    ####Variables logique####
    student_name=''
    category_name=''
    punishment_name=''
    class_name = ''
    
    comportement_table = []

    def __init__(self, class_name):

        with open(f"comportement{class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                self.comportement_table.append(ligne)

        self.class_name = class_name
        super().__init__()

        

        self.student_list_screen=StudentListScreen(class_name)
        self.categories_screen=CategoryScreen(class_name)
        self.punishment_screen=PunishmentScreen(class_name)
        
        self.addWidget(self.student_list_screen)
        self.addWidget(self.categories_screen)
        self.addWidget(self.punishment_screen)
        self.setCurrentWidget(self.student_list_screen)

        #### Signals Connexion #### 
        self.student_list_screen.student_name_set.connect( self.on_student_name_set )
        self.categories_screen.category_selected.connect( self._on_category_selected )
        self.categories_screen.back_category_button_clicked.connect( self._on_student_canceled )
        self.punishment_screen.punishment_selected.connect(self._on_punishment_selected)
        self.punishment_screen.back_button_clicked.connect( self._on_category_canceled )
        

    ####Methode de classe
    def get_punishment_value( self, punishment_name : str ) -> int:

        if punishment_name[-3]==' ':
            return int(punishment_name[-2:])
        else : 
            return int(punishment_name[-3:])
        return 0


    def save_punition( self ) -> None :
        punishment_index = 0 
        student_index = 0 

        punishment_index =  get_thing_index( transpose_table( self.comportement_table )[1], self.punishment_name ) 
        student_index = get_thing_index( self.comportement_table[0], self.student_name )
        print(punishment_index)
        print(student_index)

        punishment_value = self.get_punishment_value(self.comportement_table[punishment_index][1])

        current_punishment_score = int(self.comportement_table[punishment_index][student_index])
        current_new_punishment_score = current_punishment_score + punishment_value

        self.comportement_table[punishment_index][student_index] = str(current_new_punishment_score) 

        with open(f"comportement{self.class_name}.csv", newline="",mode='w') as fichier:
            writer = csv.writer(fichier,delimiter=";")
            for ligne in self.comportement_table:
                writer.writerow(ligne)

    #### Signals responses ####
    def on_student_name_set( self, name : str ) -> None : 
        self.student_name = name
        self.setCurrentWidget( self.categories_screen )
        return None

    def _on_category_selected( self , cat_name : str ) -> None : 
        self.category_name = cat_name
        self.setCurrentWidget( self.punishment_screen )
        self.punishment_screen.set_punishements_list(self.categories_screen.get_punishment_list( cat_name ))
        return None
    
    def _on_punishment_selected( self, punishment_name :str ) -> None : 
        self.punishment_name = punishment_name 
        self.save_punition()
        self.setCurrentWidget(self.student_list_screen)
        self.student_list_screen.refresh_colors()
        return None
    
    def _on_student_canceled( self ) -> None : 
        self.student_name = ''
        self.category_name = ''
        self.setCurrentWidget( self.student_list_screen )
        return None

    def _on_category_canceled( self ) -> None : 
        self.category_name = ''
        self.setCurrentWidget( self.categories_screen )
        return None
    

    



 ####Logic####

def get_thing_index( table : list, thing : str ) -> int : 
    id = 0 
    for elt in table : 
        if elt == thing : 
            return id
        id += 1

    return id


def transpose_table ( table : list ) -> list : 
    transposed_table=[[]]
    for j in range( len( table[0] ) ):
        for i in range( len(table) ):
            transposed_table[j].append( table[i][j] )
        transposed_table.append([])
    return transposed_table