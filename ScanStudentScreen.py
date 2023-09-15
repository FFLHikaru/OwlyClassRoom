import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from scanStudentComposants.StudentButton import StudentButton
from scannerScreenComposants.CustomLayout import CustomLayout

class ScanStudentScreen( QWidget ):
    def __init__(self, student_list : list ) -> None:
        super().__init__() 

        #### Variable logique ####
        self.student_list = []
        self.scanned_student = []

        #### Widgets ####

        self.student_button_list = []
        self.grid_layout = CustomLayout()


        #### Init logic ####

        self.student_list = result_list_to_student_list( student_list )
        self._create_all_student_button()
        
        self.setLayout(self.grid_layout)

        self._set_button_on_grid()

    #### Built in ####

    def resizeEvent( self, event ) -> None:
        self.grid_layout.geometry_changed.emit( self.geometry() )

        return super().resizeEvent( event )

    #### Class methods ####

    def _create_all_student_button( self ) -> None :
        i = 0
        j = 0
        for student in self.student_list : 
            self.student_button_list.append( StudentButton( student ) )
        return None
    
    def _set_button_on_grid( self ) -> None : 
        i=0
        for student_button in self.student_button_list : 
            self.grid_layout.addWidget( student_button, i//7 , i%7, 1, 1 )
            i+=1

    




def result_list_to_student_list( result_list : str ) -> list :
    student_list = []
    for student_result in result_list[1:] : 
        student_list.append(student_result[0])

    return student_list