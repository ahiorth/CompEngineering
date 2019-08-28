B = dlmread('jotun2.dat', '\t', 1, 0); % skip 1 first lines
% sort the matrix after the first row
%M = sortrows(B);
dim = size(B);                        % get the size of the matrix 
Days = B(1:dim(1,1),1);               % Year
OilProd = B(1:dim(1,1),2);            % Oil Production
CumOilProd = cumsum(OilProd);

ft = fittype('exp_decline(x,A,D)')
%f=fit(Year-2003, OilProd,'exp1', 'Startpoint', [1e5,-0.3]) 
f1=fit(Days, OilProd,ft, 'Startpoint', [1,0.003]) 
figure
plot(f1,Days,OilProd)

ft = fittype('hyp_decline(x,A,D,b)')
%f=fit(Year-2003, OilProd,'exp1', 'Startpoint', [1e5,-0.3]) 
f2=fit(Days, OilProd,ft, 'Lower', [0,0,0], 'Upper', [Inf,Inf,1], 'Startpoint', [1,0.3,0.5]) 
figure
plot(f2,Days,OilProd)

ft = fittype('harm_decline(x,A,D)')
%f=fit(Year-2003, OilProd,'exp1', 'Startpoint', [1e5,-0.3]) 
f3=fit(Days, OilProd,ft, 'Startpoint', [1,0.3]) 
figure
plot(f3,Days,OilProd)


figure
yyaxis left
title('Jotun Production Profile')
ylabel('MSm^3/year')
plot(f,Days,OilProd, 'b--o')
yyaxis right
ylabel('Cumulativ production [MSm^3]')
plot(Days,CumOilProd, 'r--o')
