import os
import re
import matplotlib.pyplot as plt
from PyLTSpice import SimRunner
from models.ops import load_asc, load_ltr, rise_delay_connected, fall_delay_connected, save_image, table_creation
from properties import l_min_pmos, l_min_nmos, w_min_nmos, tran, rit_models, w_min_pmos_step_param, \
    save_w_min_pmos_analysis
from utils.conversion import to_order, Order
from utils.paths import ltspice, images, data
from utils.patterns import rise_delay_connected_pattern, fall_delay_connected_pattern, w_min_pmos_analysis_pattern


def minimum_inverter_sizing_analysis():
    minimum_inverter_sizing_analysis_netlist = load_asc(
        asc_file_path=os.path.join(ltspice, "minimum-inverter/get_sizing/minimum_inverter_sizing_analysis.asc"),
        schematic_image_path=os.path.join(images, "minimum_inverter_sizing_analysis.png")
    )
    minimum_inverter_sizing_analysis_netlist.set_parameter('l_min_pmos', l_min_pmos)
    minimum_inverter_sizing_analysis_netlist.set_parameter('l_min_nmos', l_min_nmos)
    minimum_inverter_sizing_analysis_netlist.set_parameter('w_min_nmos', w_min_nmos)
    minimum_inverter_sizing_analysis_netlist.add_instructions(
        rit_models,
        tran,
        w_min_pmos_step_param,
        save_w_min_pmos_analysis,
        rise_delay_connected(),
        fall_delay_connected()
    )
    minimum_inverter_sizing_analysis_runner = SimRunner(output_folder=f"{data}/in/minimum-inverter/get_sizing/")
    minimum_inverter_sizing_analysis_runner.run(netlist=minimum_inverter_sizing_analysis_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(minimum_inverter_sizing_analysis_runner.okSim) + '/' + str(
        minimum_inverter_sizing_analysis_runner.runno))

    minimum_inverter_sizing_analysis_raw = ""
    minimum_inverter_sizing_analysis_log = ""
    for minimum_inverter_sizing_analysis_raw, minimum_inverter_sizing_analysis_log in minimum_inverter_sizing_analysis_runner:
        print(
            "Raw file: %s, Log file: %s" % (minimum_inverter_sizing_analysis_raw, minimum_inverter_sizing_analysis_log))

    minimum_inverter_sizing_analysis_ltr = load_ltr(raw_file_path=minimum_inverter_sizing_analysis_raw)
    v_in_minimum_inverter_sizing_analysis = minimum_inverter_sizing_analysis_ltr.get_trace("V(in)")
    v_out_minimum_inverter_sizing_analysis = minimum_inverter_sizing_analysis_ltr.get_trace("V(out)")
    v_supply_minimum_inverter_sizing_analysis = minimum_inverter_sizing_analysis_ltr.get_trace("V(supply)")
    time = minimum_inverter_sizing_analysis_ltr.get_trace('time')
    steps = minimum_inverter_sizing_analysis_ltr.get_steps()

    plt.figure(figsize=(16, 4))
    for step in range(len(steps)):
        plt.plot(time.get_wave(step), v_in_minimum_inverter_sizing_analysis.get_wave(step), label=steps[step],
                 color='blue')
        plt.plot(time.get_wave(step), v_out_minimum_inverter_sizing_analysis.get_wave(step), label=steps[step],
                 color='red')
        plt.plot(time.get_wave(step), v_supply_minimum_inverter_sizing_analysis.get_wave(step), label=steps[step],
                 color='green')
    plt.legend(["V(in)", "V(out)", "V(supply)"])
    save_image(image_path=os.path.join(images, "minimum_inverter_sizing_analysis_simulation.png"), plt=plt)
    plt.show()

    minimum_inverter_sizing_analysis_log_file_path = f"./{minimum_inverter_sizing_analysis_log}"

    with open(minimum_inverter_sizing_analysis_log_file_path, "r") as file:
        content = file.read()

    w_min_pmos_analysis_data = re.search(w_min_pmos_analysis_pattern, content, re.DOTALL).group(1)
    rise_delay_minimum_inverter_sizing_analysis_data = re.search(rise_delay_connected_pattern, content,
                                                                 re.DOTALL).group(1)
    fall_delay_minimum_inverter_sizing_analysis_data = re.search(fall_delay_connected_pattern, content,
                                                                 re.DOTALL).group(1)

    w_min_pmos_analysis_lines = w_min_pmos_analysis_data.strip().split('\n')[1:]
    rise_delay_minimum_inverter_sizing_analysis_lines = rise_delay_minimum_inverter_sizing_analysis_data.strip().split(
        '\n')[1:]
    fall_delay_minimum_inverter_sizing_analysis_lines = fall_delay_minimum_inverter_sizing_analysis_data.strip().split(
        '\n')[1:]

    w_min_pmos_analysis = [float(line.split('\t')[1]) for line in w_min_pmos_analysis_lines]
    plt.figure(figsize=(16, 4))
    plt.legend(['w_min_pmos_analysis'])
    plt.plot(w_min_pmos_analysis, label='w_min_pmos_analysis')
    plt.ylabel('w_min_pmos')
    plt.xlabel('steps')
    plt.title('W min PMOS Trend')
    save_image(image_path=os.path.join(images, "w_min_pmos_analysis.png"), plt=plt)
    plt.show()

    rise_delay_minimum_inverter_sizing_analysis = [float(line.split('\t')[1]) for line in
                                                   rise_delay_minimum_inverter_sizing_analysis_lines]

    fall_delay_minimum_inverter_sizing_analysis = [float(line.split('\t')[1]) for line in
                                                   fall_delay_minimum_inverter_sizing_analysis_lines]

    diff_delay = [-1] * len(rise_delay_minimum_inverter_sizing_analysis) if len(
        rise_delay_minimum_inverter_sizing_analysis) == len(fall_delay_minimum_inverter_sizing_analysis) else -1
    i = 0
    for rise_delay, fall_delay in zip(rise_delay_minimum_inverter_sizing_analysis,
                                      fall_delay_minimum_inverter_sizing_analysis):
        diff_delay[i] = abs(rise_delay - fall_delay)
        i = i + 1

    data_table_w_pmos = {
        'w_pmos [m]': w_min_pmos_analysis,
        'rise_delay-fall_delay [s]': diff_delay
    }
    table_creation(
        data_table=data_table_w_pmos,
        title_plot="W_PMOS Sizing Analysis",
        title_image_saving="table_w_pmos_sizing_analysis.png",
        figsize=[16, 4]
    )

    i_min_diff = 0
    min_diff = diff_delay[i_min_diff]
    for i in range(len(diff_delay)):
        if diff_delay[i] < min_diff:
            i_min_diff = i
            min_diff = diff_delay[i]
    print(f'min(rise_delay-fall_delay) = {min_diff}')

    w_min_pmos_value = 0
    for i in range(len(w_min_pmos_analysis)):
        if i == i_min_diff:
            w_min_pmos_value = w_min_pmos_analysis[i]
    print(f'w_min_pmos = {w_min_pmos_value}')
    w_min_pmos = to_order(w_min_pmos_value, Order.MICRO)
    w_min_pmos = str(w_min_pmos) + 'u'
    print(f'w_min_pmos = {w_min_pmos}')

    w_min_pmos_file_path = os.path.join(data, 'out', 'minimum-inverter', 'get_sizing', 'w_min_pmos.txt')
    with open(w_min_pmos_file_path, 'w') as file:
        file.write(f'{w_min_pmos}\n')


if __name__ == "__main__":
    minimum_inverter_sizing_analysis()