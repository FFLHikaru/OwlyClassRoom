from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from paramComposants.questionParamScreen import QuestionParamScreen
from paramComposants.classParamScreen import ClassParamScreen
from copy import deepcopy

class QuestionGestureScreen(QTabWidget):

#### Signals #### 


    def __init__( self, results_list, class_name ):
        #### Logic variables #### 

        self.student_list = result_list_to_student_list( results_list )

        #### Widget ####
        self.class_parameter_screen = ClassParamScreen( deepcopy( self.student_list ), class_name )
        self.question_parameter_screen = QuestionParamScreen( deepcopy( self.student_list ) )



        super().__init__()


        #### Init Logic #### 

        self.addTab( self.class_parameter_screen, " paramétrer la liste des élèves " )
        self.addTab( self.question_parameter_screen, " modifier les questions " )

        #### signals connection

        
    ####Public Class Methods ####

    def has_camera( self ) -> bool :
        return False   
    
    #### Private Class Methods #### 



####Logic functions####

def result_list_to_student_list( result_list : str ) -> list :
        student_list = []
        for student_result in result_list[1:] : 
            student_list.append(student_result[0])

        return student_list

