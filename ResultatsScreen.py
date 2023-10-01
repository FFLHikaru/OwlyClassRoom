
from PyQt5.QtWidgets import QWidget

class ResultatsScreen(QWidget):
    def __init__(self):
        super().__init__()


    #### Class Methods ####

    def has_camera( self ) -> bool :
        return False   