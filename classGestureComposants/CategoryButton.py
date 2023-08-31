from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

class CategoryButton(QPushButton):
    category_name=''
    
    ####signal#### 
    button_click = pyqtSignal(QPushButton)
    
    
#### init ####
    def __init__( self, category_name : str, ):
        
        self.category_name = category_name
        super().__init__()
        self.setStyleSheet( style_sheet() )
        
        self.setText(category_name)
    ####signals connection####
        self.clicked.connect(self.on_button_click)

    #### Signales responses ####
    def on_button_click( self ) -> None:
        self.button_click.emit( self )
        return None

    

#### Logic ####
def style_sheet(): 
    return ('QPushButton{' + f'''    
                    font:bold;
                    font-size:20px;
                    border-color:black;
                    border-width:2px;
                    border-style:solid;
                    border-radius: 20px;
                    padding : 20px;
                    background-color: #FFB2B2;           
            '''+'''}
            QPushButton:hover{
                background-color: #E50000;
            }
            

            ''' )