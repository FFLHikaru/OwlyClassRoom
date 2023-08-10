from PyQt5.QtWidgets import QWidget,QGridLayout,QSizePolicy,QFrame,QListView,QHBoxLayout
from PyQt5.QtCore import QStringListModel,QItemSelectionModel
from scannerScreenComposants.QuizzScreen import QuizzScreen
from scannerScreenComposants.CameraScreen import CameraScreen

class ListesScreen(QFrame):
    listeGauche=None
    listeDroite=None

    listeModelGauche=None
    listeModelDroite=None

    selectionModelGauche=None
    selectionModelDroite=None

    def __init__(self,listeElevesResultats):
        print(listeElevesResultats)
        super().__init__()
        layout=QHBoxLayout()
        self.listeGauche=QListView()
        self.listeGauche.setEditTriggers(QListView.NoEditTriggers)
        self.listeGauche.setSelectionMode(QListView.NoSelection)
        self.listeDroite=QListView()
        self.listeDroite.setEditTriggers(QListView.NoEditTriggers)
        self.listeDroite.setSelectionMode(QListView.NoSelection)

        self.listePrenomGauche=[ligne[0] for ligne in listeElevesResultats[1:(len(listeElevesResultats)-1)//2+1]]
        self.listModelGauche=QStringListModel()
        self.listModelGauche.setStringList(self.listePrenomGauche)
        self.listeGauche.setModel(self.listModelGauche)

        listePrenomDroite=[ligne[0] for ligne in listeElevesResultats[(len(listeElevesResultats)-1)//2+1:]]
        self.listeModelDroite=QStringListModel()
        self.listeModelDroite.setStringList(listePrenomDroite)
        self.listeDroite.setModel(self.listeModelDroite)

        self.selectionModelGauche = QItemSelectionModel(self.listModelGauche)
        self.selectionModelDroite = QItemSelectionModel(self.listeModelDroite)

        self.listeDroite.setSelectionModel(self.selectionModelDroite)
        self.listeGauche.setSelectionModel(self.selectionModelGauche)

        layout.addWidget(self.listeGauche)
        layout.addWidget(self.listeDroite)
        self.setLayout(layout)
        
    
    