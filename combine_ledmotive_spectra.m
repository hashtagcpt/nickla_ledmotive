wavelength = csvread('lambda.csv');
l1 = csvread('l1_spect_ledmotive.csv');
l2 = csvread('l2_spect_ledmotive.csv');
l3 = csvread('l3_spect_ledmotive.csv');
l4 = csvread('l4_spect_ledmotive.csv');
l5 = csvread('l5_spect_ledmotive.csv');
l6 = csvread('l6_spect_ledmotive.csv');
l7 = csvread('l7_spect_ledmotive.csv');

spects = [wavelength', l1, l2, l3, l4, l5, l6, l7];

plot(spects(:,2)); hold on;
plot(spects(:,3))
plot(spects(:,4))
plot(spects(:,5))
plot(spects(:,6))
plot(spects(:,7))
plot(spects(:,8))