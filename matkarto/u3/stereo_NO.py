from math import *

# Optimal stereographic projection - Norway
R = 1

#Pole
uk = 64.9646739 * pi/180
vk = 18.7974046 * pi/180

#Edge point
u1 = 58.0683207 *pi/180
v1 = 6.6273357 *pi/180

# Transformation to oblique aspect
sj = asin(sin(u1) * sin(uk) + cos(u1) * cos(uk) * cos(vk-v1))

# psi = 90° - sj
psi_j = pi/2 - sj

# Multiplication constant
mu = (2 * cos(psi_j/2)**2) / (1 + cos(psi_j/2)**2)

# Scales
m_edge = mu / cos(psi_j/2)**2
m_center = mu

# Distortions in per mille
ny_edge = (m_edge - 1) * 1000
ny_center = (m_center - 1) * 1000

print(ny_edge, ny_center)