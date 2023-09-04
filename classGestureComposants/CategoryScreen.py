from PyQt5.QtWidgets import QWidget,QVBoxLayout,QGridLayout,QPushButton
import csv
from PyQt5.QtCore import pyqtSignal
from classGestureComposants.CategoryButton import CategoryButton



class CategoryScreen(QWidget):

    ####widgets####
    categories_button_list = []
    container = None
    main_layout = QVBoxLayout()
    hud_layout = QGridLayout()
    back_button = None

    ####Variables logiques####
    categories_list = []
    comportement_table = []
    
    ####Signals####
    category_selected = pyqtSignal( str )
    back_category_button_clicked = pyqtSignal()


    def __init__(self,class_name):
        with open(f"comportement{class_name}.csv", newline="") as fichier:
            lecteur = csv.reader(fichier, delimiter=";")
            for ligne in lecteur:
                self.comportement_table.append(ligne)
        
        for i in range(1, len (self.comportement_table) ):
            if self.comportement_table[i][0] != '':
                self.categories_list.append(self.comportement_table[i][0])

        super().__init__()


        self._set_categories_button_list()
        self._set_button_on_grid()
        self.container=QWidget()
        self.back_button=QPushButton('Go Back')
        self.container.setLayout(self.main_layout)
        self.hud_layout.addWidget(self.container,1,1,20,20)
        self.hud_layout.addWidget(self.back_button,1,1,1,1)
        self.setLayout(self.hud_layout)

        ####Signals connexion####
        for button in self.categories_button_list : 
            button.button_click.connect(self._on_category_button_click)

        self.back_button.clicked.connect(self._on_back_button_click)


    ####Signals Responses####
    def _on_category_button_click( self, button : CategoryButton ) -> None : 
        self.category_selected.emit( button.text() )
        return None
    
    def _on_back_button_click( self ) -> None : 
        self.back_category_button_clicked.emit()
        return None

    #### class methods #### 

    def _set_categories_button_list( self ) -> None : 
        for category in self.categories_list :
            self.categories_button_list.append( CategoryButton( category ) )
        return None
    
    def _set_button_on_grid( self ) -> None :
        for button in self.categories_button_list :
            self.main_layout.addWidget(button)

        return None
    
    def get_punishment_list( self, category_name : str ) -> list : 
        punishment_list = []
        starting_index = get_thing_row( transpose_table(self.comportement_table)[0], category_name )
        ending_index = find_next_non_empty_string( transpose_table(self.comportement_table)[0][starting_index+1:], starting_index )

        for i in range(ending_index-starting_index):
            punishment_list.append(self.comportement_table[starting_index+i][1])

        return punishment_list


#### Logic ####

def get_thing_row( table : list, thing : str ) -> int : 
    id = 0 
    for elt in table : 
        if elt == thing : 
            return id
        id += 1

    return id

def transpose_table ( table : list ) -> list : 
    transposed_table=[[]]
    for j in range( len( table[0] ) ):
        for i in range( len(table) ):
            transposed_table[j].append( table[i][j] )
        transposed_table.append([])
    return transposed_table

def find_next_non_empty_string(table : list, starting_index : int ) -> int :
    id = starting_index+1
    for elt in table : 
        if elt != '' :
            return id
        id += 1 
    return id