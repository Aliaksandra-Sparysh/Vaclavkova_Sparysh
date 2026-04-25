from math import *

def calculate_cartography_metrics(center_lat, center_lon, vertices):
    # Convert center coordinates to radians
    phi0 = radians(center_lat)
    lam0 = radians(center_lon)
    
    # Loop through all vertices
    for lat, lon in vertices:
        # Convert current vertex coordinates to radians
        phi = radians(lat)
        lam = radians(lon)
        d_lam = lam - lam0
        
        #Angular distance (z)
        cos_z = sin(phi) * sin(phi0) + cos(phi) * cos(phi0) * cos(d_lam)
        cos_z = max(-1.0, min(1.0, cos_z)) # Prevent rounding errors
        
        #Meridian convergence - gamma
        num = sin(d_lam) * sin(phi0)
        denom = cos(phi) * cos(phi0) + sin(phi) * sin(phi0) * cos(d_lam)
        gamma = degrees(atan2(num, denom))
        
        #Scale distortion - m
        m = 1 / (cos_z**2)
        
        #Round values to 4 decimal places
        convergence = round(abs(gamma), 4)
        distortion = round(m, 4)
        
        # Print output
        print("Lat:", lat, "Lon:", lon, "Convergence:", convergence, "Distortion:", distortion)


print("Tetrahedron")
calculate_cartography_metrics(19.4712, 60.0, [(-19.4712, 0.0), (-19.4712, 120.0), (90.0, 0.0)])

print("Cube")
calculate_cartography_metrics(0.0, 45.0, [(35.2644, 0.0), (35.2644, 90.0), (-35.2644, 90.0), (-35.2644, 0.0)])

print("Octahedron")
calculate_cartography_metrics(35.2644, 45.0, [(0.0, 0.0), (0.0, 90.0), (90.0, 0.0)])

print("Icosahedron")
calculate_cartography_metrics(52.62, 36.0, [(26.57, 0.0), (26.57, 72.0), (90.0, 36.0)])
