from PyQt5.QtWidgets import QWidget,QVBoxLayout
import csv
from PyQt5.QtCore import pyqtSignal
from classGestureComposants.CategoryButton import CategoryButton


class PunishmentScreen(QWidget):

    ####widgets####
    punishments_button_list = []
    main_layout = QVBoxLayout()

    ####Variables logiques####
    punishments_list = []
    comportement_table = []
    punishment_number = 0

    ####Signals####
    punishment_selected = pyqtSignal( str )
    punishments_list_set = pyqtSignal()


    def __init__(self,class_name):

        super().__init__()
        
        self.setLayout(self.main_layout)

        ####Signals connexion####
        for button in self.punishments_button_list : 
            button.button_click.connect(self._on_punishment_button_click)
        self.punishments_list_set.connect(self._on_punishments_list_set)



    ####Signals Responses####
    def _on_punishment_button_click( self, button : CategoryButton ) -> None : 
        self.punishment_selected.emit( button.text() )
        return None
    
    def _on_punishments_list_set( self ) -> None : 
        self._set_punishments_button_list()
        self._set_button_on_grid()
        return None

    #### class methods #### 

    def _set_punishments_button_list( self ) -> None : 
        for punishment in self.punishments_list :
            self.punishments_button_list.append( CategoryButton( punishment ) )
        for button in self.punishments_button_list : 
            button.button_click.connect(self._on_punishment_button_click)
        return None
    
    def _set_button_on_grid( self ) -> None :
        for button in self.punishments_button_list :
            self.main_layout.addWidget(button)

        return None
    
    def set_punishements_list ( self, punishment_list : list ) -> None :
        self.punishments_list = punishment_list 
        self.punishments_list_set.emit()

        return None
    

#### Logic ####
