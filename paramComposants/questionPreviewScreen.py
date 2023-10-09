import typing
from PyQt5.QtCore import pyqtSignal
from scannerScreenComposants.NeumorphicLabel import NeumorphicLabel
from scannerScreenComposants.CustomLayout import CustomLayout
from PyQt5.QtWidgets import QWidget



class QuestionPreviewScreen( QWidget ):
    def __init__( self ) -> None:
        #### variables logiques ####
        

        #### Widget ####
        self.preview_list = [NeumorphicLabel(),NeumorphicLabel(),NeumorphicLabel(),NeumorphicLabel(),NeumorphicLabel()]

        self.grid_layout = CustomLayout()

        super().__init__()
        self.grid_layout.set_margin(20,20)
        self.setLayout(self.grid_layout)

        self.grid_layout.addWidget(self.preview_list[0],0,0,10,4)
        self.grid_layout.addWidget(self.preview_list[1],10,0,3,2)
        self.grid_layout.addWidget(self.preview_list[2],13,0,3,2)
        self.grid_layout.addWidget(self.preview_list[3],10,2,3,2)
        self.grid_layout.addWidget(self.preview_list[4],13,2,3,2)
    
    ####Signals responses ####

    #### Builts-in ####
    def resizeEvent( self, event ):
        self.grid_layout.geometry_changed.emit( self.geometry() )
        return super().resizeEvent(event)
    #### Private methods ####

    #### Public methods #####