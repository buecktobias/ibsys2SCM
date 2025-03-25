def build_polynomial_function(coeffs):
    """
    Given a list of coefficients [a0, a1, a2, ...],
    return f(x) = a0 + a1*x + a2*x^2 + ...
    """

    def polynomial_fn(x):
        val = 0.0
        for n, c in enumerate(coeffs):
            val += c * (x ** n)
        return val

    return polynomial_fn
