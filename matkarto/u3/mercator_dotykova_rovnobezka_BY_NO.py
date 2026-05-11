from math import sin, cos, tan, atan, atan2, asin, acos, pi

# Exact calculation of the true parallel of the cylindrical projection

# Convert 
def deg_to_rad(deg):
    return deg * pi / 180

def rad_to_deg(rad):
    return rad * 180 / pi

def cartographic_pole(u1, v1, u2, v2):
    # Calculation of the cartographic pole from two points

    vk = atan2( tan(u1) * cos(v2) - tan(u2) * cos(v1), tan(u2) * sin(v1) - tan(u1) * sin(v2))

    uk = atan(-1 / tan(u2) * cos(vk - v2))

    return uk, vk


def transformed_latitude(u, v, uk, vk):
    # Calculation of the transformed cartographic latitude s

    return asin(sin(u) * sin(uk)+ cos(u) * cos(uk) * cos(vk - v))


def true_parallel_from_edge(s_edge):
    # Exact calculation of the true / standard parallel
    # cos(s0) = 2 * cos(s_edge) / (1 + cos(s_edge))

    return acos(2 * cos(s_edge) / (1 + cos(s_edge)))


def mercator_scale(s0, s):
    # Calculation of scale and linear distortion

    m = cos(s0) / cos(s)
    ny = (m - 1) * 1000
    return m, ny

# Run the calculation for one country.
def compute_country(name, data):
    # Run the calculation for one country.
    print(name)

    # Input points
    u1 = deg_to_rad(data["P1"][0])
    v1 = deg_to_rad(data["P1"][1])

    u2 = deg_to_rad(data["P2"][0])
    v2 = deg_to_rad(data["P2"][1])

    u3 = deg_to_rad(data["P3"][0])
    v3 = deg_to_rad(data["P3"][1])

    u4 = deg_to_rad(data["P4"][0])
    v4 = deg_to_rad(data["P4"][1])

    # Calculation of the cartographic pole
    uk, vk = cartographic_pole(u1, v1, u2, v2)

    # Transformation of points into the oblique aspect
    s1 = transformed_latitude(u1, v1, uk, vk)
    s2 = transformed_latitude(u2, v2, uk, vk)
    s3 = transformed_latitude(u3, v3, uk, vk)
    s4 = transformed_latitude(u4, v4, uk, vk)

    # Exact calculation of the true parallel
    s0 = true_parallel_from_edge(s3)

    # Calculation of scale and linear distortion
    results = { "P1": mercator_scale(s0, s1),
        "P2": mercator_scale(s0, s2),
        "P3": mercator_scale(s0, s3),
        "P4": mercator_scale(s0, s4),}

    # Output

    print("Cartographic pole:")
    print(f"uk = {rad_to_deg(uk):.9f}°")
    print(f"vk = {rad_to_deg(vk):.9f}°")

   # Print the transformed latitude of the selected edge point.
    print("Edge transformed latitude:")
    print(f"s3 = {rad_to_deg(s3):.9f}°")

    # Print the calculated true parallel
    print("True parallel of the cylindrical projection:")
    print(f"s0 = {rad_to_deg(s0):.9f}°")

    # Print the distortion check

    print("Control of distortions:")
    print(f"ny_center = {results['P1'][1]:.6f} ‰")
    print(f"ny_edge   = {results['P3'][1]:.6f} ‰")


# u =  latitude
# v =  longitude

countries = {
    "Belarus": {
        # Points on the cartographic equator
        "P1": (53.9876934, 22.9613584),
        "P2": (53.6887991, 32.5455298),

        # Edge points
        "P3": (56.1721272, 28.1401159),
        "P4": (51.2650360, 30.5382051),
    },

    "Norway": {
        # Points on the cartographic equator
        "P1": (59.1435133, 4.9893009),
        "P2": (71.4099133, 28.2471188),

        # Edge points
        "P3": (68.7926664, 14.4174102),
        "P4": (69.5588683, 30.9714340),
    }
}

# Calculation

for country_name, country_data in countries.items():
    compute_country(country_name, country_data)