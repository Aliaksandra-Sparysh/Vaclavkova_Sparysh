from math import *
# Optimal LCC projection
R = 1

#Pole
uk = 38.9682253 * pi/180
vk = 25.6855252 * pi/180 

#Northernmost point
u1 = 56.1734200 *pi/180
v1 = 28.1382440 *pi/180

#Southernmost point
u2 = 51.4688578 *pi/180
v2 = 27.7471415 *pi/180

#Transformation to the oblique aspect
s1 = asin(sin(u1) * sin(uk) + cos(u1) * cos(uk) * cos(vk-v1))
s2 = asin(sin(u2) * sin(uk) + cos(u2) * cos(uk) * cos(vk-v2))

#Constant c of the conic projection
cn = log10(cos(s1)) - log10(cos(s2))
cd = log10(tan(s2/2+pi/4))-log10(tan(s1/2+pi/4))
c = cn / cd

#Compute s0
s0 = asin(c)

#Compute rho0: radius of the parallel (u = u0)
rho0_n = 2*R*cos(s0)*cos(s1)*(tan(s1/2+pi/4))**c
rho0_d = c*(cos(s0)*(tan(s0/2+pi/4))**c+cos(s1)*(tan(s1/2+pi/4))**c)
rho0 = rho0_n/rho0_d

#Compute rho1: radius of the north parallel (u = u1)
rho1 = rho0*((tan(s0/2+pi/4))/(tan(s1/2+pi/4)))**c

#Compute rho2: radius of the south parallel (u = u2)
rho2 = rho0*((tan(s0/2+pi/4))/(tan(s2/2+pi/4)))**c

#Scales
m1 = (c * rho1)/(R * cos(s1))
m2 = (c * rho2)/(R * cos(s2))
m0 = (c * rho0)/(R * cos(s0))

ny1 = (m1 -1) * 1000
ny2 = (m2 -1) * 1000
ny0 = (m0 - 1) * 1000

print(ny1, ny2, ny0)