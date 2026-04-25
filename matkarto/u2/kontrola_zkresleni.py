from pyproj import Proj

def get_dist(c_lat, c_lon, v_lat, v_lon):
    p = Proj(f"+proj=gnom +lat_0={c_lat} +lon_0={c_lon} +R=1")
    f = p.get_factors(longitude=v_lon, latitude=v_lat)
    print(round(f.tissot_semimajor, 4))

# Tetrahedron
get_dist(19.4712, 60.0, -19.4712, 0.0)

# Cube
get_dist(0.0, 45.0, 35.2644, 0.0)

# Octahedron
get_dist(35.2644, 45.0, 0.0, 0.0)

# Icosahedron
get_dist(52.62, 36.0, 26.57, 0.0)