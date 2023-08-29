from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout

class QuestionGestureScreen(QWidget):
    screen_title=None

#### init ####
    def __init__(self):
        super().__init__()
        main_Layout=QVBoxLayout()
        self.screen_title=QLabel('Gérer les questions')
        main_Layout.addWidget(self.screen_title)
        self.setLayout(main_Layout)

        #### signals connection

        
####Méthodes de classe



####Logic####



