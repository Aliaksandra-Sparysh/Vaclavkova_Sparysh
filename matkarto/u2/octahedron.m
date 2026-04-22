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

%Octahedron angle in radians
ur = 35.2644 * pi/180;
urj = -ur;

figure('Color', 'w', 'Name', 'Octahedron');

%UPPER HEMISPHERE
%Face 1
uk = ur; 
vk = 45 * pi/180;
ub = [0, 0, 90 * pi/180]; 
vb = [0, 90 * pi/180, 0];
u1 = -10 * pi/180; 
u2 = 90 * pi/180; 
v1 = -10 * pi/180; 
v2 = 100 * pi/180;
subplot(2, 4, 1);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 1');

% Face 2
uk = ur; 
vk = 135 * pi/180;
ub = [0, 0, 90*pi/180]; 
vb = [90 * pi/180, 180 * pi/180, 0];
u1 = -10 * pi/180; u2 = 90 * pi/180; 
v1 = 80 * pi/180; v2 = 190 * pi/180;
subplot(2, 4, 2);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 2');

%Face 3
uk = ur; 
vk = 225 * pi/180;
ub = [0, 0, 90 * pi/180]; 
vb = [180 * pi/180, 270 * pi/180, 0];
u1 = -10 * pi/180; 
u2 = 90 * pi/180; 
v1 = 170 * pi/180; 
v2 = 280 * pi/180;
subplot(2, 4, 3);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 3');

%Face 4
uk = ur; vk = 315 * pi/180;
ub = [0, 0, 90*pi/180]; vb = [270*pi/180, 360*pi/180, 0];
u1 = -10*pi/180; u2 = 90*pi/180; v1 = 260*pi/180; v2 = 370*pi/180;
subplot(2, 4, 4);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 4');

%LOWER HEMISPHERE
%Face 5
uk = urj; 
vk = 45 * pi/180;
ub = [0, 0, -90 * pi/180]; 
vb = [0, 90 * pi/180, 0];
u1 = -90 * pi/180; 
u2 = 10 * pi/180; 
v1 = -10 * pi/180; 
v2 = 100 * pi/180;
subplot(2, 4, 5);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 5');

%Face 6
uk = urj; 
vk = 135 * pi/180;
ub = [0, 0, -90 * pi/180]; 
vb = [90 * pi/180, 180 * pi/180, 0];
u1 = -90 * pi/180; 
u2 = 10 * pi/180; 
v1 = 80 * pi/180; 
v2 = 190 * pi/180;
subplot(2, 4, 6);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 6');

%Face 7
uk = urj; vk = 225 * pi/180;
ub = [0, 0, -90 * pi/180]; 
vb = [180 * pi/180, 270 * pi/180, 0];
u1 = -90 * pi/180; 
u2 = 10 * pi/180; 
v1 = 170 * pi/180; 
v2 = 280 * pi/180;
subplot(2, 4, 7);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 7');

%Face 8
uk = urj; 
vk = 315 * pi/180;
ub = [0, 0, -90 * pi/180]; 
vb = [270 * pi/180, 360 * pi/180, 0];
u1 = -90 * pi/180; 
u2 = 10 * pi/180; 
v1 = 260 * pi/180; 
v2 = 370 * pi/180;
subplot(2, 4, 8);
createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
title('Face 8');



