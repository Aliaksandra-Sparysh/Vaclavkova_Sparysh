clc
clear
format long

syms R u v

%Gnomonic projection
x = R*tan(pi/2-u)*cos(v);
y = R*tan(pi/2-u)*sin(v);

%Partial derivatives
fu = simplify(diff(x,u), 'Steps', 20);
fv = simplify(diff(x,v), 'Steps', 20);
gu = simplify(diff(y,u), 'Steps', 20);
gv = simplify(diff(y,v), 'Steps', 20);

%Scale factors
mp2 = simplify((fu*fu + gu*gu)/(R*R), 'Steps', 20);
mr2 = simplify((fv*fv + gv*gv)/(R*R*cos(u)*cos(u)), 'Steps', 20);
mr = simplify(sqrt(mr2), 'Steps', 20);
mp = simplify(sqrt(mp2), 'Steps', 20);
p = 2*(fu*fv + gu*gv);

P1 = simplify((gu*fv - fu*gv)/(R^2*cos(u)), 'Steps', 20);
P2 = simplify(mp * mr, 'Steps', 50);
d_omega = simplify(2*asin(abs(mr-mp)/(mr+mp)), 'Steps', 50);
omega_ = simplify(atan2(gu*fv-gv*fu, fu*fv+gu*gv), 'Steps', 50);

% Point on the face boundary
un = -19.4712;
vn = 0;

%Convert (u,v) to (s,d)
uk = -90; vk = 0;
[snd, dnd] = uv_to_sd(un, vn, uk, vk);
sn = snd * pi / 180;
dn = dnd * pi / 180;

%Substitution
Rn = 6380*1000/1000000;
xn = double(subs(x, {R, u, v}, {Rn, sn, dn}));
yn = -double(subs(y, {R, u, v}, {Rn, sn, dn}));

%Partial derivatives after substitution
fun = double(subs(fu, {R, u, v}, {Rn, sn, dn}));
fvn = double(subs(fv, {R, u, v}, {Rn, sn, dn}));
gun = double(subs(gu, {R, u, v}, {Rn, sn, dn}));
gvn = double(subs(gv, {R, u, v}, {Rn, sn, dn}));

%Local linear scales
mpn = double(subs(mp, {R, u, v}, {Rn, sn, dn}));
mrn = double(subs(mr, {R, u, v}, {Rn, sn, dn}));
pn = double(subs(p, {R, u, v}, {Rn, sn, dn}));

%Area scale
Pn = double(subs(P1, {R, u, v}, {Rn, sn, dn}));
Pn1 = double(subs(P2, {R, u, v}, {Rn, sn, dn}));

%Directions
sigma_p = dn;
sigma_r = sn - pi/2;

%Maximum angular distortion
d_omegan = double(subs(d_omega, {R, u, v}, {Rn, sn, dn})) * 180/pi;

%omega
omega_n = atan((gun*fvn-gvn*fun)/(fun*fvn+gun*gvn)) * 180/pi;

% Meridian convergence
c_n = abs(sigma_p + pi/2)/pi * 180;

% Create and plot graticule
hold on
fproj = @gnom;
Du = 10; Dv = 10;
du = 1; dv = 1;
u1 = -90; u2 = -10;
v1 = -180; v2 = 180;

[XM,YM,XP,YP] = my_graticule(u1,u2,v1,v2,Du,Dv,du,dv,Rn,fproj,uk,vk);
plot(XM', YM', 'k');
plot(XP', YP', 'k');

% Ellipse
t = 0:pi/10:2*pi;
xe = mpn*cos(t);
ye = mrn*sin(t);
E = [xe; ye];

% Rotation matrix
ROT = [cos(sigma_p) -sin(sigma_p); sin(sigma_p) cos(sigma_p)];

% Rotated ellipse
ER = ROT*E; 

% Shifted and rotated ellipse
plot(ER(1, :) + xn, ER(2, :) + yn, 'r');

axis equal