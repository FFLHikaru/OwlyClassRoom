from PyQt5.QtWidgets import QWidget,QGridLayout,QLabel
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from scannerScreenComposants.NeumorphicLabel import NeumorphicLabel
from scannerScreenComposants.CustomLayout import CustomLayout
from PyQt5.QtGui import QImage, QPixmap
from scannerScreenComposants.textToPix import tex2svg


class QuizzScreen(QWidget):
    
    questionShowed=None
    reponse1Showed=None
    reponse2Showed=None
    reponse3Showed=None
    reponse4Showed=None

    score_text_label = None

    layout = None

    def __init__(self):
        super().__init__()
        
        self.setStyleSheet('QWidget{border: 3px solid black;}')
        self.layout=CustomLayout(self.geometry())
        self.layout.set_margin(20,20)
        self.setLayout(self.layout)
        
        self.questionShowed=NeumorphicLabel()
        self.reponse1Showed=NeumorphicLabel()
        self.reponse2Showed=NeumorphicLabel()
        self.reponse3Showed=NeumorphicLabel()
        self.reponse4Showed=NeumorphicLabel()

        self.score_text_label=QLabel("Score : ")
        self.score_text_label.setStyleSheet("font-size: 18px; text-align: center")
        self.score_text_label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.questionShowed,0,0,10,4)
        self.layout.addWidget(self.reponse1Showed,10,0,3,2)
        self.layout.addWidget(self.reponse2Showed,13,0,3,2)
        self.layout.addWidget(self.reponse3Showed,10,2,3,2)
        self.layout.addWidget(self.reponse4Showed,13,2,3,2)
        self.layout.addWidget(self.score_text_label,9,1,1,2)

        

    def _on_resize( self ) -> None :
        self.layout.geometry_changed.emit( self.geometry() )
        self.questionShowed.rescale_after_resize()
        self.reponse1Showed.rescale_after_resize()
        self.reponse2Showed.rescale_after_resize()
        self.reponse3Showed.rescale_after_resize()
        self.reponse4Showed.rescale_after_resize()
        return None

    def resizeEvent(self, event):
        self._on_resize()
        super().resizeEvent(event)

    def set_score_label_text( self, text : str = "score : 0") -> None : 
        self.score_text_label.setText( text )
        return None 
    
    def setQuestion(self,question):
        self.questionShowed.setPixmap('Enonce : '+question[0])
        self.reponse1Showed.setPixmap("A : "+question[1])
        self.reponse2Showed.setPixmap("B : "+question[2])
        self.reponse3Showed.setPixmap("C : "+question[3])
        self.reponse4Showed.setPixmap("D : "+question[4])