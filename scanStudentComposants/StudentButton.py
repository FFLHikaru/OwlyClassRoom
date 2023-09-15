from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

class StudentButton(QPushButton):
    
#### init ####
    def __init__( self, student_name : str ):
        
        self.student_name=student_name

        super().__init__()

        self.setStyleSheet( style_sheet( "white" ) ) 
        self.setText(student_name)
        
        ####signals connection####

    
    
    #### Signals responses ####


    #### Class Methods #### 
 






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