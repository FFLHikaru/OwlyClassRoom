from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget

class QuestionParamScreen( QWidget ) : 

    def __init__( self, students_list ) -> None:
        super().__init__()