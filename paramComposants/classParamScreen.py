from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton
from paramComposants.studentButton import StudentButton
from scannerScreenComposants.CustomLayout import CustomLayout

class ClassParamScreen( QWidget ) : 

    #### Signals ####



    def __init__( self, students_list, class_name ) -> None:

        #### Logical variables ####

        self.students_list = students_list
        self.class_name = class_name

        #### Widget ####

        self.grid_layout = CustomLayout()
        self.button_list = []

        #### Init Logic ####
        super().__init__()
        self.setMouseTracking(True)
        self.setLayout(self.grid_layout)
        self._create_all_button()
        self._set_buttons_on_grid_layout()
        self.grid_layout.set_margin(10,10)

        #### Signals connexion ####
        self.button_list[-1].clicked.connect( self._create_new_button )
        

    #### Signals responses ####

    #### Built In ####
    def resizeEvent( self, event ):
        self.grid_layout.geometry_changed.emit( self.geometry() )
        return super().resizeEvent(event)

    def mouseMoveEvent( self, e ) -> None : 
        for button in self.button_list[0:30] : 
            button.mouse_moved.emit()
        return None
    
    #### Private class methods ####
    def _create_all_button( self ) -> None : 
        print(self.students_list)
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
    
    def _create_new_button( self ) -> None : 
        self.grid_layout.moveWidget( self.button_list[-1] , 8, 5,2,1)
    


    #### Public Class methods ####

    
            

#### Logical functions ####

        

       