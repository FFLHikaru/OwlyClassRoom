
from PyQt5.QtWidgets import QWidget,QGridLayout,QSizePolicy,QFrame
from PyQt5.QtCore import Qt
from scannerScreenComposants.QuizzScreen import QuizzScreen
from scannerScreenComposants.CameraScreen import CameraScreen
from scannerScreenComposants.ListesScreen import ListesScreen

class MainGrid(QFrame):
    quizzScreen=None
    cameraScreen=None
    vertBar=None
    elevesScanned=None
    layout=None
    listesScreen=None
    def __init__(self,listeElevesResultats):
        
        super().__init__()
        self.setStyleSheet('MainGrid{background-color:green}')
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.quizzScreen=QuizzScreen()
        self.cameraScreen=CameraScreen()
        self.listesScreen=ListesScreen(listeElevesResultats)
        layout=QGridLayout()
        layout.addWidget(self.quizzScreen,0,0,16,10)
        layout.addWidget(self.cameraScreen,10,10,6,6,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.listesScreen,0,10,10,6)
        for i in range (16):
            layout.setRowStretch(i,1)
            layout.setColumnStretch(i,1)

        self.setLayout(layout)
