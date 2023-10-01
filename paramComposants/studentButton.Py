from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton,QTextEdit
from scannerScreenComposants.CustomLayout import CustomLayout
from PyQt5.QtCore import pyqtSignal


class StudentButton( QPushButton ) :

    #### Signals #### 

    mouse_quit = pyqtSignal()
    mouse_enter = pyqtSignal()
    mouse_moved = pyqtSignal()
    name_text_changed = pyqtSignal( str )
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
        self.setMouseTracking(True)

        if student_name == '+':
            self.label.setReadOnly( True )
            self.clicked.connect( self._on_click )



        #### Signals connexion ####
        self.mouse_quit.connect( self._on_mouse_quit )
        self.mouse_enter.connect( self._on_mouse_enter )
        self.mouse_moved.connect( self._on_mouse_moved )
        self.label.textChanged.connect( self._on_text_changed )


    #### Signals responses ####
    def _on_text_changed( self ) -> None :
        self.name_text_changed.emit( self.label.toPlainText() )
        return None

    def _on_mouse_quit( self ) -> None :
        print("quit")
        self.is_hovered = False
        self._hide_sub_button()
        return None
    
    def _on_mouse_enter( self ) -> None :
        print('enter')
        self.is_hovered = True
        self._show_sub_button()
        return None

    def _on_mouse_moved( self ) -> None:
        if self.is_hovered : 
            if not self.underMouse():
                self.mouse_quit.emit()
        else : 
            if self.underMouse():    
                self.mouse_enter.emit()
        return None
    
    def _on_click( self ) -> None : 
        self.new_button_recquired.emit()
        return None
    
    #### Built in ####

    def resizeEvent( self, event ):
        self.grid_layout.geometry_changed.emit( self.geometry() )
        return super().resizeEvent(event)
    
    def mouseMoveEvent( self, e ) -> None:
        self.mouse_moved.emit()
        return super().mouseMoveEvent(e)

    #### Private Class methods ####

    def _hide_sub_button( self ) -> None :
        self.delete_button.deleteLater()
        self.grid_layout.deleteWidget( self.delete_button )
        return None

    def _show_sub_button( self ) -> None :
        self.delete_button = QPushButton('del')
        self.grid_layout.addWidget( self.delete_button, 3, 3, 1, 1)
        return None


    #### Public Class Methods #### 



####Logic Function #### 