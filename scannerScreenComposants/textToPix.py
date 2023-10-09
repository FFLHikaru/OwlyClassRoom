import sys
import matplotlib as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PyQt5.QtGui import QImage,QPixmap
from PIL import Image, ImageDraw, ImageFont


from io import BytesIO
import matplotlib.pyplot as plt
plt.rc('mathtext', fontset='cm')

def tex2svg(formula, fontsize=24, dpi=300):
    try:
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, r'{}'.format(formula), fontsize=fontsize)

        output = BytesIO()
        fig.savefig(output, dpi=dpi, transparent=True, format='png',
                    bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)

        output.seek(0)

        image = QImage.fromData(output.read())
        pixmap = QPixmap.fromImage(image)
        
        return pixmap
    except Exception as e:
         # Créer une nouvelle image avec la taille spécifiée et un arrière-plan blanc
        image = Image.new('RGB', (400, 400),'white')
        draw = ImageDraw.Draw(image)
        
        
        
        # Dessiner le texte sur l'image
        draw.text((0,0), formula )
        
        # Convertir l'image Pillow en QImage
        image = image.convert('RGBA')
        qimage = QImage(image.tobytes(), image.size[0], image.size[1], QImage.Format_RGBA8888)
        
        # Convertir QImage en QPixmap
        qpixmap = QPixmap.fromImage(qimage)
        
        return qpixmap