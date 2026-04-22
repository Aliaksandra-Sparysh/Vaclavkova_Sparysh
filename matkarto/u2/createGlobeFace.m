function [] = createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk)
%Draw one polyhedron face (graticule, continents, boundary)

axis equal
hold on

%Create graticule
[XM, YM, XP, YP] = graticule(u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
plot(XM', YM', 'k-', 'LineWidth', 0.05); 
plot(XP', YP', 'k-', 'LineWidth', 0.05);

%Draw continents
drawContinents('eur.txt',   R, uk, vk, fproj, 0);
drawContinents('amer.txt',  R, uk, vk, fproj, 0);
drawContinents('austr.txt', R, uk, vk, fproj, 0);
drawContinents('anta.txt',  R, uk, vk, fproj, 0);

%Face boundary
[sb, db] = uvtosd(ub, vb, uk, vk);
[xb, yb] = fproj(R, sb, db, 0);
xb_l = [xb, xb(1)];
yb_l = [yb, yb(1)];

plot(xb_l, yb_l, 'm', 'LineWidth', 1);

%Display limits
c_lim = 2.5 * R; 
xlim([-c_lim, c_lim]); 
ylim([-c_lim, c_lim]);
end