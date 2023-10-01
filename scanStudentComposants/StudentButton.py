from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


class StudentButton(QPushButton):

    #### Signals ####
    selection_changed = pyqtSignal()
    
#### init ####
    def __init__( self, student_name : str ):
        
        
        #### Widget ####
        self.student_name=student_name
        
        #### logic variables ####
        self.is_selected = False

        super().__init__()

        self.setStyleSheet( style_sheet( "white" ) ) 
        self.setText(student_name)
        
        ####signals connection####

        self.clicked.connect(self._on_click)
        self.selection_changed.connect(self._on_is_selected_changed)
    
    #### Signals responses ####
    def _on_click( self ) -> None : 
        self.is_selected = not self.is_selected
        self.selection_changed.emit()
        return None
    
    def _on_is_selected_changed( self ) -> None:
        self._change_color()
        return None

    #### Private Class Methods #### 
    def _change_color( self ) -> None : 
        if self.is_selected : 
            self.setStyleSheet( style_sheet( "orange" ) )
            return None
        self.setStyleSheet( style_sheet( "white" ) )
        return None

 
    #### Public Class Metods ####
    def marker_detected( self ) -> None : 
        self.setStyleSheet( style_sheet("orange") )
        if self.is_selected :
            return None
        else :
            self.is_selected = True
            self.selection_changed.emit()
        return None
    
    def reset_button( self ) -> None : 
        self.is_selected = False
        self.selection_changed.emit()
        return None





####Logic####

def style_sheet( color_hex : str ) -> str:
    return ('QPushButton{' + f'''    
                    font:bold;
                    font-size:20px;
                    border-color:black;
                    border-width:2px;
                    border-style:solid;
                    border-radius: 20px;
                    padding : 20px;
                    color: black;
                    background-color: {color_hex};           
            '''+'''}
            QPushButton:hover{
                background-color: red;
            }
            

            ''' )