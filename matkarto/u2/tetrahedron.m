clc
clear
close all

%Input parameters 
R = 1;      
fproj = @gnom;
u0 = 0;

%Graticule step in radians
Du = 10 * pi/180;
Dv = 10 * pi/180;
du = 5 * pi/180;
dv = 5 * pi/180;

%Tetrahedron angle in radians
ur = 19.4712 * pi/180;
urj = -ur;

figure('Color', 'w', 'Name', 'Tetrahedron');

%Face 1
uk = ur; vk = 60 * pi/180;
ub = [urj, urj, 90 * pi/180];
vb = [0, 120, 0] * pi/180;
u1 = -40 * pi/180; 
u2 = 90 * pi/180; 
v1 = -10 * pi/180; 
v2 = 130 * pi/180;

subplot(2, 2, 1);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 1');

%Face 2
uk = ur; vk = 180 * pi/180;
ub = [urj, urj, 90 * pi/180];
vb = [120, 240, 0] * pi/180;
u1 = -40 * pi/180; 
u2 = 90 * pi/180; 
v1 = 110 * pi/180; 
v2 = 250 * pi/180;

subplot(2, 2, 2);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 2');

%Face 3
uk = ur; vk = 300 * pi/180;
ub = [urj, urj, 90 * pi/180];
vb = [240, 360, 0] * pi/180;
u1 = -40 * pi/180; 
u2 = 90 * pi/180; 
v1 = 230 * pi/180; 
v2 = 370 * pi/180;

subplot(2, 2, 3);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 3');

%Face 4
uk = -90 * pi/180; vk = 0;
ub = [urj, urj, urj];
vb = [0, 120, 240] * pi/180;
u1 = -90 * pi/180; 
u2 = -15 * pi/180; 
v1 = -180 * pi/180; 
v2 = 180 * pi/180;

subplot(2, 2, 4);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 4 (South)');

