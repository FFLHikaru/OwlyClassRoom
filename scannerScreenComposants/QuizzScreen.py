from PyQt5.QtWidgets import QWidget,QGridLayout
from scannerScreenComposants.NeumorphicLabel import NeumorphicLabel
from PyQt5.QtGui import QImage, QPixmap
from scannerScreenComposants.textToPix import tex2svg

class QuizzScreen(QWidget):
    
    questionShowed=None
    reponse1Showed=None
    reponse2Showed=None
    reponse3Showed=None
    reponse4Showed=None

    def setQuestion(self,question):
        self.questionShowed.setPixmap(tex2svg('Enonce : '+question[0],self.questionShowed.width()-30))
        self.reponse1Showed.setPixmap(tex2svg("A : "+question[1],self.reponse1Showed.width()-30))
        self.reponse2Showed.setPixmap(tex2svg("B : "+question[2],self.reponse2Showed.width()-30))
        self.reponse3Showed.setPixmap(tex2svg("C : "+question[3],self.reponse3Showed.width()-30))
        self.reponse4Showed.setPixmap(tex2svg("D : "+question[4],self.reponse4Showed.width()-30))

    def __init__(self):
        print('questionScreen')
        super().__init__()
        
        self.setStyleSheet('QWidget{border: 3px solid black;}')
        layout=QGridLayout()
        self.questionShowed=NeumorphicLabel()
        self.reponse1Showed=NeumorphicLabel()
        self.reponse2Showed=NeumorphicLabel()
        self.reponse3Showed=NeumorphicLabel()
        self.reponse4Showed=NeumorphicLabel()

        layout.addWidget(self.questionShowed,0,0,10,4)
        layout.addWidget(self.reponse1Showed,10,0,3,2)
        layout.addWidget(self.reponse2Showed,13,0,3,2)
        layout.addWidget(self.reponse3Showed,10,2,3,2)
        layout.addWidget(self.reponse4Showed,13,2,3,2)

        self.setLayout(layout)
