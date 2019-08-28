%skip first coloumn, data are seperated with tabulator
B = dlmread('draugen.txt', '\t', 0, 1);
% get the size of the matrix 
dim = size(B);
% Assume 30 days in each month and 365 in year
ProdStart = B(1,1)+B(1,2)*30/365;      
% Year now starts at time 0
Year       = B(1:dim(1,1),1)+B(1:dim(1,1),2)*30/365-ProdStart; 

OilProd    = B(1:dim(1,1),3);
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
% define function to be fitted
ft = fittype('exp_decline(x,A,D)')
% only choose data from the decline phase (i.e. after approx. 8 years)
T0 = 1.8;
% extract indexes 
ind = Year > T0;
% cooresponding X and Y-value
NewY = Year(ind)-T0; %important to start at 0
NewP = OilProd(ind);
f=fit(NewY, NewP,ft, 'Startpoint', [1,100])
% extract parameters
par = coeffvalues(f);
model = exp_decline(NewY,par(1),par(2));
% Investigate the quality of the fit
figure
plot(Year,OilProd,NewY+T0,model)
title('Draugen production profile')
ylabel('MSm^3/month')
xlabel('Years of production')

ft = fittype('hyp_decline(x,A,D,b)')
f2=fit(NewY, NewP,ft, 'Lower', [0,0,0], 'Upper', [Inf,Inf,1], 'Startpoint', [1,100,0.5])
par = coeffvalues(f2);
model = hyp_decline(NewY,par(1),par(2),par(3));
figure
plot(Year,OilProd,NewY+T0,model)
title('Jotun production profile')
ylabel('MSm^3/year')
xlabel('Years of production')