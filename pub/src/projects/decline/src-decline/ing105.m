% read data from file, data separated by tab, skip 0 rows and 1 coloumn
B = dlmread('draugen.txt', '\t', 0, 1);
% get the size of the matrix
dim = size(B);
% Assume 30 days in each month and 365 in year
ProdStart = B(1,1)+B(1,2)*30/365;
% Year now starts at time 0
Year= B(1:dim(1,1),1)+B(1:dim(1,1),2)*30/365-ProdStart;
% oilproduction in third coloumn
OilProd= B(1:dim(1,1),3);
CumOilProd = cumsum(OilProd);
figure
yyaxis left
title('Draugen production profile')
plot(Year,OilProd, 'b--o')
ylabel('MSm^3/month')
xlabel('Years of production')
yyaxis right
plot(Year,CumOilProd, 'r--o')
ylabel('Cumulativ production [MSm^3]')

ft = fittype('exp_decline(x,A,D)') % define fit function
% only choose data from the decline phase
% (i.e. after approx. 8 years for the Draugen case)
T0 = 8;
%extract indexes
ind = Year > T0;
% corresponding X and Y-value
NewY = Year(ind)-T0; %important to start at 0
NewP = OilProd(ind);
f=fit(NewY, NewP,ft, 'Startpoint', [1,100])
% extract parameters
par = coeffvalues(f);
model = exp_decline(NewY,par(1),par(2));
% Investigate the quality of the fit
Imod = cumsum(model)
d=CumOilProd(ind)
figure
h= plot(Year,OilProd, 'b--o',NewY+T0,model)
set(h,{'LineWidth'},{1;3})
ylabel('MSm^3/month')
xlabel('Years of production')
yyaxis right
plot(NewY+T0,Imod+d(1), 'g-o', Year,CumOilProd, 'r-')
ylabel('Cumulativ production [MSm^3]')



