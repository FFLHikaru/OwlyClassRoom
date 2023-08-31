from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

class StudentButton(QPushButton):
    student_name=''
    color_hexa=''
    
    ####signal#### 
    button_click = pyqtSignal(QPushButton)
    
    
#### init ####
    def __init__( self, student_name : str, student_score : int ):
        
        self.student_name=student_name
        super().__init__()
        self.setStyleSheet( style_sheet( score_to_hexa_string( student_score ) ) )
        
        self.setText(student_name)
    ####signals connection####
        self.clicked.connect(self.on_button_click)

    #### Signales responses ####
    def on_button_click( self ) -> None:
        self.button_click.emit( self )
        return None

    #### Class Methods #### 
    def set_button_color( self , score : int ) -> None :
        color_hex : str = score_to_hexa_string( score )
        self.setStyleSheet(style_sheet( color_hex ))
    
        print(color_hex)
        return None
    






####Logic####
def score_to_hexa_string( score : int ) -> str :
    min_score = 0
    max_score = 20

    normalized_score = (score - min_score) / (max_score - min_score)

    red = int((1 - normalized_score) * 255)
    green = int(normalized_score * 255)
    blue = 0 

    color_hex = "#{:02X}{:02X}{:02X}".format(red, green, blue)

    return color_hex

def style_sheet( color_hex : str ) -> str:
    return ('QPushButton{' + f'''    
                    font:bold;
                    font-size:20px;
                    border-color:black;
                    border-width:2px;
                    border-style:solid;
                    border-radius: 20px;
                    padding : 20px;
                    background-color: {color_hex};           
            '''+'''}
            QPushButton:hover{
                background-color: red;
            }
            

            ''' )