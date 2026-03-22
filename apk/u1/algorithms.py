
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *


class Algorithms:
    def __init__(self):
        # Tolerance used to slightly expand the bounding box
        self.tolerance = 5
    def createMinMaxBox(self, poly_rings: list[QPolygonF]):
         # Initialize extreme values for bounding box computation
        min_x = float("inf")
        max_x = float("-inf")
        min_y = float("inf")
        max_y = float("-inf")
        
        # Iterate through all polygon rings and their vertices
        for ring in poly_rings:
            for p in ring:
                # Update minimum and maximum coordinates
                if p.x() < min_x:
                    min_x = p.x()
                if p.x() > max_x:
                    max_x = p.x()
                if p.y() < min_y:
                    min_y = p.y()
                if p.y() > max_y:
                    max_y = p.y()
                    
         # Create and return bounding box
        return QRectF(
            QPointF(min_x - self.tolerance, min_y - self.tolerance),
            QPointF(max_x + self.tolerance, max_y + self.tolerance)
        )

    def pointInMinMaxBox(self, q: QPointF, box: QRectF):
        return box.left() <= q.x() <= box.right() and box.top() <= q.y() <= box.bottom()
    
    def getPointPolygonPositionRC(self, q:QPointF, poly_rings:list[QPolygonF]):
        #Analyze point and polygon position using ray crossing algorithm
        k = 0  
        
        for pol in poly_rings:
            n = len(pol) 
            for i in range(n):
                #Check vertex hit
                dist_v = sqrt((q.x() - pol[i].x())**2 + (q.y() - pol[i].y())**2) 
                if dist_v <= self.tolerance: 
                    return -2 

        #Process polygon parts
        for pol in poly_rings:
            n = len(pol)
            for i in range(n):
                p_i = pol[i]
                p_ii = pol[(i + 1) % n]

                #Start point of the edge
                xi = pol[i].x() - q.x()
                yi = pol[i].y() - q.y()
                
                #End point of the edge        
                xi1 = pol[(i+1)%n].x() - q.x()
                yi1 = pol[(i+1)%n].y() - q.y()

                ux_e = pol[(i+1)%n].x() - pol[i].x()
                uy_e = pol[(i+1)%n].y() - pol[i].y()
                vx_p = q.x() - pol[i].x()
                vy_p = q.y() - pol[i].y()
                
                # Calculate the squared length of the edge vector
                l2 = ux_e**2 + uy_e**2
                # Evaluate if the point lies directly on the edge
                if l2 == 0:
                    dist = sqrt(vx_p**2 + vy_p**2)
                else:
                    t_proj = max(0.0, min(1.0, (vx_p * ux_e + vy_p * uy_e) / l2))
                    dist = sqrt((q.x() - (pol[i].x() + t_proj * ux_e))**2 + (q.y() - (pol[i].y() + t_proj * uy_e))**2)
                
                #If the point hits the edge buffer
                if dist <= self.tolerance:
                    return -1
                
                #Find suitable segment
                if (yi1 > 0) and (yi<= 0) or (yi > 0) and (yi1 <= 0):
                    #Compute intersection
                    xm = (xi1 * yi - xi * yi1) / (yi1 - yi) 
                    #Correct intersection
                    if xm > 0:
                        #Increment number of intersections
                        k = k + 1   
                        
        #Point is inside the polygon 
        if k % 2 == 1:
            return 1 
            
        #Point is outside the polygon
        return 0    
    

    def getPointPolygonPositionWinding(self, q, poly_rings:list[QPolygonF]):
        #Initialize the total winding angle
        total_angle = 0
        #handling floating-point inaccuracies
        eps = 0.000001
        
        for pol in poly_rings:
            n = len(pol)
            for i in range(n):
                dist_v = sqrt((q.x() - pol[i].x())**2 + (q.y() - pol[i].y())**2) 
                if dist_v <= self.tolerance: 
                    return -2
        
        for pol in poly_rings:
            n = len(pol)
            for i in range(n):
                p_i = pol[i]
                p_ii = pol[(i + 1) % n]
                
                #Calculate vector components relative to point q
                ux = p_i.x() - q.x()
                uy = p_i.y() - q.y()
                vx = p_ii.x() - q.x()
                vy = p_ii.y() - q.y()
                
                #Calculate cross and dot products for boundary check
                t = ux * vy - uy * vx
                dot_product = ux * vx + uy * vy
                
                ux_e = pol[(i+1)%n].x() - pol[i].x()
                uy_e = pol[(i+1)%n].y() - pol[i].y()
                vx_p = q.x() - pol[i].x()
                vy_p = q.y() - pol[i].y()
                
                #Calculate the squared length of the edge
                l2 = ux_e**2 + uy_e**2
                if l2 == 0:
                    dist = sqrt(vx_p**2 + vy_p**2)
                else:
                    t_proj = max(0.0, min(1.0, (vx_p * ux_e + vy_p * uy_e) / l2))
                    dist = sqrt((q.x() - (pol[i].x() + t_proj * ux_e))**2 + (q.y() - (pol[i].y() + t_proj * uy_e))**2)
                
                if dist <= self.tolerance:
                    return -1
            
                # Calculate vector norms
                u_norm = sqrt(ux**2 + uy**2)
                v_norm = sqrt(vx**2 + vy**2)

                #Handle zero-length vectors to prevent division by zero errors
                if u_norm * v_norm <= eps:
                    cos_omega = 1.0
                else:
                    cos_omega = max(-1, min(1, dot_product / (u_norm * v_norm)))
                
                #Compute the angle in radians
                omega_i = acos(cos_omega)
            
                # Add or subtract angle based on position
                if t > 0:
                    total_angle += omega_i
                elif t < 0:
                    total_angle -= omega_i
            
        # Check if total angle is 2*pi
        if abs(abs(total_angle) - 2 * pi) < eps:
            return 1  
        else:
            return 0