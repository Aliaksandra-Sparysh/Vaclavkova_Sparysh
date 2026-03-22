from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # List of polygons (each polygon can contain multiple rings)
        self.__pols = []
        # Query point (tested against polygons)
        self.__q = QPointF(100, 100)
        self.__add_vertex = True
         # Currently highlighted polygons
        self.highlighted_polygon = None
        self.highlighted_polygons = []
        self.minmax_boxes = []

    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Set new q coordinates
        if not self.__add_vertex:
              # Clear previous results
            self.highlighted_polygons.clear() 
            self.setMinMaxBoxes([]) 
            # Set new query point position
            self.__q.setX(x)
            self.__q.setY(y)
            
            #Update
            self.update()

    def setMinMaxBoxes(self, boxes):
        self.minmax_boxes = boxes
        self.update()

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter()

        #Start draw
        if not qp.begin(self):
            return

        #Draw polygons with black outline and yellow fill
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)

        for poly_rings in self.__pols:
            # Use painter path to correctly handle polygons with holes
            path = QPainterPath()
            path.setFillRule(Qt.FillRule.OddEvenFill)
            for ring in poly_rings:
                path.addPolygon(ring)
            qp.drawPath(path)

        #Highlight polygon if found
        if len(self.highlighted_polygons) > 0:
            qp.setPen(Qt.GlobalColor.red)
            qp.setBrush(Qt.GlobalColor.red)
            for highlighted_poly_rings in self.highlighted_polygons:
                path = QPainterPath()
                path.setFillRule(Qt.FillRule.OddEvenFill)
                for ring in highlighted_poly_rings:
                    path.addPolygon(ring)
                qp.drawPath(path)

        # Draw min-max boxes
        if len(self.minmax_boxes) > 0:
            qp.setPen(QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.DashLine))
            qp.setBrush(Qt.BrushStyle.NoBrush)
            for box in self.minmax_boxes:
                qp.drawRect(box)

        #Draw point
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.green)

        r = 5
        qp.drawEllipse(int(self.__q.x()-r), int(self.__q.y()-r), 2*r, 2*r)

        #End draw
        qp.end()

    def changeStatus(self):
        #Input source: point or polygon
        self.__add_vertex = not (self.__add_vertex)

    def clearData(self):
        #Clear datas
        self.__pols.clear()
        self.__q.setX(-25)
        self.__q.setY(-25)
        self.highlighted_polygons = []
        self.minmax_boxes = []
        self.update()


    def setHighlightedPolygons(self, pols):
        self.highlighted_polygons = pols
        self.update()

    def getQ(self):
        #Return point
        return self.__q

    def getPol(self):
        return self.__pols


    def drawPolygons(self, polygons):
        self.clearData()
        # polygons is List[List[np.array]]
        for poly_rings in polygons:
            new_poly_rings = []
            for ring in poly_rings:
                new_ring = QPolygonF()
                for point in ring:
                    # Explicit conversion to float to avoid issues with numpy types in QPointF
                    p = QPointF(float(point[0]), float(point[1]))
                    new_ring.append(p)
                new_poly_rings.append(new_ring)
            self.__pols.append(new_poly_rings)
        self.update()