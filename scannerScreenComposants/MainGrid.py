
from PyQt5.QtWidgets import QLayout, QWidget,QGridLayout,QSizePolicy,QFrame,QPushButton

from scannerScreenComposants.QuizzScreen import QuizzScreen
from scannerScreenComposants.CameraScreen import CameraScreen
from scannerScreenComposants.ListesScreen import ListesScreen
from scannerScreenComposants.NeumorphicLabel import NeumorphicLabel
from scannerScreenComposants.GraphScreen import GraphScreen
from scannerScreenComposants.CustomLayout import CustomLayout
from PyQt5.QtSvg import QSvgRenderer
from scannerScreenComposants.RoundedButton import RoundedButton
from PyQt5.QtGui import QPixmap,QIcon

class MainGrid(QWidget):
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
        self.setStyleSheet('MainGrid{background-color:red}')
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.quizzScreen=QuizzScreen()
        self.cameraScreen=CameraScreen()
        self.listesScreen=ListesScreen(listeElevesResultats)
        
        self.afficher_reponses_eleves=RoundedButton()
        self.afficher_reponses_eleves.setIcon(QIcon(r"C:\Users\13ist\OneDrive\Bureau\python\23-diploma.svg"))

        self.graphiqueButton=RoundedButton()
        self.graphiqueButton.setIcon(QIcon(r"C:\Users\13ist\OneDrive\Bureau\python\48-abacus.svg"))
        




        self.layout=CustomLayout(self.geometry())
        self.setLayout(self.layout)

        self.layout.addWidget(self.quizzScreen,0,0,16,10)
        self.layout.addWidget(self.cameraScreen,11,10,5,6)
        self.layout.addWidget(self.listesScreen,0,10,11,6)
        self.layout.addWidget(self.graphiqueButton,11,14,2,2)
        self.layout.addWidget(self.afficher_reponses_eleves,13,14,2,2)

        self.layout.set_margin(10,10)

        #### Signals Connexion ####

        self.resizeEvent(self._on_resize())
        
    def setLayout(self, a0: CustomLayout) -> None:
        super().setLayout(a0)    
        a0.geometry_changed.emit( self.geometry() )
        return None
    
    def _on_resize( self ) -> None :
        self.layout.geometry_changed.emit( self.geometry() )
        return None

    def resizeEvent(self, event):
        self._on_resize()
        super().resizeEvent(event)

