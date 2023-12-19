import os
import matplotlib.pyplot as plt
from models.ops import save_image
from utils.dir import get_values_from_file
from utils.paths import data
from utils.paths import images


def buffer_plotting():
    s1_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard', 's1_buffer_analysis.txt')
    s1 = get_values_from_file(s1_buffer_analysis_file_path)
    s2_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard', 's2_buffer_analysis.txt')
    s2 = get_values_from_file(s2_buffer_analysis_file_path)

    fig, (plt1, plt2) = plt.subplots(2, 1, sharex=True, figsize=(16, 6))
    plt1.legend(['S1'])
    plt2.legend(['S2'])
    plt1.plot(s1, label='s1', color='b')
    plt1.set_ylabel('s1 values')
    plt1.set_xlabel('Monte Carlo Experiments')
    plt1.set_title('S1 Trend')
    plt2.plot(s2, label='s2', color='r')
    plt2.set_xlabel('Monte Carlo Experiments')
    plt2.set_ylabel('s2 values')
    plt2.set_title('S2 Trend')
    plt.tight_layout()
    save_image(image_path=os.path.join(images, "s1_s2_montecarlo_trend.png"), plt=plt)
    plt.show()

    """It can be seen that the experiments conducted according to the Monte Carlo method actually reflect the design 
        values: the values generated for S1 are around 4 with a variation of 0.75 and the values generated for S2 are 
        around 16 with a variation of 0.75."""

    """At this point, the energy-delay points obtained after considering the random variables S1 and S2 by means of 
    the Monte Carlo method and after simulating the 3-stage buffer are plotted. Specifically, the plot considered is 
    of the scatter type with the delay on the abscissas and the energy on the ordinates. Performing an initial 
    empirical analysis, it is possible to note that the optimum possible points from the point of view of low power 
    could be represented by all the points that present an energy-delay trade-off that makes their ratio as low as 
    possible, or at the same energy considering even greater delays. This last statement allows us to consider a 
    buffer with low power criteria, which is our goal while considering longer delays. Therefore, the optimal 
    possible curve could coincide with the minimum points obtained from the simulations considering Monte Carlo 
    experiments and visible in the scatter plot. It must be specified that this curve is not necessarily the optimal 
    one. In fact, this has to be confirmed by means of unconstrained optimisation with 2 variables, S1 and S2, 
    using the scipy.minimise optimisation algorithm available in Python or fmincon in MATLAB. Therefore, the optimal 
    curve will then be generated and compared with the scatter plot energy-delay obtained."""

    delay_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                             'delay_connected_buffer_analysis.txt')
    delay_connected_buffer = get_values_from_file(delay_connected_buffer_analysis_file_path)
    energy_connected_buffer_analysis_file_path = os.path.join(data, 'out', 'buffer', 'standard',
                                                              'energy_connected_buffer_analysis.txt')
    energy_connected_buffer = get_values_from_file(energy_connected_buffer_analysis_file_path)

    plt.scatter(delay_connected_buffer, energy_connected_buffer, edgecolors='black')
    plt.xlabel('Delay')
    plt.ylabel('Energy')
    plt.title('Monte Carlo Experiments')
    plt.tight_layout()
    save_image(image_path=os.path.join(images, "montecarlo_experiments.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    buffer_plotting()
