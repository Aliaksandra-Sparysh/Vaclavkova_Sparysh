function [] = drawContinents(continent, R, uk, vk, fproj, u0)
% Draw continents
% R: sphere radius
% uk, vk: face center

% Load data (files are stored in degrees)
try
    con = load(continent);
catch
    return; % If the file does not exist, exit the function
end
u_con = con(:,1) * pi / 180;
v_con = con(:,2) * pi / 180;
[s_con, d_con] = uvtosd(u_con, v_con, uk, vk);

% clipping - gnomonic projection cannot display points beyond the horizon
idx = find(s_con > 0.3);
if ~isempty(idx)
    % Compute planar coordinates
    [xc_con, yc_con] = fproj(R, s_con(idx), d_con(idx), u0);
    
    % Plot continent
    plot(xc_con, yc_con, 'Color', [1, 0.4, 0.8], 'LineWidth', 1.5); %ZMĚNĚNA BARVA
end
end