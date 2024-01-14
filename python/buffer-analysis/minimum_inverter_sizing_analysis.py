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
    """
    The dimensioning of a minimum inverter involves analysing it by considering an associated load, a Vin and a
    Vsupply. Specifically, what is analysed is the rise and fall time obtained at the output (Vout). It must be
    specified that the minimum PMOS sizing of the minimum inverter in question occurs at a rise time equal to the
    corresponding fall time or at least in an infinitesimal range thereof.
    :return:
    """

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

    diff_delay = [
        abs(rise_delay - fall_delay)
        for rise_delay, fall_delay in
        zip(rise_delay_minimum_inverter_sizing_analysis, fall_delay_minimum_inverter_sizing_analysis)
    ]

    data_table_w_pmos = {
        'w_pmos [m]': w_min_pmos_analysis,
        'rise_delay-fall_delay [s]': diff_delay
    }
    table_creation(
        data_table=data_table_w_pmos,
        title_plot="W_PMOS Sizing Analysis",
        title_image_saving="table_w_pmos_sizing_analysis.png",
        figsize=[16, 7]
    )

    min_diff_delay = min(diff_delay)
    i_min_diff_delay = diff_delay.index(min_diff_delay)
    w_min_pmos_value = w_min_pmos_analysis[i_min_diff_delay]
    print(f'w_min_pmos = {w_min_pmos_value}')
    w_min_pmos = to_order(w_min_pmos_value, Order.MICRO)
    w_min_pmos = str(w_min_pmos) + 'u'
    print(f'w_min_pmos = {w_min_pmos}')

    w_min_pmos_file_path = os.path.join(data, 'out', 'minimum-inverter', 'get_sizing', 'w_min_pmos.txt')
    with open(w_min_pmos_file_path, 'w') as file:
        file.write(f'{w_min_pmos}\n')

    """What has been done is to calculate the difference between the corresponding ascent time and descent time and 
    consider the minimum of all calculated differences. What can be seen is that the differences are all almost very 
    small (on the order of magnitude of 10e-11). One of them turns out to be even smaller than the others (of the 
    order of magnitude 10e-14). Therefore, a corresponding width W of the PMOS transistor of 0.18u is obtained."""


if __name__ == "__main__":
    minimum_inverter_sizing_analysis()
