clear; clc; close all;

% 1. CUBE DEFINITION)
% Normalized coordinates are used so that all vertices lie on the sphere
r = 1/sqrt(3); 
V = [
    -1 -1 -1;  1 -1 -1;  1  1 -1; -1  1 -1; % Bottom face (1-4)
    -1 -1  1;  1 -1  1;  1  1  1; -1  1  1  % Top face (5-8)
] * r;

% Definition of the 6 faces (each face has 4 vertices)
F = [
    1 2 6 5; % front
    2 3 7 6; % right
    3 4 8 7; % back
    4 1 5 8; % left
    5 6 7 8; % top
    1 2 3 4  % bottom
];

% Compute face normals and distances for the 6 faces
N = zeros(6, 3); d = zeros(6, 1);
for i = 1:6
    center = mean(V(F(i,:), :));
    N(i,:) = center / norm(center);  
    d(i) = dot(N(i,:), V(F(i,1), :)); 
end

% 2. LOAD CONTINENTS FROM TXT FILES
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
    lon_vals = linspace(-180, 180, 200);
    [x, y, z] = sph2cart(deg2rad(lon_vals), deg2rad(lat_val * ones(size(lon_vals))), 1);
    grid_points = [grid_points; x', y', z'; NaN, NaN, NaN];
end
for lon_val = -180 : step : 180-step
    lat_vals = linspace(-90, 90, 200);
    [x, y, z] = sph2cart(deg2rad(lon_val * ones(size(lat_vals))), deg2rad(lat_vals), 1);
    grid_points = [grid_points; x', y', z'; NaN, NaN, NaN];
end

% 4. PROJECTION ONTO 6 FACES
proj_cont = project_to_polyhedron(cont_points, N, d);
proj_grid = project_to_polyhedron(grid_points, N, d);

% 5. PLOTTING
figure('Color', 'w', 'Name', 'Polyedrický globus - Krychle'); 
hold on; axis equal; view(3);

% A. FACES
patch('Faces', F, 'Vertices', V, 'FaceColor', [1 1 1], 'FaceAlpha', 0.95, 'EdgeColor', 'k', 'LineWidth', 0.5);

% B. GRATICULE
plot3(proj_grid(:,1)*1.001, proj_grid(:,2)*1.001, proj_grid(:,3)*1.001, 'Color', [0.2 0.8 0.2], 'LineWidth', 0.5);

% C. CONTINENTS
plot3(proj_cont(:,1)*1.002, proj_cont(:,2)*1.002, proj_cont(:,3)*1.002, 'Color', [1 0.07 0.65], 'LineWidth', 1.5);

% D. CUBE EDGES
for i = 1:6
    pts = V(F(i,[1 2 3 4 1]), :); 
    plot3(pts(:,1)*1.003, pts(:,2)*1.003, pts(:,3)*1.003, 'k-', 'LineWidth', 1);
end

camlight; lighting gouraud;
axis([-1.2 1.2 -1.2 1.2 -1.2 1.2]);
axis off; rotate3d on;

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