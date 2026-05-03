from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from random import *
from triangle import * 
from edge import * 
from math import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__points = []
        self.__DT = []
        self.__contours = []
        self.__triangles = [] 
        self.__viewDT = True             
        self.__viewContours = True      
        self.__viewSlope = True     
        self.__viewAspect = False        
        self.__terrainMode = "random"

    def mousePressEvent(self, e):
        # Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
         # Define elevation range
        z_min = 200
        z_max = 600
        
        # Center of the canvas 
        cx = self.width() / 2
        cy = self.height() / 2
        
        # Distance from center
        dx = x - cx
        dy = y - cy
        dist = sqrt(dx*dx + dy*dy)

        # Generate elevation based on selected terrain mode
        if self.__terrainMode == "hill":
            z = 600 - dist

        elif self.__terrainMode == "valley":
            z = 200 + dist

        else:
            # Random terrain
            z = random() * (z_max - z_min) + z_min

        # Create new point
        p = QPoint3DF(x, y, z)
        
        # Add P to polygon
        self.__points.append(p)
        
        # Repaint
        self.repaint()

    def paintEvent(self, e):
        #Initialize the painter object
        qp = QPainter(self)
        qp.begin(self)

        #Draw only if Slope or Aspect view is enabled
        if self.__viewSlope or self.__viewAspect:
            for tri in self.__triangles:
                if self.__viewSlope:
                    #Visualize slope using grayscale shades
                    slope = tri.getSlope()
                    #Map: 0 rad (flat) = white, pi/2 (vertical) = black
                    grey_val = int(255 - min(255, slope * 255 / (pi/2)))
                    qp.setBrush(QColor(grey_val, grey_val, grey_val))
                
                elif self.__viewAspect:
                    #Visualize aspect using a color wheel
                    aspect = tri.getAspect()
                    #Map angle to Hue value (0-359)
                    hue = int(((aspect + pi) / (2 * pi)) * 359)
                    qp.setBrush(QColor.fromHsv(hue, 150, 255))
                
                #Set transparent border and draw the triangle polygon
                qp.setPen(Qt.GlobalColor.transparent) 
                p1, p2, p3 = tri.getVertices()
                poly = QPolygonF([p1, p2, p3])
                qp.drawPolygon(poly)

        #Draw edges if Delaunay Triangulation view is enabled
        if self.__viewDT:
            pen_dt = QPen(Qt.GlobalColor.green, 1)
            qp.setPen(pen_dt)
            qp.setBrush(Qt.BrushStyle.NoBrush)
            for edge in self.__DT:
                qp.drawLine(edge.getStart(), edge.getEnd())

        #Draw lines if Contour view is enabled
        if self.__viewContours:
           # counting
            i = 0 
            
            for c in self.__contours:
                z = c.getStart().z()
                
                #Highlight index contours (every 100 meters)
                if int(z) % 100 == 0:
                    pen_c = QPen(Qt.GlobalColor.red, 2)
                    draw_label = True  
                else:
                    pen_c = QPen(Qt.GlobalColor.gray, 1)
                    draw_label = False
                
                qp.setPen(pen_c)
                qp.drawLine(c.getStart(), c.getEnd())
                
                # Label
                if draw_label and i % 7 == 0:
                    x1 = c.getStart().x()
                    y1 = c.getStart().y()
                    x2 = c.getEnd().x()
                    y2 = c.getEnd().y()

                    # middle of segment
                    xm = (x1 + x2) / 2
                    ym = (y1 + y2) / 2

                    # label
                    label = str(int(z))

                    # offset
                    qp.setPen(Qt.GlobalColor.black)
                    qp.drawText(int(xm + 3), int(ym - 3), label)
                i += 1

        #Draw original points to see the input data
        pen_p = QPen(Qt.GlobalColor.black, 8)
        qp.setPen(pen_p)
        qp.drawPoints(self.__points)

        qp.end()
   

    def setDT(self, DT):
        #Set Delaunay Triangulation edges
        self.__DT = DT
        
    def getDT(self):
        #Return list of triangulation edges
        return self.__DT

    def getPoints(self):
        #Return list of input points
        return self.__points
    
    def setContours(self, contours):
        #Set generated contour lines
        self.__contours = contours

    
    def setTriangles(self, triangles):
        #Set generated triangle objects
        self.__triangles = triangles
    
    
    def getTriangles(self):
        #Return list of triangles
        return self.__triangles
    
    def setViewDT(self, state):
        #Toggle visibility of triangulation edges
        self.__viewDT = state
        self.repaint()

    def setViewContours(self, state):
        #Toggle visibility of contour lines
        self.__viewContours = state
        self.repaint()

    def setViewSlope(self, state):
        #Enable slope view and disable aspect
        self.__viewSlope = state
        if state:
            self.__viewAspect = False 
        self.repaint()

    def setViewExposition(self, state): 
        #Enable aspect view and disable slope
        self.__viewAspect = state
        if state:
            self.__viewSlope = False 
        self.repaint()

    def setTerrainMode(self, mode):
        self.__terrainMode = mode
   
    def clearResult(self):
        #Remove calculated data and refresh
        self.__DT.clear()
        self.__contours.clear()
        self.__triangles.clear() 
        self.repaint()

    
    def clearAll(self):
        #Remove points and all calculated data
        self.__points.clear()
        self.clearResult()