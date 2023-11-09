s1_pattern = r"Measurement: s1_values\n(.*?)(?=\n\n|\Z)"
s2_pattern = r"Measurement: s2_values\n(.*?)(?=\n\n|\Z)"
energy_connected_pattern = r"Measurement: energy_connected\n(.*?)(?=\n\n|\Z)"
energy_disconnected_pattern = r"Measurement: energy_disconnected\n(.*?)(?=\n\n|\Z)"
rise_delay_connected_pattern = r"Measurement: rise_delay_connected\n(.*?)(?=\n\n|\Z)"
fall_delay_connected_pattern = r"Measurement: fall_delay_connected\n(.*?)(?=\n\n|\Z)"
rise_delay_disconnected_pattern = r"Measurement: rise_delay_disconnected\n(.*?)(?=\n\n|\Z)"
fall_delay_disconnected_pattern = r"Measurement: fall_delay_disconnected\n(.*?)(?=\n\n|\Z)"
