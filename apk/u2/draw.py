from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Make lists
        self.__buildings = [] 
        self.__mbrs = []
        self.__chs = []
        #Maintain a temporary polygon for mouse clicks
        self.__current_building = QPolygonF() 
        self.__buildings.append(self.__current_building)

    def mousePressEvent(self, e):
        #Add points
        x = e.position().x()
        y = e.position().y()
        self.__current_building.append(QPointF(x, y))
        self.repaint()

    def loadBuildings(self, polygons):
        self.clearResult()
        self.__buildings.clear()
        
        for poly_rings in polygons:
            if len(poly_rings) > 0:
                #Take the first ring (outer boundary) for generalization
                ring = poly_rings[0] 
                building = QPolygonF()
                for point in ring:
                    p = QPointF(float(point[0]), float(point[1]))
                    building.append(p)
                self.__buildings.append(building)
        
        self.repaint()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.begin(self)
        
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        for b in self.__buildings:
            qp.drawPolygon(b)
        
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.transparent)
        for ch in self.__chs:
            qp.drawPolygon(ch)
        
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)
        for mbr in self.__mbrs:
            qp.drawPolygon(mbr)
        
        qp.end()

    def setMBRs(self, mbrs: list):
        self.__mbrs = mbrs
        
    def setCHs(self, chs: list):
        self.__chs = chs 

    def getBuildings(self):
        return self.__buildings

    def clearResult(self):
        self.__chs.clear()
        self.__mbrs.clear()
        self.repaint()
        
    def clearAll(self):
        self.__buildings.clear()
        self.__current_building = QPolygonF()
        self.__buildings.append(self.__current_building)
        self.clearResult()