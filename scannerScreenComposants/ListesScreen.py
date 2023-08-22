from PyQt5.QtWidgets import QWidget,QGridLayout,QSizePolicy,QFrame,QListView,QHBoxLayout
from PyQt5.QtCore import QStringListModel,QItemSelectionModel,Qt
from scannerScreenComposants.QuizzScreen import QuizzScreen
from scannerScreenComposants.CameraScreen import CameraScreen

class ListesScreen(QFrame):
    listeGauche=None
    listeDroite=None

    listeModelGauche=None
    listeModelDroite=None

    selectionModelGauche=None
    selectionModelDroite=None

    listePrenomGauche=None
    listePrenomDroite=None
    
    def __init__(self,listeElevesResultats):
        super().__init__()
        self.setStyleSheet('''
                           background-color:#F8F8FE;
                           border-width:0px;
                           border-color:white;
                           font-size:16px;

                           QListView.item.selected{
                            background-color:green;

                           }

                           ''')
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

    def set_response_to_eleve(self, id : int , response : str ) -> None :
        if id>len(self.listePrenomGauche):
            index=self.listeModelDroite.index(id-len(self.listePrenomGauche)-1,0)
            if self.listeModelDroite.data( index , Qt.DisplayRole ).endswith((" A"," B"," C"," D")):
                self.listeModelDroite.setData( index , self.listeModelDroite.data( index , Qt.DisplayRole )[:-2] + response )
            else:
                self.listeModelDroite.setData( index , self.listeModelDroite.data( index , Qt.DisplayRole ) + response )
        else:
            index = self.listModelGauche.index(id-1, 0)
            if self.listModelGauche.data( index , Qt.DisplayRole ).endswith((" A"," B"," C"," D")):
                self.listModelGauche.setData( index , self.listModelGauche.data( index , Qt.DisplayRole )[:-2] + response )
            else:
                self.listModelGauche.setData( index , self.listModelGauche.data( index , Qt.DisplayRole ) + response )


    def set_all_scanned_responses( self, responses_list : list ) -> None :
        longueur_liste_gauche=len( self.listModelGauche.stringList() ) 
        longueur_liste_droite = len( self.listeModelDroite.stringList() )
        longueur_totale = longueur_liste_droite + longueur_liste_gauche
        for j in range( 1, longueur_totale ) : 
            self.set_response_to_eleve( j , seek_scanned_responses(responses_list, j))
        

    def delete_response(self, id : int ) -> None :
        
        if id>len(self.listePrenomGauche):
            index=self.listeModelDroite.index(id-len(self.listePrenomGauche)-1,0)
            response_and_name=self.listeModelDroite.data( index , Qt.DisplayRole )
            if response_and_name.endswith((" A"," B"," C", " D")):
                self.listeModelDroite.setData( index , response_and_name[:-2])
        else:
            index = self.listModelGauche.index(id-1, 0)
            response_and_name=self.listModelGauche.data( index , Qt.DisplayRole )
            if response_and_name.endswith((" A"," B"," C", " D")):
                self.listModelGauche.setData( index , response_and_name[:-2])
            

    def delete_all_responses(self) -> None : 
        longueur_liste_gauche=len( self.listModelGauche.stringList() ) 
        longueur_liste_droite = len( self.listeModelDroite.stringList() )
        longueur_totale = longueur_liste_droite + longueur_liste_gauche
        for j in range( 1, longueur_totale ) : 
            self.delete_response( j )


def seek_scanned_responses( responses_list : list , id : int ) -> str:
    for response in responses_list : 
        if response[1] == id :
            return " "+response[0]
    return " "

