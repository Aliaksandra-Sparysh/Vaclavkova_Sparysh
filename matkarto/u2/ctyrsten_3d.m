clear; clc; close all;

% 1. TETRAHEDRON DEFINITION
v1 = [0, 0, 1];
v2 = [2*sqrt(2)/3, 0, -1/3];
v3 = [-sqrt(2)/3, sqrt(6)/3, -1/3];
v4 = [-sqrt(2)/3, -sqrt(6)/3, -1/3];
V = [v1; v2; v3; v4];
F = [1 2 3; 1 3 4; 1 4 2; 2 4 3];

N = zeros(4, 3); d = zeros(4, 1);
for i = 1:4
    center = (V(F(i,1),:) + V(F(i,2),:) + V(F(i,3),:)) / 3;
    N(i,:) = center / norm(center);  
    d(i) = dot(N(i,:), V(F(i,1),:)); 
end

% 2.LOAD CONTINENTS FROM TXT FILES
cont_files = {'eur.txt', 'amer.txt', 'austr.txt', 'anta.txt'};
cont_points = [];
for f = 1:length(cont_files)
    if exist(cont_files{f}, 'file')
        data = load(cont_files{f});
        [x, y, z] = sph2cart(deg2rad(data(:,2)), deg2rad(data(:,1)), 1);
        cont_points = [cont_points; x, y, z; NaN, NaN, NaN];
    end
end

% 3. GENERATE GRATICULE
grid_points = [];
step = 15; 
for lat_val = -90+step : step : 90-step
    lon_vals = linspace(-180, 180, 150);
    [x, y, z] = sph2cart(deg2rad(lon_vals), deg2rad(lat_val * ones(size(lon_vals))), 1);
    grid_points = [grid_points; x', y', z'; NaN, NaN, NaN];
end
for lon_val = -180 : step : 180-step
    lat_vals = linspace(-90, 90, 150);
    [x, y, z] = sph2cart(deg2rad(lon_val * ones(size(lat_vals))), deg2rad(lat_vals), 1);
    grid_points = [grid_points; x', y', z'; NaN, NaN, NaN];
end

% 4. PROJECTION
proj_cont = project_to_polyhedron(cont_points, N, d);
proj_grid = project_to_polyhedron(grid_points, N, d);

% 5. PLOTTING
figure('Color', 'w', 'Name', 'Neprůhledný polyedrický globus'); 
hold on; axis equal; view(3);

% A. FILLED FACES
% FaceAlpha', 0.9 makes the surface almost opaque
patch('Faces', F, 'Vertices', V, ...
      'FaceColor', [1 1 1], ...
      'FaceAlpha', 0.9, ...
      'EdgeColor', 'none');

% B. GRATICULE - Green
% A small offset of 0.001 prevents flickering due to overlap with the surface
plot3(proj_grid(:,1)*1.001, proj_grid(:,2)*1.001, proj_grid(:,3)*1.001, ...
      'Color', [0.2 0.8 0.2], 'LineWidth', 0.5);

% C. CONTINENTS - Pink
plot3(proj_cont(:,1)*1.002, proj_cont(:,2)*1.002, proj_cont(:,3)*1.002, ...
      'Color', [1 0.07 0.65], 'LineWidth', 1.5);

% D. TETRAHEDRON EDGES
for i = 1:4
    pts = V(F(i,[1 2 3 1]), :); 
    plot3(pts(:,1)*1.003, pts(:,2)*1.003, pts(:,3)*1.003, 'k-', 'LineWidth', 1);
end

camlight; lighting gouraud;

axis([-1.5 1.5 -1.5 1.5 -1.5 1.5]);
axis off;
rotate3d on;

% FUNCTION
function proj_points = project_to_polyhedron(points, N, d)
    if isempty(points), proj_points = []; return; end
    proj_points = NaN(size(points)); 
    for i = 1:size(points, 1)
        if isnan(points(i,1)), continue; end
        p = points(i, :)'; 
        dots = N * p;
        [~, idx] = max(dots);
        t = d(idx) / (N(idx,:) * p);
        proj_points(i, :) = (t * p)';
    end
end