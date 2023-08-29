import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from ClassSelectionScreen import ClassSelectionScreen
from MainScreen import MainScreen
ecranActif=1
app = QApplication(sys.argv)

# Créer un widget principal pour contenir les autres widgets
main_widget = QStackedWidget()
main_widget.setStyleSheet('background-color:#F8F8FE')
classSelectionScreen=ClassSelectionScreen()
def classSelected(texte):
    mainScreen=MainScreen(texte)
    main_widget.addWidget(mainScreen)
    main_widget.setCurrentWidget(mainScreen)

classSelectionScreen.boutonClicked.connect(classSelected)



main_widget.addWidget(classSelectionScreen)
main_widget.resize(1920,1080)
main_widget.show()
sys.exit(app.exec_())                                