from math import sin, cos, tan, atan, atan2, asin, acos, pi, log
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import json

# Equideformation lines of linear distortion for Belarus

CONTOUR_STEP = 1.0

def deg_to_rad(deg):
    # Convert degrees to radians
    return deg * pi / 180

def rad_to_deg(rad):
    # Convert radians to degrees
    return rad * 180 / pi


def transformed_latitude(u, v, uk, vk):
    # Transform geographic coordinates into the oblique aspect
    return asin(sin(u) * sin(uk) + cos(u) * cos(uk) * cos(vk - v))


# GEOJSON COUNTRY OUTLINE

def load_country_outline_geojson(filename):
    # Load country outline from a GeoJSON file.
    with open(filename, "r", encoding="utf-8") as file:
        geojson = json.load(file)

    outlines = []

    for feature in geojson["features"]:
        geometry = feature["geometry"]
        geom_type = geometry["type"]
        coordinates = geometry["coordinates"]

        if geom_type == "Polygon":
            for ring in coordinates:
                lon = [point[0] for point in ring]
                lat = [point[1] for point in ring]
                outlines.append((lon, lat))

        elif geom_type == "MultiPolygon":
            for polygon in coordinates:
                for ring in polygon:
                    lon = [point[0] for point in ring]
                    lat = [point[1] for point in ring]
                    outlines.append((lon, lat))

    return outlines

def plot_country_outline(filename):
    # Plot country boundary from a GeoJSON file.
    outlines = load_country_outline_geojson(filename)

    for lon, lat in outlines:
        plt.plot(lon, lat, color="black", linewidth=1.5)

# MERCATOR PROJECTION

def mercator_parameters_no():
    # Points on the cartographic equator
    u1 = deg_to_rad(53.9876934)
    v1 = deg_to_rad(22.9613584)

    u2 = deg_to_rad(53.6887991)
    v2 = deg_to_rad(32.5455298)

    # Edge point used for the true parallel
    u3 = deg_to_rad(56.1721272)
    v3 = deg_to_rad(28.1401159)

    # Cartographic pole
    vk = atan2(
        tan(u1) * cos(v2) - tan(u2) * cos(v1),
        tan(u2) * sin(v1) - tan(u1) * sin(v2))

    uk = atan(-1 / tan(u2) * cos(vk - v2))

    # Transformed latitude of the edge point
    s3 = transformed_latitude(u3, v3, uk, vk)

    # True parallel
    s0 = acos(2 * cos(s3) / (1 + cos(s3)))

    return uk, vk, s0


def mercator_distortion_no(u, v, params):
    # Linear distortion for the Mercator projection
    uk, vk, s0 = params

    s = transformed_latitude(u, v, uk, vk)
    m = cos(s0) / cos(s)
    ny = (m - 1) * 1000

    return ny

# LAMBERT CONFORMAL CONIC PROJECTION

def lcc_parameters_no():
    R = 1.0

    # Cartographic pole
    uk = deg_to_rad(38.9682253)
    vk = deg_to_rad(25.6855252)

    # Northernmost point
    u1 = deg_to_rad(56.1734200)
    v1 = deg_to_rad(28.1382440)

    # Southernmost point
    u2 = deg_to_rad(51.4688578)
    v2 = deg_to_rad(27.7471415)

    # Transformation into the oblique aspect
    s1 = transformed_latitude(u1, v1, uk, vk)
    s2 = transformed_latitude(u2, v2, uk, vk)

    # Constant c of the conic projection
    cn = log(cos(s1)) - log(cos(s2))
    cd = log(tan(s2 / 2 + pi / 4)) - log(tan(s1 / 2 + pi / 4))
    c = cn / cd

    # Compute s0
    s0 = asin(c)

    # Compute rho0
    rho0_n = 2 * R * cos(s0) * cos(s1) * (tan(s1 / 2 + pi / 4) ** c)
    rho0_d = c * (
        cos(s0) * (tan(s0 / 2 + pi / 4) ** c)
        + cos(s1) * (tan(s1 / 2 + pi / 4) ** c))
    rho0 = rho0_n / rho0_d

    return uk, vk, c, s0, rho0, R


def lcc_distortion_no(u, v, params):
    # Linear distortion for the Lambert conformal conic projection.
    uk, vk, c, s0, rho0, R = params

    s = transformed_latitude(u, v, uk, vk)
    rho = rho0 * ((tan(s0 / 2 + pi / 4)) / (tan(s / 2 + pi / 4))) ** c
    m = (c * rho) / (R * cos(s))
    ny = (m - 1) * 1000

    return ny


# STEREOGRAPHIC PROJECTION

def stereo_parameters_no():
    # Cartographic pole
    uk = deg_to_rad(53.4474898)
    vk = deg_to_rad(27.7220901)

    # Edge point
    u1 = deg_to_rad(53.3907239)
    v1 = deg_to_rad(32.7812055)

    # Transformation of the edge point
    sj = transformed_latitude(u1, v1, uk, vk)

    # psi_j = 90° - sj
    psi_j = pi / 2 - sj

    # Multiplication constant
    mu = (2 * cos(psi_j / 2) ** 2) / (1 + cos(psi_j / 2) ** 2)

    return uk, vk, mu


def stereo_distortion_no(u, v, params):
    # Linear distortion for the stereographic projection.
    uk, vk, mu = params

    s = transformed_latitude(u, v, uk, vk)
    psi = pi / 2 - s

    m = mu / (cos(psi / 2) ** 2)
    ny = (m - 1) * 1000

    return ny

# GRID AND PLOTTING

def build_grid(construction_points, reference_points):
    # Build the geographic extent from all displayed points.

    all_points = list(construction_points.values()) + list(reference_points.values())

    latitudes = [p[0] for p in all_points]
    longitudes = [p[1] for p in all_points]

    lat_min = min(latitudes) - 1.0
    lat_max = max(latitudes) + 1.0
    lon_min = min(longitudes) - 1.0
    lon_max = max(longitudes) + 1.0

    lat_grid = np.linspace(lat_min, lat_max, 250)
    lon_grid = np.linspace(lon_min, lon_max, 250)

    LON, LAT = np.meshgrid(lon_grid, lat_grid)

    return LON, LAT

def compute_distortion_grid(LAT, LON, distortion_function, params):
    # Compute distortion value in every grid point.
    NY = np.zeros_like(LAT)

    for i in range(LAT.shape[0]):
        for j in range(LAT.shape[1]):
            u = deg_to_rad(LAT[i, j])
            v = deg_to_rad(LON[i, j])
            NY[i, j] = distortion_function(u, v, params)

    return NY

def contour_levels(NY, step):
    # Create symmetric contour levels.
    max_abs = np.max(np.abs(NY))
    level_max = np.ceil(max_abs / step) * step
    return np.arange(-level_max, level_max + step, step)


def plot_projection(title, distortion_function, params,
                    construction_points, reference_points, output_name,
                    outline_file=None):

    # Build grid
    LON, LAT = build_grid(construction_points, reference_points)

    # Compute distortion grid
    NY = compute_distortion_grid(LAT, LON, distortion_function, params)

    # Create contour levels with larger spacing
    levels = contour_levels(NY, CONTOUR_STEP)

    # Create plot
    plt.figure(figsize=(10, 7))

    contour = plt.contour(LON, LAT, NY, levels=levels, linewidths=1)

    # Label contour lines in m/km.
    plt.clabel(contour, inline=True, fontsize=8, fmt="%.2f")

    # Plot country outline.
    if outline_file is not None:
        plot_country_outline(outline_file)

    # Plot construction points.
    for point_name, (lat, lon) in construction_points.items():
        plt.scatter( lon, lat, s=90, marker="o", facecolors="none", edgecolors="red", linewidths=1.5)
        plt.text(lon, lat, f" {point_name}", fontsize=9, color="red")

    # Plot reference points.
    for point_name, (lat, lon) in reference_points.items():
        plt.scatter(lon,lat,  s=45,   marker="x",  color="black",  linewidths=1.2 )
        plt.text(lon, lat, f" {point_name}", fontsize=9, color="black")

    # Legend.
    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="red",
            markerfacecolor="none",
            markersize=8,
            linewidth=0,
            label="Construction points"),
        
        Line2D(
            [0],
            [0],
            marker="x",
            color="black",
            markersize=8,
            linewidth=0,
            label="Reference points"),
        
        Line2D(
            [0],
            [0],
            color="black",
            linewidth=1.5,
            label="Country outline")]

    plt.legend(handles=legend_handles, loc="best")

    plt.title(title)
    plt.xlabel("Longitude [°]")
    plt.ylabel("Latitude [°]")
    plt.grid(True)

    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Figure saved as: {output_name}")


# COMMON REFERENCE POINTS FOR ALL FIGURES

# These points are shown in every plot for comparison.
points_P1_P4 = {
    "P1": (53.9876934, 22.9613584),
    "P2": (53.6887991, 32.5455298),
    "P3": (56.1721272, 28.1401159),
    "P4": (51.2650360, 30.5382051),}


# CONSTRUCTION POINTS FOR EACH PROJECTION

# Mercator:
# P1 and P2 define the cartographic equator.
# P3 is the edge point used for the true parallel.
mercator_construction_points = {
    "P1": (53.9876934, 22.9613584),
    "P2": (53.6887991, 32.5455298),
    "P3": (56.1721272, 28.1401159),
}

# Lambert conformal conic:
# North and South are points used to define the conic projection.
lcc_construction_points = {
    "North": (56.1734200, 28.1382440),
    "South": (51.4688578, 27.7471415),
}

# Stereographic:
# Pole is the center/cartographic pole of the projection.
# Edge is the point used for the scale optimization.
stereo_construction_points = {
    "Pole": (53.4474898, 27.7220901),
    "Edge": (53.3907239, 32.7812055),
}


# CALCULATE PARAMETERS

mercator_params = mercator_parameters_no()
lcc_params = lcc_parameters_no()
stereo_params = stereo_parameters_no()


# COUNTRY OUTLINE FILE

outline_file = "blr.geo.json"


# RUN ALL THREE PLOTS
plot_projection(
    title="Equideformation lines of linear distortion, Belarus, Mercator",
    distortion_function=mercator_distortion_no,
    params=mercator_params,
    construction_points=mercator_construction_points,
    reference_points=points_P1_P4,
    output_name="belarus_equideformations_mercator.png",
    outline_file=outline_file)

plot_projection(
    title="Equideformation lines of linear distortion, Belarus, Lambert Conformal Conic",
    distortion_function=lcc_distortion_no,
    params=lcc_params,
    construction_points=lcc_construction_points,
    reference_points=points_P1_P4,
    output_name="belarus_equideformations_lcc.png",
    outline_file=outline_file)

plot_projection(
    title="Equideformation lines of linear distortion, Belarus, Stereographic",
    distortion_function=stereo_distortion_no,
    params=stereo_params,
    construction_points=stereo_construction_points,
    reference_points=points_P1_P4,
    output_name="belarus_equideformations_stereographic.png",
    outline_file=outline_file)