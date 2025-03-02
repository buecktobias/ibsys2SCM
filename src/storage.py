from scipy.stats import norm

def storage_cost(expected_storage, standard_deviation_relative, threshold):
    standard_deviation = expected_storage * standard_deviation_relative
    z = (threshold - expected_storage) / standard_deviation
    phi_z = norm.cdf(z)
    one_minus_phi_z = 1 - phi_z
    phi_z = norm.pdf(z)

    e_x_below = expected_storage - standard_deviation * (phi_z / phi_z) if phi_z > 0 else expected_storage
    e_x_above = expected_storage + standard_deviation * (phi_z / one_minus_phi_z) if one_minus_phi_z > 0 else expected_storage

    return (0.006 * e_x_below * phi_z) + ((5000 + 0.012 * e_x_above) * one_minus_phi_z)