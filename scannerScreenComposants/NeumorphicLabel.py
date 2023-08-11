from PyQt5.QtWidgets import  QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from PyQt5 import QtCore

class NeumorphicLabel(QLabel):
    
    def __init__(self):
        super().__init__()

        # Appliquer un style de fond personnalisé
        self.setStyleSheet('''
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 10px;
            color: white;
            font-size: 18px;
            border-radius: 40px;               
        ''')
        
        
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("Innovative Label")




