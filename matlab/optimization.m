clear; close all; clc;

addpath src
import energy_model.*;
import dealy_constraints.*;

%% buffer_data variables from python
buffer_data_file_path = "buffer_data.txt";
fileID = fopen(buffer_data_file_path, 'r');

data = fscanf(fileID, '%f');
fclose(fileID);


vdd = data(1);
c_min = data(2);
gamma_e = data(3);
tau_nom = data(4);
gamma_d = data(5);
s_load = data(6);
s0 = [data(7) data(8)];
d_max = data(9);
d_min = data(10);
step = 10;

%% start point
step_range = ((d_max-d_min)/step)+1;
delay_range = d_max : -step : d_min;

%% optimization algorithm options
options = optimoptions('fmincon', ...
                                  'Display', 'off', ...
                                  'MaxIterations', 1000, ...
                                  'MaxFunctionEvaluations', 10000, ...
                                  'StepTolerance', 0.01, ...
                                  'OptimalityTolerance', 0.1, ...
                                  'ConstraintTolerance', 1, ...
                                  'ObjectiveLimit', -1e20);

%% formatting optimal values generated
fprintf('%-15s %-15s %-15s %-15s\n', 'delay_step', 's1', 's2', 'optimal_energy');

%% sizing factor arrays
s1 = [];
s2 = [];

%% optimization algorithm
for d = delay_range
    [optimal_s, optimal_energy] = fmincon( ...
                                           @(s) energy_model(s, vdd, c_min, s_load, gamma_e), ...
                                           s0, ...
                                           [], ...
                                           [], ...
                                           [], ...
                                           [], ...
                                           [0, 0], ...
                                           [], ...
                                           @(s) delay_constraints(s, d, tau_nom, s_load, gamma_d), ...
                                           options ...
                                       );
    s1 = [s1 ; optimal_s(1)];
    s2 = [s2 ; optimal_s(2)];
    fprintf('%-15d %-15.4f %-15.4f %-15.4f\n', d, optimal_s(1), optimal_s(2), optimal_energy);
end
figure;
plot(s1), hold on, plot(s2);
plot(s1, '.'), hold on, plot(s2, '.');
legend('s1', 's2', 's1-value', 's2-value', 'Location', 'northwest');

%% clear files
s1_data = 'data/s1_data.txt';
s2_data = 'data/s2_data.txt';

fileID_s1 = fopen(s1_data, 'w');
fileID_s2 = fopen(s2_data, 'w');

if or(fileID_s1 == -1, fileID_s2 == -1)
    error('Impossibile aprire il file s1_data e/o s2_data');
else
    fclose(fileID_s1);
    fclose(fileID_s2);
end


%% write optimal values
fileID_s1 = fopen(s1_data, 'a');
fileID_s2 = fopen(s2_data, 'a');

if or(fileID_s1 == -1, fileID_s2 == -1)
    error('Impossibile aprire il file s1_data e/o s2_data');
else
    fprintf(fileID_s1, '%d\n', s1);
    fprintf(fileID_s2, '%d\n', s2);
    fclose(fileID_s1);
    fclose(fileID_s2);
end
