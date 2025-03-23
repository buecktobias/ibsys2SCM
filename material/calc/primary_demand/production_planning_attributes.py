from dataclasses import dataclass


@dataclass
class ProductionPlanningAttributes:
    """
    Holds the main numeric parameters for production planning.
    """
    inv_a: float
    inv_b: float
    prod_fixed: float
    prod_var: float
    smoothing_factor: float
    max_period_production: float = 10e100
