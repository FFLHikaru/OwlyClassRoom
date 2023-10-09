from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton,QTextEdit
from scannerScreenComposants.CustomLayout import CustomLayout
from PyQt5.QtCore import pyqtSignal


class StudentButton( QPushButton ) :

    #### Signals #### 

    mouse_quit = pyqtSignal()
    mouse_enter = pyqtSignal()
    mouse_moved = pyqtSignal()
    name_text_changed = pyqtSignal()
    new_button_recquired = pyqtSignal()

    def __init__( self, student_name : str = '+' ) -> None :

        #### Logic Variables ####
        self.is_hovered = False

        #### Widget #### 

        self.grid_layout = CustomLayout()
        self.label = QTextEdit(student_name)
        self.delete_button = QPushButton('del')
         


        #### Init logic ####
        super().__init__()
        self.setLayout(self.grid_layout)
        self.grid_layout.addWidget(self.label,0,0,4,4)
        self.grid_layout.addWidget( self.delete_button, 3, 3, 1, 1)
        self.delete_button.hide()
        self.setMouseTracking(True)




        #### Signals connexion ####
        self.label.textChanged.connect( self._on_text_changed )


    #### Signals responses ####
    def _on_text_changed( self ) -> None :
        self.name_text_changed.emit()
        return None
    
    def enterEvent(self, a0 ) -> None:
        self.delete_button.show()
        return super().enterEvent(a0)
    
    #### Built in ####

    def resizeEvent( self, event ):
        self.grid_layout.geometry_changed.emit( self.geometry() )
        return super().resizeEvent(event)
    def enterEvent(self, a0 ) -> None:
        self.delete_button.show()
        return super().enterEvent(a0)
    def leaveEvent(self, a0 ) -> None:
        self.delete_button.hide()
        return super().enterEvent(a0)

    #### Private Class methods ####


    #### Public Class Methods #### 



####Logic Function #### 