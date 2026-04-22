function [x, y] = gnom(R, s, d, ~)
% Gnomonic projection
% Inputs R, s, d are in radians, the fourth parameter is ignored (~).

% Distance from the projection center
% s is the latitude, pi/2 - s is the angular distance from the center
r = R * tan(pi/2 - s);

% Compute planar coordinates
x = r .* cos(d);
y = r .* sin(d);

end