from PyQt5.QtWidgets import QFrame, QGridLayout
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure  # Importer la classe Figure
import matplotlib.patches as patches


class GraphScreen(QFrame):
    categories = ['Réponse A', 'Réponse B', 'Réponse C', 'Réponse D']
    reponses=[0,0,0,0]
    
    def __init__(self,reponsesScanned):
        super().__init__()
        self.reponses=[0,0,0,0]
        for reponse in reponsesScanned:
            if reponse[0]=='A':
                self.reponses[0]+=1
            elif reponse[0]=='B':
                self.reponses[1]+=1
            elif reponse[0]=='C':
                self.reponses[2]+=1
            else:
                self.reponses[3]+=1
                

        layout = QGridLayout()

        self.setStyleSheet('''
            background-color: rgba(255, 230, 218, 0);
        ''')
        
        # Créer une instance de la classe Figure
        fig = Figure(figsize=(5, 3))
        fig.set_facecolor((0.95,0.9,0.7,0.95))
        
        
        # Ajouter l'axe au figure
        ax = fig.add_subplot(111)  # 111 signifie 1x1 grid, first subplot
        
        bars = ax.bar(self.categories, self.reponses)
        ax.bar(self.categories, self.reponses)
        ax.tick_params(axis='x', labelsize=20) 
        ax.set_title('Liste des réponses',fontsize=30)
        ax.set_facecolor((0.95,0.9,0.7,0))
        # Créer le canvas à partir de la figure
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height/2,
                str(height),
                ha='center',
                va='bottom',
                fontsize=22
            )
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_yticks([])


        static_canvas = FigureCanvasQTAgg(fig)
    
        layout.addWidget(static_canvas)
        self.setLayout(layout)
