from math import sin, cos, tan, atan, atan2, pi

# Calculation of the cartographic pole of the cylindrical projection


def deg_to_rad(deg):
    # Convert degrees to radians.
    return deg * pi / 180

def rad_to_deg(rad):
    # Convert radians to degrees.
    return rad * 180 / pi


def cartographic_pole(u1, v1, u2, v2):
    # Calculate the cartographic pole from two points.

    vk = atan2(
        tan(u1) * cos(v2) - tan(u2) * cos(v1),
        tan(u2) * sin(v1) - tan(u1) * sin(v2))

    uk = atan(
        -1 / tan(u2) * cos(vk - v2))

    return uk, vk


def compute_country(name, data):
    print(name)

    # Input points on the cartographic equator
    u1 = deg_to_rad(data["P1"][0])
    v1 = deg_to_rad(data["P1"][1])

    u2 = deg_to_rad(data["P2"][0])
    v2 = deg_to_rad(data["P2"][1])

    # Calculation of the cartographic pole
    uk, vk = cartographic_pole(u1, v1, u2, v2)

    print("Input points on the cartographic equator:")
    print(f"P1: u1 = {data['P1'][0]:.7f}°, v1 = {data['P1'][1]:.7f}°")
    print(f"P2: u2 = {data['P2'][0]:.7f}°, v2 = {data['P2'][1]:.7f}°")
    
    print("Cartographic pole:")
    print(f"uk = {rad_to_deg(uk):.9f}°")
    print(f"vk = {rad_to_deg(vk):.9f}°")


# Input coordinates
# u = geographic latitude
# v = geographic longitude

countries = {
    "Belarus": {
        "P1": (53.9876934, 22.9613584),
        "P2": (53.6887991, 32.5455298)},

    "Norway": {
        "P1": (59.1435133, 4.9893009),
        "P2": (71.4099133, 28.2471188)}}


# Run calculation

for country_name, country_data in countries.items():
    compute_country(country_name, country_data)