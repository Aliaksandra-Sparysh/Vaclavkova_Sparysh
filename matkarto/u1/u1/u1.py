from math import *
from uvtosd import*

def WGSToJTSK (phi_WGS, la_WGS):
    #WGS84 parameters
    a_WGS = 6378137.00
    b_WGS = 6356752.3142
    
    e2_WGS = (a_WGS*a_WGS - b_WGS*b_WGS)/(a_WGS*a_WGS)
    W_WGS = sqrt(1-e2_WGS*(sin(phi_WGS))**2)
    N_WGS = a_WGS/W_WGS
    
    #XYZ coordinates, WGS 84
    X_WGS = N_WGS * (cos(phi_WGS) * cos(la_WGS))
    Y_WGS = N_WGS * (cos(phi_WGS) * sin(la_WGS))
    Z_WGS = N_WGS * (1 - e2_WGS) * sin(phi_WGS)

    print("WGS_XYZ:", X_WGS, Y_WGS, Z_WGS)
    
    #Helmert transformation, parameters
    om_x = 4.9984 / 3600 * pi /180 
    om_y = 1.5867 /3600 * pi / 180
    om_z = 5.2611 /3600 * pi / 180
    m = 1 - 3.5623e-06
    dlt_x = -570.8285
    dlt_y = -85.6769
    dlt_z = -462.8420
    
    #Helmert transformation, Bessel ellipsoid
    X_Bes = m * (X_WGS + Y_WGS * om_z - om_y * Z_WGS) + dlt_x
    Y_Bes = m * (-om_z * X_WGS + Y_WGS + om_x * Z_WGS) + dlt_y
    Z_Bes = m * (om_y * X_WGS - om_x * Y_WGS + Z_WGS) + dlt_z

    print("Bessel_XYZ:", X_Bes, Y_Bes, Z_Bes)
    
    #Bessel parameters
    a_Bes = 6377397.155
    b_Bes = 6356078.963
    e2_Bes = (a_Bes*a_Bes - b_Bes*b_Bes)/(a_Bes*a_Bes)
   
    #Phi, lam, Bessel
    la_Bes = atan2(Y_Bes,X_Bes)
    tan_phi_Bes = Z_Bes / ((1 - e2_Bes) * sqrt(X_Bes**2 + Y_Bes**2))
    phi_Bes = atan(tan_phi_Bes)

    print("Bess_lam_phi:", la_Bes, phi_Bes)
    
    #Shift to Feerro
    la_Ferro = la_Bes + (17 + 2/3) * pi / 180
    
    #Gauss conformal projection, parameters
    phi0 = 49.5 * pi / 180
    alpha = sqrt (1 + e2_Bes * (cos(phi0))**4 / (1 - e2_Bes))
    u0 = asin(sin(phi0)/alpha)
    
    kn = (tan(phi0/2+pi/4)**alpha*((1-sqrt(e2_Bes)*sin(phi0))/(1+sqrt(e2_Bes)*sin(phi0)))**(alpha*sqrt(e2_Bes)/2))
    kd = tan(u0/2+pi/4)
    k = kn / kd
    
    R = (a_Bes*sqrt(1-e2_Bes))/(1-e2_Bes*(sin(phi0)**2))
    print("alpha, u0, k:", alpha, u0, k)
 
    #Gauss conformal projection
    u = 2*(atan(1/k*(tan(phi_Bes/2+pi/4)*((1-sqrt(e2_Bes)*sin(phi_Bes))/(1+sqrt(e2_Bes)*sin(phi_Bes)))**(sqrt(e2_Bes)/2))**alpha))-pi/2

    v = alpha*la_Ferro

    print("Gauss u,v:", u,v)
    
    #Cartographic pole
    uk = (59+(42/60)+(42.6969/3600))*(pi/180)
    vk = (42+(31/60)+(31.41725/3600))*(pi/180)

    print("uk, vk:",uk, vk)
    
    #Conversion (u, v) -> (s, d)
    s, d = uvTosd(u, v, uk, vk)

    print("š,d:",s,d)
    
    #LCC
    s0 = 78.5 * pi/180
    rho0 = R*1/tan(s0)*0.9999
    c = sin(s0)
    print("c, š0, rho0:",c, s0, rho0)
    
    rho = rho0*((tan(s0/2+pi/4))/(tan(s/2+pi/4)))**c
    eps = c * d
    print("rho,eps:",rho, eps)
   

    # (rho, eps) -> (y, x)
    y_jtsk = rho*sin(eps)
    x_jtsk = rho*cos(eps)
    
    print("Křovák y,x:",y_jtsk, x_jtsk)

    #Meridian convergence
    ksi = asin(cos(uk) * sin(pi - d) / cos(u))
    mer_conv = (eps - ksi)

    print("mer_conv:", mer_conv)

    #Scale distortion
    m = (c * rho) / (R * cos(s))
    m_distortion= m - 1
    print("m",m)
    print("m_distortion",m_distortion)

def Ignore_Ellipsoid_Change (phi_WGS, la_WGS):
    #Skipping Helmert transformation, treating WGS84 as Bessel
    phi_Bes = phi_WGS
    la_Bes = la_WGS
    
    #Bessel Ellipsoid parameters
    a_Bes = 6377397.155
    b_Bes = 6356078.963
    e2_Bes = (a_Bes**2 - b_Bes**2) / (a_Bes**2)
    
    #Shift to Ferro
    la_Ferro = la_Bes + (17 + 2/3) * pi / 180
    
    #Gauss conformal projection parameters
    phi0 = 49.5 * pi / 180
    alpha = sqrt(1 + e2_Bes * (cos(phi0))**4 / (1 - e2_Bes))
    u0 = asin(sin(phi0) / alpha)
    
    kn = (tan(phi0/2+pi/4)**alpha*((1-sqrt(e2_Bes)*sin(phi0))/(1+sqrt(e2_Bes)*sin(phi0)))**(alpha*sqrt(e2_Bes)/2))
    kd = tan(u0/2+pi/4)
    k = kn / kd
    R = (a_Bes * sqrt(1 - e2_Bes)) / (1 - e2_Bes * (sin(phi0)**2))
    
    #Spherical latitude u and longitude v
    u = 2*(atan(1/k*(tan(phi_Bes/2+pi/4)*((1-sqrt(e2_Bes)*sin(phi_Bes))/(1+sqrt(e2_Bes)*sin(phi_Bes)))**(sqrt(e2_Bes)/2))**alpha))-pi/2
    v = alpha * la_Ferro
    
    #Cartographic pole coordinates
    uk = (59+(42/60)+(42.6969/3600))*(pi/180)
    vk = (42+(31/60)+(31.41725/3600))*(pi/180)
    
    s_approx, d_approx = uvTosd(u, v, uk, vk)
    
    #LCC 
    s0 = 78.5 * pi / 180
    c_const = sin(s0)
    rho0 = R * (1/tan(s0)) * 0.9999
    rho_approx = rho0 * ((tan(s0/2+pi/4)) / (tan(s_approx/2+pi/4)))**c_const
    eps_approx = c_const * d_approx
    
    y_approx = rho_approx * sin(eps_approx)
    x_approx = rho_approx * cos(eps_approx)
    
    print("Ignored ellipdoid change y x:", y_approx, x_approx)

def Calc_JTSK_Ignored_Gauss(phi_WGS, la_WGS):
    la_Ferro = la_WGS + (17 + 2/3) * pi / 180
    # We skip the ellipsoid-to-sphere (Gauss projection) math entirely
    u = phi_WGS
    v = la_Ferro

    #Cartographic pole
    uk = (59+(42/60)+(42.6969/3600))*(pi/180)
    vk = (42+(31/60)+(31.41725/3600))*(pi/180)

    #Use your existing uvTosd function
    s_no_gauss, d_no_gauss = uvTosd(u, v, uk, vk)

    #Use Krovak LCC with spherical radius R 
    R = 6380703.6105 
    s0 = 78.5 * pi/180
    c_const = sin(s0)
    rho0 = R * (1/tan(s0)) * 0.9999
    
    rho_no_gauss = rho0 * ((tan(s0/2+pi/4))/(tan(s_no_gauss/2+pi/4)))**c_const
    eps_no_gauss = c_const * d_no_gauss

    y_no_gauss = rho_no_gauss * sin(eps_no_gauss)
    x_no_gauss = rho_no_gauss * cos(eps_no_gauss)

    print("Gauss ignored y x:",y_no_gauss, x_no_gauss)
 
#Input coordinates
phi_WGS = 50.065294 * pi/180
la_WGS = 14.410046 * pi/180

WGSToJTSK (phi_WGS, la_WGS)
Ignore_Ellipsoid_Change(phi_WGS, la_WGS)
Calc_JTSK_Ignored_Gauss(phi_WGS, la_WGS)
