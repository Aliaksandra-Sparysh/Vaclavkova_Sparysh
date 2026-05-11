from math import sin, cos, tan, atan, atan2, asin, acos, pi, log
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Equideformation lines of linear distortion for Norway

CONTOUR_STEP = 1.0
OUTLINE_FILE = Path(__file__).with_name("norsko.geojson")

def deg_to_rad(deg):
    return deg * pi / 180

def rad_to_deg(rad):
    return rad * 180 / pi

def transformed_latitude(u, v, uk, vk):
    return asin(sin(u) * sin(uk) + cos(u) * cos(uk) * cos(vk - v))


# MERCATOR PROJECTION

def mercator_parameters_no():
    u1 = deg_to_rad(59.1435133)
    v1 = deg_to_rad(4.9893009)

    u2 = deg_to_rad(71.4099133)
    v2 = deg_to_rad(28.2471188)

    u3 = deg_to_rad(68.7926664)
    v3 = deg_to_rad(14.4174102)

    vk = atan2(tan(u1) * cos(v2) - tan(u2) * cos(v1),
        tan(u2) * sin(v1) - tan(u1) * sin(v2))

    uk = atan(-1 / tan(u2) * cos(vk - v2))

    s3 = transformed_latitude(u3, v3, uk, vk)

    s0 = acos(2 * cos(s3) / (1 + cos(s3)))

    return uk, vk, s0


def mercator_distortion_no(u, v, params):
    uk, vk, s0 = params

    s = transformed_latitude(u, v, uk, vk)
    m = cos(s0) / cos(s)
    ny = (m - 1) * 1000

    return ny

# LAMBERT CONFORMAL CONIC PROJECTION

def lcc_parameters_no():
    R = 1.0

    uk = deg_to_rad(54.7247337)
    vk = deg_to_rad(46.8650335)

    u1 = deg_to_rad(68.8220156)
    v1 = deg_to_rad(14.5119521)

    u2 = deg_to_rad(60.0877399)
    v2 = deg_to_rad(12.5134610)

    s1 = transformed_latitude(u1, v1, uk, vk)
    s2 = transformed_latitude(u2, v2, uk, vk)

    cn = log(cos(s1)) - log(cos(s2))
    cd = log(tan(s2 / 2 + pi / 4)) - log(tan(s1 / 2 + pi / 4))
    c = cn / cd

    s0 = asin(c)

    rho0_n = 2 * R * cos(s0) * cos(s1) * (tan(s1 / 2 + pi / 4) ** c)
    rho0_d = c * (
        cos(s0) * (tan(s0 / 2 + pi / 4) ** c)
        + cos(s1) * (tan(s1 / 2 + pi / 4) ** c))

    rho0 = rho0_n / rho0_d

    return uk, vk, c, s0, rho0, R


def lcc_distortion_no(u, v, params):
    uk, vk, c, s0, rho0, R = params

    s = transformed_latitude(u, v, uk, vk)

    rho = rho0 * (
        (tan(s0 / 2 + pi / 4)) /
        (tan(s / 2 + pi / 4))) ** c

    m = (c * rho) / (R * cos(s))
    ny = (m - 1) * 1000

    return ny


# STEREOGRAPHIC PROJECTION

def stereo_parameters_no():
    uk = deg_to_rad(64.9646739)
    vk = deg_to_rad(18.7974046)

    u1 = deg_to_rad(58.0683207)
    v1 = deg_to_rad(6.6273357)

    sj = transformed_latitude(u1, v1, uk, vk)

    psi_j = pi / 2 - sj

    mu = (2 * cos(psi_j / 2) ** 2) / (1 + cos(psi_j / 2) ** 2)

    return uk, vk, mu


def stereo_distortion_no(u, v, params):
    uk, vk, mu = params

    s = transformed_latitude(u, v, uk, vk)
    psi = pi / 2 - s

    m = mu / (cos(psi / 2) ** 2)
    ny = (m - 1) * 1000

    return ny


# GRID, GEOJSON OUTLINE AND PLOTTING

def load_geojson_outline(filename=OUTLINE_FILE):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def iter_geojson_rings(geojson_data):
    for feature in geojson_data.get("features", []):
        geometry = feature.get("geometry", {})
        geometry_type = geometry.get("type")
        coordinates = geometry.get("coordinates", [])

        if geometry_type == "Polygon":
            polygons = [coordinates]
        elif geometry_type == "MultiPolygon":
            polygons = coordinates
        else:
            continue

        for polygon in polygons:
            if polygon:
                yield polygon[0]


def geojson_bounds(geojson_data):
    latitudes = []
    longitudes = []

    for ring in iter_geojson_rings(geojson_data):
        for lon, lat in ring:
            longitudes.append(lon)
            latitudes.append(lat)

    if not latitudes or not longitudes:
        raise ValueError("GeoJSON file does not contain Polygon or MultiPolygon coordinates.")

    return min(latitudes), max(latitudes), min(longitudes), max(longitudes)


def draw_geojson_outline(geojson_data):
    for ring in iter_geojson_rings(geojson_data):
        lon = [point[0] for point in ring]
        lat = [point[1] for point in ring]
        plt.plot(lon, lat, color="black", linewidth=1.2)


def build_grid(construction_points, reference_points, geojson_data=None):
    all_points = list(construction_points.values()) + list(reference_points.values())

    latitudes = [p[0] for p in all_points]
    longitudes = [p[1] for p in all_points]

    if geojson_data is not None:
        lat_min_geo, lat_max_geo, lon_min_geo, lon_max_geo = geojson_bounds(geojson_data)
        latitudes.extend([lat_min_geo, lat_max_geo])
        longitudes.extend([lon_min_geo, lon_max_geo])

    lat_min = min(latitudes) - 1.0
    lat_max = max(latitudes) + 1.0
    lon_min = min(longitudes) - 1.0
    lon_max = max(longitudes) + 1.0

    lat_grid = np.linspace(lat_min, lat_max, 250)
    lon_grid = np.linspace(lon_min, lon_max, 250)

    LON, LAT = np.meshgrid(lon_grid, lat_grid)

    return LON, LAT


def compute_distortion_grid(LAT, LON, distortion_function, params):
    NY = np.zeros_like(LAT)

    for i in range(LAT.shape[0]):
        for j in range(LAT.shape[1]):
            u = deg_to_rad(LAT[i, j])
            v = deg_to_rad(LON[i, j])
            NY[i, j] = distortion_function(u, v, params)

    return NY


def contour_levels(NY, step):
    max_abs = np.max(np.abs(NY))
    level_max = np.ceil(max_abs / step) * step
    return np.arange(-level_max, level_max + step, step)


def plot_projection(
    title,
    distortion_function,
    params,
    construction_points,
    reference_points,
    output_name,
    geojson_data):
    
    LON, LAT = build_grid(construction_points, reference_points, geojson_data)

    NY = compute_distortion_grid(LAT, LON, distortion_function, params)

    levels = contour_levels(NY, CONTOUR_STEP)

    plt.figure(figsize=(10, 7))

    contour = plt.contour(LON, LAT, NY, levels=levels, linewidths=1)

    draw_geojson_outline(geojson_data)

    plt.clabel(contour, inline=True, fontsize=8, fmt="%.2f")

    for point_name, (lat, lon) in construction_points.items():
        plt.scatter(lon, lat, s=90, marker="o", facecolors="none", edgecolors="red", linewidths=1.5)
        plt.text(lon, lat, f" {point_name}", fontsize=9, color="red")

    for point_name, (lat, lon) in reference_points.items():
        plt.scatter( lon,lat, s=45, marker="x", color="black", linewidths=1.2 )
        plt.text(lon, lat, f" {point_name}", fontsize=9, color="black")

    legend_handles = [
        Line2D( [0], [0], marker="o", color="red", markerfacecolor="none", markersize=8, linewidth=0, label="Construction points" ),
        Line2D( [0], [0], marker="x", color="black", markersize=8,  linewidth=0, label="Reference points"),
        Line2D([0],[0], color="black", linewidth=1.2, label="Country outline")]

    plt.legend(handles=legend_handles, loc="best")

    plt.title(title)
    plt.xlabel("Longitude [°]")
    plt.ylabel("Latitude [°]")
    plt.grid(True)

    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Figure saved as: {output_name}")


# COMMON REFERENCE POINTS FOR ALL FIGURES

points_P1_P4 = {
    "P1": (59.1435133, 4.9893009),
    "P2": (71.4099133, 28.2471188),
    "P3": (68.7926664, 14.4174102),
    "P4": (69.5588683, 30.9714340),}


# CONSTRUCTION POINTS FOR EACH PROJECTION

mercator_construction_points = {
    "P1": (59.1435133, 4.9893009),
    "P2": (71.4099133, 28.2471188),
    "P3": (68.7926664, 14.4174102),}

lcc_construction_points = {
    "North": (68.8220156, 14.5119521),
    "South": (60.0877399, 12.5134610),}

stereo_construction_points = {
    "Pole": (64.9646739, 18.7974046),
    "Edge": (58.0683207, 6.6273357),}


# LOAD GEOJSON OUTLINE

norway_outline = load_geojson_outline()


# CALCULATE PARAMETERS

mercator_params = mercator_parameters_no()
lcc_params = lcc_parameters_no()
stereo_params = stereo_parameters_no()


# RUN ALL THREE PLOTS

plot_projection(
    title="Equideformation lines of linear distortion, Norway, Mercator",
    distortion_function=mercator_distortion_no,
    params=mercator_params,
    construction_points=mercator_construction_points,
    reference_points=points_P1_P4,
    output_name="norway_equideformations_mercator.png",
    geojson_data=norway_outline)

plot_projection(
    title="Equideformation lines of linear distortion, Norway, Lambert Conformal Conic",
    distortion_function=lcc_distortion_no,
    params=lcc_params,
    construction_points=lcc_construction_points,
    reference_points=points_P1_P4,
    output_name="norway_equideformations_lcc.png",
    geojson_data=norway_outline)

plot_projection(
    title="Equideformation lines of linear distortion, Norway, Stereographic",
    distortion_function=stereo_distortion_no,
    params=stereo_params,
    construction_points=stereo_construction_points,
    reference_points=points_P1_P4,
    output_name="norway_equideformations_stereographic.png",
    geojson_data=norway_outline)