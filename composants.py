from PyQt5.QtWidgets import  QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from PyQt5 import QtCore

class NeumorphicLabel(QLabel):
    
    def __init__(self):
        super().__init__()

        # Créer un effet de surbrillance
        highlight_effect = QGraphicsDropShadowEffect(self)
        highlight_effect.setBlurRadius(10)
        highlight_effect.setColor(QColor('#FFDD55'))
        highlight_effect.setOffset(0, 0)

        self.setGraphicsEffect(highlight_effect)

        # Appliquer un style de fond personnalisé
        self.setStyleSheet('''
            background-color: #2299FF;
            border-radius: 15px;
            border: 1px solid #0077CC;
            padding: 15px;
            color: white;
            font-size: 18px;
        ''')
        
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("Innovative Label")




