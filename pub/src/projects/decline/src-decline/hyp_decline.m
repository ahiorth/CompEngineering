% Define hyperbolic decline function
function y = hyp_decline(x,A,D,b)
y=A*(1+b*D*x).^(-1/b);
end
