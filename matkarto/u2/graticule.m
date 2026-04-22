function [XM, YM, XP, YP] = graticule(u1, u2, v1, v2, Du, Dv, du, dv, R, fproj, uk, vk)
%Create a graticule of meridians and parallels

%Parallels
XP = []; YP = [];
for u = u1:Du:u2
    %Create points on a parallel
    vp = v1:dv:v2;
    up = u * ones(1, length(vp));
    
    %Transform to oblique aspect
    [sp, dp] = uvtosd(up, vp, uk, vk); 
    
    %Projection
    [xp, yp] = fproj(R, sp, dp, 0);
    
    %Store row
    XP = [XP; xp];
    YP = [YP; yp];
end

%Meridians 
XM = []; YM = [];
for v = v1:Dv:v2
    %Create points on a meridian
    um = u1:du:u2;
    vm = v * ones(1, length(um));
    
    %Transform to oblique aspect
    [sm, dm] = uvtosd(um, vm, uk, vk);
    
    %Projection
    [xm, ym] = fproj(R, sm, dm, 0);
    
    %Store row
    XM = [XM; xm];
    YM = [YM; ym];
end

end