from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import pyqtSignal
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
    

    def __init__(self, class_name):
        super().__init__()

        self.student_list_screen=StudentListScreen(class_name)
        self.categories_screen=CategoryScreen(class_name)
        self.punishment_screen=PunishmentScreen(class_name)
        
        self.addWidget(self.student_list_screen)
        self.addWidget(self.categories_screen)
        self.addWidget(self.punishment_screen)
        self.setCurrentWidget(self.student_list_screen)

        #### Signals Connexion #### 
        self.student_list_screen.student_name_set.connect(self.on_student_name_set)
        self.categories_screen.category_selected.connect(self._on_category_selected)
        self.punishment_screen.punishment_selected.connect(self._on_punishment_selected)

    ####Methode de classe

    #### Signals responses ####
    def on_student_name_set( self, name : str ) -> None : 
        self.student_name = name
        self.setCurrentWidget( self.categories_screen )
        return None

    def _on_category_selected( self , cat_name : str ) -> None : 
        self.category_name = cat_name
        self.setCurrentWidget( self.punishment_screen )
        self.punishment_screen.set_punishements_list(self.categories_screen.get_punishment_list( cat_name ))
        self.categories_screen.get_punishment_list( self.category_name )
        return None
    
    def _on_punishment_selected( self, punishment_name :str ) -> None : 
        print(punishment_name)
        return None
 ####Logic####