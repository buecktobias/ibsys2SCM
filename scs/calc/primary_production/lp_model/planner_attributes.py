from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ProductionPlanningAttributes:
    """
    Holds the main numeric parameters for production planning.
    """
    inventory_cost_func: Callable[[float], float]
    production_cost_func: Callable[[float], float]
    smoothing_factor: float
    max_period_production: float = 10e100
    dummy_periods: int = 0
