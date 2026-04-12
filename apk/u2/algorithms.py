from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np
import numpy.linalg as np2

class Algorithms:
    
    def __init__(self):
        pass
    
    def get2VectorsAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Angle between two vectors
        ux = p2.x() - p1.x()    
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()    
        
        #Dot product
        dot = ux*vx + uy*vy
        
        #Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5
        
        #Correct interval
        if nu * nv == 0: 
            return 0
            
        arg = dot/(nu*nv)
        arg = max(-1, min(1,arg)) 
        
        return acos(arg)
    
    
    def createCH(self, pol:QPolygonF):
        #Create Convex Hull using Jarvis Scan
        ch = QPolygonF()
        
        #Find pivot q (minimize y)
        q = min(pol, key = lambda k: k.y())

        #Find left-most point (minimize x)
        s = min(pol, key = lambda k: k.x())
        
        #Initial segment
        pj = q
        pj1 = QPointF(s.x() - 1, q.y())
        #Add to CH
        ch.append(pj)
        
        #Find all points of CH
        while True:
            #Maximum and its index
            omega_max = -1.0
            index_max = -1
            
            #Browse all points
            for i in range(len(pol)):
                
                #Different points
                if pj != pol[i]:
                    
                    #Compute omega
                    omega = self.get2VectorsAngle(pj, pj1, pj, pol[i])
            
                    #Actualize maximum
                    if(omega > omega_max):
                        omega_max = omega
                        index_max = i
            
            if index_max == -1:
                break

            #Add point to the convex hull
            ch.append(pol[index_max])
            
            #Reasign points
            pj1 = pj
            pj = pol[index_max]
            
            # Stopping condition
            if pj == q:
                break
            
        return ch
    
    
    def createMMB(self, pol:QPolygonF):
        # Create min max box and compute its area

        #Points with extreme coordinates         
        p_xmin = min(pol, key = lambda k: k.x())
        p_xmax = max(pol, key = lambda k: k.x())
        p_ymin = min(pol, key = lambda k: k.y())
        p_ymax = max(pol, key = lambda k: k.y())
        
        #Create vertices
        v1 = QPointF(p_xmin.x(), p_ymin.y())
        v2 = QPointF(p_xmax.x(), p_ymin.y())
        v3 = QPointF(p_xmax.x(), p_ymax.y())
        v4 = QPointF(p_xmin.x(), p_ymax.y())
        
        #Create new polygon
        mmb = QPolygonF([v1, v2, v3, v4])
        
        #Area of MMB
        area = (v2.x() - v1.x()) * (v3.y() - v2.y())
        
        return mmb, area
      

    def rotatePolygon(self, pol:QPolygonF, sig:float):
        #Rotate polygon according to a given angle
        pol_rot = QPolygonF()

        #Process all polygon vertices
        for i in range(len(pol)):

            #Rotate point
            x_rot = pol[i].x() * cos(sig) - pol[i].y() * sin(sig)
            y_rot = pol[i].x() * sin(sig) + pol[i].y() * cos(sig)

            #Create QPoint
            vertex = QPointF(x_rot, y_rot)

            # Add vertex to rotated polygon
            pol_rot.append(vertex)

        return pol_rot
    
    
    def createMBR(self, building:QPolygonF):
        #Create minimum bounding rectangle using repeated construction of mmb
        sigma_min = 0
        
        #Convex hull
        ch = self.grahamScan(building)
        
        #Initialization
        mmb_min, area_min = self.createMMB(ch)
        
        # Process all edges of convex hull
        n = len(ch)
        for i in range(n):
            #Coordinate differences
            dx = ch[(i+1)%n].x() - ch[i].x()
            dy = ch[(i+1)%n].y() - ch[i].y()
            
            # Compute direction
            sigma = atan2(dy, dx)
            
            #Rotate convex hull
            ch_r = self.rotatePolygon(ch, -sigma)
        
            #Compute min-max box
            mmb, area = self.createMMB(ch_r)
            
            #Did we find a better min-max box?
            if area < area_min:    
                #Update minimum
                area_min = area
                mmb_min = mmb
                sigma_min = sigma
                
        #Back rotation
        return  self.rotatePolygon(mmb_min, sigma_min) 

    
    def getArea(self, pol:QPolygonF):
        #Compute area    
        area = 0
        n = len(pol)
        
        # Process all vertices
        for i in range(n):
            area += pol[i].x() * (pol[(i + 1) % n].y() - pol[(i - 1 + n) % n].y())
            
        return abs(area)/2    
    
        
    def resizeRectangle(self, building:QPolygonF, mbr: QPolygonF):
        #Resizing rectangle area to match building area
        
        #Area of the rectangle
        A = self.getArea(mbr)
        
        #Area of the building
        Ab = self.getArea(building)
        
        #Fraction of both areas
        if A == 0: return mbr
        k = Ab / A
        
        #Compute centroid of the rectangle
        x_c = (mbr[0].x()+mbr[1].x()+mbr[2].x()+mbr[3].x()) / 4
        y_c = (mbr[0].y()+mbr[1].y()+mbr[2].y()+mbr[3].y()) / 4
        
        #Compute vectors 
        v1_x = mbr[0].x() - x_c
        v1_y = mbr[0].y() - y_c 
        
        v2_x = mbr[1].x() - x_c
        v2_y = mbr[1].y() - y_c 

        v3_x = mbr[2].x() - x_c
        v3_y = mbr[2].y() - y_c 
        
        v4_x = mbr[3].x() - x_c
        v4_y = mbr[3].y() - y_c
        
        #Resize vectors v1 - v4 
        v1_x_res = v1_x * sqrt(k)
        v1_y_res = v1_y * sqrt(k)
        
        v2_x_res = v2_x * sqrt(k)
        v2_y_res = v2_y * sqrt(k)
        
        v3_x_res = v3_x * sqrt(k)
        v3_y_res = v3_y * sqrt(k)
        
        v4_x_res = v4_x * sqrt(k)
        v4_y_res = v4_y * sqrt(k)
        
        #Compute new vertices
        p1_x = v1_x_res + x_c  
        p1_y = v1_y_res + y_c 
        
        p2_x = v2_x_res + x_c  
        p2_y = v2_y_res + y_c 
        
        p3_x = v3_x_res + x_c  
        p3_y = v3_y_res + y_c 
        
        p4_x = v4_x_res + x_c  
        p4_y = v4_y_res + y_c
        
        # Compute new coordinates
        p1 = QPointF(p1_x,  p1_y)
        p2 = QPointF(p2_x,  p2_y)
        p3 = QPointF(p3_x,  p3_y)
        p4 = QPointF(p4_x,  p4_y)   
        
        #Create polygon
        mbr_res = QPolygonF()
        mbr_res.append(p1)
        mbr_res.append(p2)
        mbr_res.append(p3)
        mbr_res.append(p4)
       
        return mbr_res
    
    
    def simplifyBuildingMBR(self, building:QPolygonF):
        #Simplify building using MBR
        mbr = self.createMBR(building)
        
        #Resize rectangle
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    
    
    def simplifyBuildingPCA(self, building:QPolygonF):
        #Simplify building using PCA
        X, Y = [], []
        
        #Convert polygon vertices to matrix
        for p in building:
            X.append(p.x())
            Y.append(p.y())
            
        #Create A
        A = np.array([X, Y])

        #Compute covariance matrix
        C = np.cov(A)
        
        #Singular Value Decomposition
        [U, S, V] = np2.svd(C)
        
        #Compute direction of the principal component
        sigma = atan2(V[0][1], V[0][0])

        #Rotate building by -sigma
        build_rot = self.rotatePolygon(building, -sigma)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate min-max box by sigma
        mbr = self.rotatePolygon(mmb, sigma)
        
        #Resize min-max box
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    def simplifyBuildingWallAverage(self, building:QPolygonF):
        # Simplify building using Wall Average method
        n = len(building)
        sum_sin = 0
        sum_cos = 0
        
        # Process all edges of the building
        for i in range(n):
            p1 = building[i]
            p2 = building[(i + 1) % n]
            
            # Coordinate differences
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            
            # Edge length
            length = sqrt(dx**2 + dy**2)
            
            if length > 0:
                # Direction of the edge
                sigma_i = atan2(dy, dx)
                
                # Accumulate directions using 4-omega reduction to ensure orthogonality
                sum_sin += length * sin(4 * sigma_i)
                sum_cos += length * cos(4 * sigma_i)
            
        # Compute the weighted average direction
        sigma = 0.25 * atan2(sum_sin, sum_cos)
        
        # Rotate building to be axis-aligned
        build_rot = self.rotatePolygon(building, -sigma)
        
        # Create Min-Max Box
        mmb, area = self.createMMB(build_rot)
        
        # Rotate back to original orientation
        mbr = self.rotatePolygon(mmb, sigma)
        
        # Resize to match original building area
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    def simplifyBuildingWeightedBisector(self, building: QPolygonF):
        
         # Simplify building to LOD0 using the Weighted Bisector method.
         # Calculates dominant direction based on corner angle bisectors.
        
        n = len(building)
        sum_sin = 0
        sum_cos = 0
        
        # Process all vertices to find bisectors
        for i in range(n):
            # Get three consecutive points to define a corner
            p_prev = building[(i - 1 + n) % n]
            p_curr = building[i]
            p_next = building[(i + 1) % n]
            
            # Directions of the two edges meeting at the vertex
            s1 = atan2(p_curr.y() - p_prev.y(), p_curr.x() - p_prev.x())
            s2 = atan2(p_next.y() - p_curr.y(), p_next.x() - p_curr.x())
            
            # Weight is the sum of the lengths of the two edges
            d1 = sqrt((p_curr.x() - p_prev.x())**2 + (p_curr.y() - p_prev.y())**2)
            d2 = sqrt((p_next.x() - p_curr.x())**2 + (p_next.y() - p_curr.y())**2)
            weight = d1 + d2
            
            # Average direction (bisector) with 2-omega reduction 
            # (Bisectors are related by 180 degrees)
            sum_sin += weight * sin(2 * (s1 + s2))
            sum_cos += weight * cos(2 * (s1 + s2))
            
        # Resulting dominant direction
        sigma = 0.5 * atan2(sum_sin, sum_cos)
        
        # Transformation process
        build_rot = self.rotatePolygon(building, -sigma)
        mmb, area = self.createMMB(build_rot)
        mbr = self.rotatePolygon(mmb, sigma)
        
        # Final LOD0 rectangle with same area as original
        return self.resizeRectangle(building, mbr)
    
    def simplifyBuildingLongestEdge(self, building: QPolygonF):
        #Find the longest edge
        max_dist = -1
        sigma_max = 0
        n = len(building)
        
        for i in range(n):
            p1 = building[i]
            p2 = building[(i + 1) % n]
            
            #Compute lenght of the edge
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            dist = (dx**2 + dy**2)**0.5
            
            #Update maximum
            if dist > max_dist:
                max_dist = dist
                sigma_max = atan2(dy, dx)
        
        #Rotate building 
        build_rot = self.rotatePolygon(building, -sigma_max)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate back by sigma
        mbr = self.rotatePolygon(mmb, sigma_max)
        
        #Resize the area
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    def getOrientation(self, p: QPointF, q: QPointF, r: QPointF):
        dx1 = q.x() - p.x()
        dy1 = q.y() - p.y()
        dx2 = r.x() - q.x()
        dy2 = r.y() - q.y()
        
        val = (dy1 * dx2) - (dx1 * dy2)
        
        if abs(val) < 1e-9:
            return 0  
        if val > 0:
            return 1  
        else:
            return 2  
        
    def grahamScan(self, pol: QPolygonF):
        n = len(pol)
        if n < 3: 
            return pol

        p0 = pol[0]
        for i in range(1, n):
            if pol[i].y() < p0.y() or (pol[i].y() == p0.y() and pol[i].x() < p0.x()):
                p0 = pol[i]

        points_with_angles = []
        for p in pol:
            angle = atan2(p.y() - p0.y(), p.x() - p0.x())
            dist = (p.x() - p0.x())**2 + (p.y() - p0.y())**2
            points_with_angles.append((angle, dist, p))

        points_with_angles.sort()
        sorted_points = [item[2] for item in points_with_angles]

        hull = []
        for p in sorted_points:
            while len(hull) >= 2:
                orientation = self.getOrientation(hull[-2], hull[-1], p)
                if orientation != 2: 
                    hull.pop()
                else:
                    break
            hull.append(p)

        return QPolygonF(hull)
    def calculateRMSError(self, building: QPolygonF, simplified: QPolygonF):
        
        #Calculates the Root Mean Square Error (RMSE) of the angular deviation 
        #between the original building edges and the simplified rectangle.
        
        n = len(building)
        sum_sq_diff = 0
        total_length = 0
        
        # Get the main direction of the simplified rectangle (first edge)
        dx_ref = simplified[1].x() - simplified[0].x()
        dy_ref = simplified[1].y() - simplified[0].y()
        sigma_ref = atan2(dy_ref, dx_ref)
        
        for i in range(n):
            p1 = building[i]
            p2 = building[(i + 1) % n]
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            length = sqrt(dx**2 + dy**2)
            
            if length > 0:
                sigma_i = atan2(dy, dx)
                # Calculate angular difference reduced to 90 degrees (orthogonality)
                diff = (sigma_i - sigma_ref) % (pi/2)
                if diff > pi/4: 
                    diff -= pi/2
                
                sum_sq_diff += (diff**2) * length
                total_length += length
        
        # Weighted RMS error in radians
        rms_rad = sqrt(sum_sq_diff / total_length) if total_length > 0 else 0
        return rms_rad