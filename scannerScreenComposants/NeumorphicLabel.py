from PyQt5.QtWidgets import  QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


from scannerScreenComposants.textToPix import tex2svg

class NeumorphicLabel(QLabel):

    ####Signals#### 
    dimension_changed = pyqtSignal
    
    
    def __init__(self):

        super().__init__()

        self.image = tex2svg("A", self.width(),79)
        self.text = ' '

        #### Connect signals ####
        #self.dimension_changed.connect(self._resize)

        # Appliquer un style de fond personnalisé
        self.setStyleSheet('''
            text-align: left;
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 0px;
            color: black;
            font-size: 18px;
            border-radius: 40px;       
            border-color : black; 
            border-style : solid;
            border-width : 1px;   
                           
        ''')
        
        
        self.setAlignment(QtCore.Qt.AlignCenter)

    #### Class methods ####

    def setPixmap(self, formula : str) -> None:
        self.text = formula
        self.image=tex2svg(formula)
        self.rescale_after_resize()

        return super().setPixmap(self.image)

    def rescale_after_resize( self ) -> None :
        if self.image.width()>self.width()-30:
            self.image=self.image.scaledToWidth( self.width() -45 )

    def resizeEvent(self, event):
        self.setPixmap( self.text )
        self._on_resize()
        super().resizeEvent(event)

        return None
 
    
    def _on_resize( self ) -> None : 

        return None



