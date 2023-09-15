from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt,QSize,QRect
from PyQt5.QtGui import QPixmap,QIcon

class RoundedButton( QPushButton ) : 

    def __init__( self ):
        super().__init__()

        self.setIconSize(QSize(80,80))
        self.setStyleSheet('''
                                           QPushButton{
                                           background-color:rgba(88,93,96,0.5);
                                           border-width:2px;
                                           border-color:black;
                                           border-style:solid;
                                           border-radius:50px;
                                           opacity:0.3;
                                           }

                                           QPushButton:Hover{
                                           background-color:#D4E2EF;
                                           }
                           ''')
    
    def resizeEvent(self, event) -> None:

        self.setGeometry( QRect( self.geometry().x()+(self.geometry().width()-self.geometry().height())//2, self.geometry().y(), self.geometry().height(), self.geometry().height() ))

        self.setIconSize(QSize(self.width()-20,self.height()-20))

        return super().resizeEvent(event)