B = dlmread('jotun.dat', '\t', 3, 0); % skip 3 first lines
% sort the matrix after the first row
M = sortrows(B);
dim = size(M);                        % get the size of the matrix 
Year = M(5:dim(1,1),1);               % Year
OilProd = M(5:dim(1,1),2);            % Oil Production
CumOilProd = cumsum(OilProd);

ft = fittype('exp_decline(x,A,D)')
%f=fit(Year-2003, OilProd,'exp1', 'Startpoint', [1e5,-0.3]) 
f1=fit(Year-2003, OilProd,ft, 'Startpoint', [1,0.3]) 
figure
plot(f1,Year-2003,OilProd)

ft = fittype('hyp_decline(x,A,D,b)')
%f=fit(Year-2003, OilProd,'exp1', 'Startpoint', [1e5,-0.3]) 
f2=fit(Year-2003, OilProd,ft, 'Lower', [0,0,0], 'Upper', [Inf,Inf,1], 'Startpoint', [1,0.3,0.5]) 
figure
plot(f2,Year-2003,OilProd)

ft = fittype('harm_decline(x,A,D)')
%f=fit(Year-2003, OilProd,'exp1', 'Startpoint', [1e5,-0.3]) 
f3=fit(Year-2003, OilProd,ft, 'Startpoint', [1,0.3]) 
figure
plot(f3,Year-2003,OilProd)


figure
yyaxis left
title('Jotun Production Profile')
ylabel('MSm^3/year')
plot(f,Year,OilProd, 'b--o')
yyaxis right
ylabel('Cumulativ production [MSm^3]')
plot(Year,CumOilProd, 'r--o')
