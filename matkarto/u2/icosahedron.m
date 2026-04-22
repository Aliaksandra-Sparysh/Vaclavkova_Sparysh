clc; clear; close all;
%The original manual approach for defining all 20 faces was failing. 
% AI assistance was used to troubleshoot the execution errors and refactor 
%the code using 'for' loops, which successfully fixed the bugs and optimized the script.
%Input parameters
R = 1;
fproj = @gnom; 
phi_v = atan(0.5); 
uk_polar = 52.6226 * pi/180;
uk_equat = 10.8123 * pi/180;
Du = 10 * pi/180; 
Dv = 10 * pi/180;
du = 2 * pi/180;  
dv = 2 * pi/180;

figure('Color', 'w', 'Units', 'normalized', 'Position', [0.1 0.1 0.8 0.8]);

%Northern faces
for i = 1:5
    vk_deg = (i-1) * 72; 
    uk = uk_polar;
    vk = vk_deg * pi/180;
    ub = [90, 26.5651, 26.5651] * pi/180;
    vb = [vk_deg, vk_deg-36, vk_deg+36] * pi/180;
    u1 = 10 * pi/180; u2 = 90 * pi/180;
    v1 = floor((vk_deg-60)/10) * 10 * pi/180; 
    v2 = ceil((vk_deg+60)/10) * 10 * pi/180;
    
    subplot(4, 5, i);
    createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
    title(sprintf('N%d', i)); % N jako North
end

%Equatorial faces
for i = 1:10
    vk_deg = (i-1) * 36;
    vk = vk_deg * pi/180;
    
    if mod(i,2) == 1
        uk = uk_equat;
        ub = [26.5651, 26.5651, -26.5651] * pi/180;
        vb = [vk_deg-36, vk_deg+36, vk_deg] * pi/180;
    else
        uk = -uk_equat;
        ub = [-26.5651, -26.5651, 26.5651] * pi/180;
        vb = [vk_deg-36, vk_deg+36, vk_deg] * pi/180;
    end
    
    u1 = -50 * pi/180; u2 = 50 * pi/180;
    v1 = floor((vk_deg-60)/10) * 10 * pi/180; 
    v2 = ceil((vk_deg+60)/10) * 10 * pi/180;
    
    subplot(4, 5, i+5);
    createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
    title(sprintf('E%d', i)); 
end

%Southern faces
for i = 1:5
    vk_deg = (i-1) * 72 + 36; 
    uk = -uk_polar;
    vk = vk_deg * pi/180;
    ub = [-90, -26.5651, -26.5651] * pi/180;
    vb = [vk_deg, vk_deg-36, vk_deg+36] * pi/180;
    u1 = -90 * pi/180; u2 = -10 * pi/180;
    v1 = floor((vk_deg-60)/10) * 10 * pi/180; 
    v2 = ceil((vk_deg+60)/10) * 10 * pi/180;
    
    subplot(4, 5, i+15);
    createGlobeFace(ub, vb, u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk);
    title(sprintf('S%d', i)); 
end