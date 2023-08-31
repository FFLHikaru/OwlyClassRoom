from PyQt5.QtWidgets import QWidget,QLabel,QGridLayout

class ClassGestureScreen(QWidget):
    screen_title=None
    student_button_liste=[]

#### init ####
    def __init__(self, class_name):
        super().__init__()
        main_Layout=QGridLayout()

        self.screen_title=QLabel(class_name)
        main_Layout.addWidget(self.screen_title,1,1,1,1)

        self.setLayout(main_Layout)

        #### signals connection

        
####Méthodes de classe



####Logic####

