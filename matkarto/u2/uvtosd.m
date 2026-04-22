function [s, d] = uvtosd(u, v, uk, vk)
% Transform (u, v) to  coordinates (s, d)

%Difference in longitude
dv = v - vk;

%Compute cartographic latitude
sarg = sin(u).*sin(uk) + cos(u).*cos(uk).*cos(dv);
s = asin(sarg);

%Compute cartographic longitude
num = cos(u).*sin(dv);
denom = cos(u).*sin(uk).*cos(dv) - sin(u).*cos(uk);
d = atan2(num, denom);

end