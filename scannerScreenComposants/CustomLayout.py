from PyQt5.QtWidgets import QLayout, QWidget
from PyQt5.QtCore import QRect, pyqtSignal


class CustomLayout(QLayout):

     #### Signals ####

    row_count_changed = pyqtSignal()
    column_count_changed = pyqtSignal()
    margin_size_changed = pyqtSignal()
    padding_changed = pyqtSignal()
    geometry_changed = pyqtSignal( QRect )

    ####Built-in####
    def count( self ) : 
        return 0
    def addItem( self,arg1):
        return None
    def itemAt( self, arg1 ):
        return None


    def __init__( self, dim : QRect = QRect(0,0,1920,1080) ):
        super().__init__()
        #### Variable Logique ####
        self.row_count : int = 1
        self.column_count : int =1

        self.width : int = 500 
        self.height : int = 500 
        self.row_margin_size : int = 0
        self.column_margin_size : int = 0
        self.padding : list = [ 0, 0, 0, 0 ]

        #### Widget ####

        self.widget_list = []  # Un widget est dans le format [widget, row, col, row_span, col_span]

        self.setGeometry(dim)
        self.width = self.geometry().width()
        self.height = self.geometry().height()

        #### Signals Connexion ####
        self.row_count_changed.connect( self._on_row_count_changed )
        self.column_count_changed.connect( self._on_column_count_changed )
        self.margin_size_changed.connect( self._on_margin_size_changed )
        self.padding_changed.connect( self._on_padding_changed )
        self.geometry_changed.connect( self._on_geometry_changed )


    #### Class methods #### 

    def delete_all( self ) -> None : 
        for widget in self.widget_list : 
            widget[0].deleteLater()
            self.removeWidget(widget[0])
        self.widget_list=[]

    def deleteWidget( self, widget : QWidget ) -> None :
        for i in range(len( self.widget_list )):
            if self.widget_list[i][0] == widget :
                print('widget trouvé')
                self.widget_list.pop(i)
                self.removeWidget( widget )

            
                return None
        return None
        


    def addWidget( self, widget : QWidget , row : int = 0, column : int = 0, row_span : int = 1, column_span : int = 1) -> None : 

        #widget.setFixedSize(20,20)
        self.widget_list.append([widget, row, column, row_span, column_span])
        super().addWidget( widget )
        self._create_new_line_needed( row, row_span )
        self._create_new_col_needed( column, column_span )
        self._adjust_dimension_and_position()

        return None

    def moveWidget ( self, widget : QWidget , row : int = 0, column : int = 0, row_span : int = 1, column_span : int = 1) -> None :
        index = 0
        while self.widget_list[index][0] != widget : 
                index+=1
                print(index)
        self.widget_list[index] = [widget, row, column, row_span, column_span]
        self._create_new_line_needed( row, row_span )
        self._create_new_col_needed( column, column_span )
        self._adjust_dimension_and_position()

        return None

    def set_padding( self, left : int, top : int, right : int, bottom : int) -> None : 
        if self.padding == [ left, top, right, bottom ]:
            return None
        self.padding = [ left, top, right, bottom ]
        self.padding_changed.emit()

        return None
    
    def set_margin(self, row_margin_size : int, col_margin_size : int ) -> None : 
        self.set_row_margin_size(row_margin_size)
        self.set_column_margin_size(col_margin_size)
        return None

    def _widget_dimension_changed( self, widget : QWidget ) -> None:
        if hasattr(widget , "has_been_resized") :
            widget.has_been_resized()
        return None

    def _adjust_dimension_and_position( self ) -> None :
        len(self.widget_list)

        for widget in self.widget_list : 
            current_width = widget[0].width()
            current_height = widget[0].height()

            row = widget[1]
            column = widget[2]
            row_span = widget[3]
            column_span = widget[4]

            widget_x,widget_y = self._get_position(row, column)

            if [ current_width,current_height ] != self._get_size( row_span, column_span ):
                self._widget_dimension_changed( widget[0] )

            widget_width,widget_height = self._get_size( row_span, column_span )
            
            widget[0].setGeometry( widget_x, widget_y , widget_width, widget_height)

        return None

    def _get_position( self, row : int = 0, column : int = 0 ) -> list :   

        vertical_padding = self.padding[1] + self.padding[3]
        horizontal_padding = self.padding[0] + self.padding[2]

        free_width = self.width - self.column_margin_size * ( self.column_count - 1 ) - vertical_padding
        free_height = self.height - self.row_margin_size * ( self.row_count -1 ) - horizontal_padding

        height_case  = (free_height // self.row_count)
        width_case = (free_width // self.column_count )


        return [ ( width_case + self.column_margin_size ) * column + self.padding[0] , ( height_case + self.row_margin_size ) * row + self.padding[1] ]
    
    def _get_size( self, row_span : int = 1, col_span : int = 1 ) -> list :

        bonus_width = self.column_margin_size * ( col_span -1 )
        bonus_height = self.row_margin_size * ( row_span - 1 )

        vertical_padding = self.padding[1] + self.padding[3]
        horizontal_padding = self.padding[0] + self.padding[2]

        free_width = self.width - self.column_margin_size * ( self.column_count - 1 ) - vertical_padding
        free_height = self.height - self.row_margin_size * ( self.row_count -1 ) - horizontal_padding

        width = free_width // self.column_count * col_span + bonus_width
        height = free_height // self.row_count * row_span + bonus_height
        return [ width, height ]

    def _create_new_line_needed( self, row : int, row_span : int) -> None : 
        self._set_row_count( (row+row_span) )
        return None
    
    def _create_new_col_needed( self, column : int, column_span : int) -> None :
        self._set_column_count( (column+column_span) )

    

    #### Set ####
    def set_row_margin_size( self, value : int ) -> None :
        if self.row_margin_size == value : 
            return None
        self.row_margin_size = value 
        self.margin_size_changed.emit()

        return None

    def _reduce_row_count( self, value : int ) -> None : 
        self.row_count = value
        self.row_count_changed.emit()
        return None

    def _reduce_col_count( self, value : int ) -> None : 
        self.column_count = value
        self.column_count_changed.emit()
        return None

    def set_column_margin_size( self, value : int ) -> None : 
        if self.column_margin_size == value : 
            return None
        self.column_margin_size = value
        self.margin_size_changed.emit()

    def _set_row_count(self, value : int) -> None : 
        if value > 0 :
            if value <= self.row_count : 
                return None
            self.row_count = value
            self.row_count_changed.emit()
        return None
    
    def _set_column_count( self, value : int) -> None :
        if value > 0 :
            if value <= self.column_count : 
                return None
            self.column_count = value
            self.column_count_changed.emit()
        return None


    #### Signals responses #### 

    def _on_row_count_changed( self ) -> None :
        return None
    
    def _on_column_count_changed( self ) -> None : 
        return None
    
    def _on_margin_size_changed( self ) -> None :
        self._adjust_dimension_and_position()
        return None
    
    def _on_padding_changed( self ) -> None : 
        self._adjust_dimension_and_position()
        return None

    def _on_geometry_changed( self, geo : QRect ) -> None :
        self.setGeometry(geo)
        self.width = self.geometry().width()
        self.height = self.geometry().height()
        self._adjust_dimension_and_position()
        return None

