import dataclasses
from collections import Counter

import pytest

from scs.calc.primary_production.lp_model.planner_attributes import ProductionPlanningAttributes
from scs.calc.primary_production.lp_model.planner_solution import ProductionSolutionData
from scs.calc.primary_production.lp_model.production_planner import ProductionPlanner
from scs.calc.primary_production.math_function_builder import build_polynomial_function
from scs.core.domain.item_models import Item, ProducedItem
from scs.core.domain.periodic_quantities.periodic_item_quantities_builder import PeriodicItemQuantityBuilder


# noinspection PyUnresolvedReferences


@pytest.fixture
def demand_data():
    return (
            PeriodicItemQuantityBuilder()
            .add_product(ProducedItem(id=1), [100, 100, 50, 150])
            .add_product(ProducedItem(id=2), [150, 50, 50, 50])
            .add_product(ProducedItem(id=3), [150, 100, 50, 50])
            .build()
    )


@pytest.fixture
def init_inventory():
    return Counter[Item](
            {
                    ProducedItem(id=1): 100,
                    ProducedItem(id=2): 0,
                    ProducedItem(id=3): 100
            }
    )


def test_multi_product_optimization(demand_data, init_inventory):
    # 1) Setup attributes
    attrs = ProductionPlanningAttributes(
            inventory_cost_func=lambda x: build_polynomial_function([0, 0.002, 8e-8])(x * 200 * 4),
            production_cost_func=build_polynomial_function([20_000, 25]),
            smoothing_factor=0.5,
            max_period_production=900
    )

    planner = ProductionPlanner(attrs)

    solution1 = planner.solve(demand_data, init_inventory)
    print()
    print(solution1.get_full_summary())

    attrs2 = dataclasses.replace(attrs, dummy_periods=2)

    planner2 = ProductionPlanner(attrs2)

    solution2 = planner2.solve(demand_data, init_inventory)

    print("With 2 dummy periods:")
    print(solution2.get_full_summary())

    attrs3 = dataclasses.replace(attrs, dummy_periods=6)
    planner3 = ProductionPlanner(attrs3)
    solution3 = planner3.solve(demand_data, init_inventory)
    print("With 6 dummy periods:")
    print(solution3.get_full_summary())

    assert isinstance(solution1, ProductionSolutionData)
    assert solution1.revenue > 0
    for _, periods in solution1.production.items():
        period_values = periods.values()
        assert all(p >= 0 for p in period_values)
    assert not (solution1.earnings is None or isinstance(solution1.earnings, float) and (
            solution1.earnings != solution1.earnings))


def test_multi_product_optimization2(demand_data, init_inventory):
    attrs = ProductionPlanningAttributes(
            inventory_cost_func=lambda x: build_polynomial_function([0, 0.001, 1e-7])(x * 200 * 4),
            production_cost_func=build_polynomial_function([20_000, 25, 0.1]),
            smoothing_factor=50,
            max_period_production=900,
            dummy_periods=1
    )

    planner = ProductionPlanner(attrs)

    solution1 = planner.solve(demand_data, init_inventory)
    print()
    print(solution1.get_full_summary())
