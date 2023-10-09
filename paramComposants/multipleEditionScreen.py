import typing
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget,QTextEdit
from scannerScreenComposants.CustomLayout import CustomLayout

class MultipleEditionScreen( QWidget ) : 
    #### Signals ####
    edit_text_changed = pyqtSignal( int )

    def __init__( self ) -> None:
        #### variables logics ####
        #### Widget #####
        self.grid_layout = CustomLayout()
        self.text_edit_list = [QTextEdit(),QTextEdit(),QTextEdit(),QTextEdit(),QTextEdit()]

        super().__init__()
        self.setLayout(self.grid_layout)
        self._set_text_edit_on_grid()
        self.grid_layout.set_margin(10,10)

        for i in range( len( self.text_edit_list ) ):
            self.text_edit_list[i].textChanged.connect(lambda index=i: self._on_edit_changed(index))


        #### Signals connexion #### 
        

    #### Signals responses ####
    
    def _on_edit_changed( self, index ) -> None : 
        self.edit_text_changed.emit(index)
        return None



    #### Built-int ####

    def resizeEvent( self, event ):
        self.grid_layout.geometry_changed.emit( self.geometry() )
        return super().resizeEvent(event)
    

    #### Private class methods ####
    def _set_text_edit_on_grid( self ) -> None : 
        i=0
        for edit in self.text_edit_list : 
            self.grid_layout.addWidget(edit,i,0,1,1)
            i+=1
        return None
    

    #### Public class methods ####

    def define_all_text_edit( self, question : list ) -> None : 
        i=0
        for edit in self.text_edit_list : 
            edit.setText( question[i] )
            i+=1
        return None

#### logic function ####

