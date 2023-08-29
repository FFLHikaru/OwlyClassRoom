
from PyQt5.QtWidgets import QWidget,QGridLayout,QSizePolicy,QFrame,QPushButton
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap,QIcon
from scannerScreenComposants.QuizzScreen import QuizzScreen
from scannerScreenComposants.CameraScreen import CameraScreen
from scannerScreenComposants.ListesScreen import ListesScreen
from scannerScreenComposants.NeumorphicLabel import NeumorphicLabel
from scannerScreenComposants.GraphScreen import GraphScreen
from PyQt5.QtSvg import QSvgRenderer

class MainGrid(QFrame):
    afficher_reponses_eleves=None
    quizzScreen=None
    cameraScreen=None
    vertBar=None
    layout=None
    listesScreen=None
    graphiqueButton=None
    graphScreen=None
    visibleGraph=False
    reponses=[0,0,0,0]


    

    def __init__(self,listeElevesResultats):
        
        super().__init__()
        self.setStyleSheet('MainGrid{background-color:#F8F8FE}')
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.quizzScreen=QuizzScreen()
        self.cameraScreen=CameraScreen()
        self.listesScreen=ListesScreen(listeElevesResultats)
        
        self.afficher_reponses_eleves=QPushButton()
        self.afficher_reponses_eleves.setFixedSize(QSize(100,100))
        self.afficher_reponses_eleves.setIcon(QIcon(r"C:\Users\13ist\OneDrive\Bureau\python\23-diploma.svg"))
        self.afficher_reponses_eleves.setIconSize(QSize(80,80))

        self.graphiqueButton=QPushButton()
        self.graphiqueButton.setFixedSize(QSize(100,100))
        self.graphiqueButton.setIcon(QIcon(r"C:\Users\13ist\OneDrive\Bureau\python\48-abacus.svg"))
        self.graphiqueButton.setIconSize(QSize(80,80))
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
        




        self.layout=QGridLayout()
        self.layout.addWidget(self.quizzScreen,0,0,16,10)
        self.layout.addWidget(self.cameraScreen,13,10,3,6,Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.listesScreen,0,10,13,6)
        self.layout.addWidget(self.graphiqueButton,15,15,1,1)
        self.layout.addWidget(self.afficher_reponses_eleves,14,15,1,1)
        
        for i in range (16):
            self.layout.setRowStretch(i,1)
            self.layout.setColumnStretch(i,1)

        self.setLayout(self.layout)
