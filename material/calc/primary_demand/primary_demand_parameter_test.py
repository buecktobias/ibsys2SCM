from collections import Counter

from material.calc.primary_demand.math_function_builder import build_polynomial_function
from material.calc.primary_demand.primary_demand_optimization import ProductionPlanner
from material.calc.primary_demand.primary_production_solution_data import ProductionSolutionData
from material.calc.primary_demand.production_planning_attributes import ProductionPlanningAttributes
# noinspection PyUnresolvedReferences
from material.db.models.item import Item
from material.db.models.models import *
from material.db.models.periodic_item_quantity import PeriodicItemQuantity, PeriodicItemQuantityBuilder


def test_multi_product_optimization():
    demand_data: PeriodicItemQuantity = (
        PeriodicItemQuantityBuilder()
        .add_product(Item(1), [100, 100, 50, 150])
        .add_product(Item(2), [150, 50, 50, 100])
        .add_product(Item(3), [150, 50, 100, 150])
        .build()
    )
    init_inv = Counter[Item]({
        Item(1): 100,
        Item(2): 0,
        Item(3): 100
    }
    )

    # 1) Setup attributes
    attrs = ProductionPlanningAttributes(
        inventory_cost_func=lambda x: build_polynomial_function([0, 0.002, 8e-8])(x * 200 * 4),
        production_cost_func=build_polynomial_function([20_000, 25]),
        smoothing_factor=0.5,
        max_period_production=900
    )

    planner = ProductionPlanner(attrs)

    solution = planner.solve(demand_data, init_inv)
    print()
    print(solution.get_full_summary())
    assert isinstance(solution, ProductionSolutionData)
    assert solution.revenue > 0
    for _, periods in solution.production.items():
        period_values = periods.values()
        assert all(p >= 0 for p in period_values)
    assert not (solution.earnings is None or isinstance(solution.earnings, float) and (
            solution.earnings != solution.earnings))
