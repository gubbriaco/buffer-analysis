# BUFFER ANALYSIS
[Analysis of an Inverter Chain (Buffer) using a Jupyter notebook from which, via API calls to LTspice, it is possible to set the sizing factor of the inverters using the Monte Carlo method. Therefore, the Optimal Pareto Curve is analyzed through an optimization process and compared to the Monte Carlo experiments.]

## Description
[The initial part of the project involved the design of a 3-stage inverter chain (buffer): the first stage composed of an inverter of minimum dimensions, the second and third stages composed of an inverter each and respectively sized S1 and S2 times the minimum inverter. Specifically, these sizing parameters were obtained by considering the Monte Carlo method so as to allow us to obtain a certain randomness during the N_RUNS simulations conducted. At the output of the buffer, a load was considered represented by an inverter sized S_Load times the minimum inverter. Specifically, the behavior of the buffer was analyzed considering a certain V_IN voltage, of the pulse type having certain parameters, a V_Supply voltage for the 3 inverter stages and a V_Supply_L for the load inverter. After carrying out simulations regarding the circuit in question, the energy associated with the inverter chain was calculated considering the two possible transitions: 0->1 (from 13 ns to 18 ns) and 1->0 (from 18 ns to 22 ns). Furthermore, the rise and fall delays were calculated considering respectively rising and falling edges of the signal. It must be specified that the minimum isolated inverter was considered in the analyzes so as to be able to calculate the total capacity (connecting the minimum inverter from the load), the intrinsic output capacity (disconnecting the minimum inverter from the load) and, finally, the capacity input (minimum) obtained as the difference between the two just mentioned. Therefore, after calculating the characteristic parameters of the buffer, such as gamma_e, gamma_d, tau_nom and c_min, it was possible to move on to the next phase of the project: the optimization of the dimensioning factors S1 and S2 of the circuit. Specifically, considering a non-linear optimization algorithm and taking into account an objective function represented by the energy model of an inverter chain, and equality and inequality constraints obtained from the delay model, it was possible to obtain excellent values considering a delay range between d_max and d_min in steps of 10. Subsequently, the optimal values, obtained from the algorithm just mentioned, were used within the schematic buffer_optimized to simulate the inverter chain circuit again and obtain the delay and energy parameters . Therefore, finally, it was possible to carry out a comparative analysis between the experiments conducted during the initial part of the project, obtained through the Monte Carlo method, and the optimal Pareto curve, obtained through the circuit optimization and simulation process.]

## Index
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Params](#params)

## Requirements
- [LTspice](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html)
- [Support for running Jupyter Notebooks](https://jupyter.org/)

## Installation
- Clone the repository: `https://github.com/gubbriaco/buffer-analysis.git`

## Usage
1. Open .raw files in LTspice
2. Open Jupyter Notebook
3. Run the Jupyter Notebook

## Params
- ### Buffer
  - #### energy
    - energy_connected_buffer `keep the entire circuit connected and carry out the measurements taking into account v(supply) and i(Vsupply) between 13 ns and 22 ns`
  - #### delay
    - ##### rise
      - rise_delay_connected_buffer `keep the entire circuit connected and carry out the measurements taking into account v(IN) and V(OUT)`
    - ##### fall
      - fall_delay_connected_buffer `keep the entire circuit connected and carry out the measurements taking into account v(IN) and V(OUT)`

- ### Minimum Inverter
  - #### energy
    - energy_connected_minimum_inverter `keep the entire circuit connected and carry out the measurements taking into account v(supply) and i(Vsupply) between 18 ns and 22 ns`
    - energy_disconnected_minimum_inverter `disconnect the circuit at the OUT connection and carry out the measurements taking into account v(supply) and i(Vsupply) between 18 ns and 22 ns`
  - #### delay
    - ##### rise
      - rise_delay_disconnected_minimum_inverter `disconnect the circuit at the OUT connection and carry out the measurements taking into account v(IN) and v(OUT)`
      - rise_delay_connected_minimum_inverter `keep the entire circuit connected and carry out the measurements taking into account v(IN) and V(OUT)`
    - ##### fall
      - fall_delay_disconnected_minimum_inverter `disconnect the circuit at the OUT connection and carry out the measurements taking into account v(IN) and v(OUT)`
      - fall_delay_connected_minimum_inverter `keep the entire circuit connected and carry out the measurements taking into account v(IN) and V(OUT)`
