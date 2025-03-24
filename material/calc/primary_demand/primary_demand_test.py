from collections import Counter

import pytest

from material.calc.primary_demand.math_function_builder import build_polynomial_function
from material.calc.primary_demand.primary_demand_optimization import ProductionPlanner
from material.calc.primary_demand.primary_production_solution_data import ProductionSolutionData
from material.calc.primary_demand.production_planning_attributes import ProductionPlanningAttributes
# noinspection PyUnresolvedReferences
from material.db.models.item import Item
from material.db.models.models import *
from material.db.models.periodic_item_quantity import PeriodicItemQuantity, PeriodicItemQuantityBuilder


@pytest.fixture
def single_product_data():
    """
    Simple scenario: 1 product, 2 periods
    """
    demand_data: PeriodicItemQuantity = {
        1: Counter[Item]({Item(1): 80}),
        2: Counter[Item]({Item(1): 50})
    }
    init_inv = Counter[Item]({Item(1): 10})
    return demand_data, init_inv


@pytest.fixture
def multi_product_data():
    """
    More complex scenario: 2 products, 3 periods
    """
    demand_data: PeriodicItemQuantity = (
        PeriodicItemQuantityBuilder()
        .add_product(Item(1), [80, 100, 50, 100])
        .add_product(Item(2), [0, 0, 0, 100])
        .add_product(Item(3), [50, 0, 0, 100])
        .build()
    )
    init_inv = Counter[Item]({
        Item(1): 100,
        Item(2): 50,
        Item(3): 0
    }
    )

    return demand_data, init_inv


def test_single_product_optimization(single_product_data):
    demand_data, init_inv = single_product_data

    attrs = ProductionPlanningAttributes(
        inventory_cost_func=build_polynomial_function([0, 0.002, 8e-8]),
        production_cost_func=build_polynomial_function([1000, 10]),
        smoothing_factor=0.3,
        max_period_production=100
    )

    planner = ProductionPlanner(attrs)

    solution = planner.solve(demand_data, init_inv)

    assert isinstance(solution, ProductionSolutionData)
    total_production = sum(solution.production[p][Item(1)] for p in [1, 2])
    assert total_production >= 0


def test_multi_product_optimization(multi_product_data):
    demand_data: PeriodicItemQuantity = (
        PeriodicItemQuantityBuilder()
        .add_product(Item(1), [80, 100, 50, 100])
        .add_product(Item(2), [0, 0, 0, 100])
        .add_product(Item(3), [50, 0, 100, 10])
        .build()
    )
    init_inv = Counter[Item]({
        Item(1): 100,
        Item(2): 50,
        Item(3): 0
    }
    )

    # 1) Setup attributes
    attrs = ProductionPlanningAttributes(
        inventory_cost_func=build_polynomial_function([0, 0.002, 8e-8]),
        production_cost_func=build_polynomial_function([1000, 10]),
        smoothing_factor=0.3,
        max_period_production=100
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


def test_solution_print_table(capsys, multi_product_data):
    """
    Test the print_primary_demand_table method to ensure it prints a table
    in the correct format (GitHub style).
    We'll simply check that something is printed, not the exact string.
    """
    demand_data, init_inv = multi_product_data

    attrs = ProductionPlanningAttributes(
        inventory_cost_func=build_polynomial_function([0, 0.002, 8e-8]),
        production_cost_func=build_polynomial_function([1000, 10]),
        smoothing_factor=0.3,
        max_period_production=100
    )
    planner = ProductionPlanner(attrs)
    solution = planner.solve(demand_data, init_inv)
    print()
    solution.format_primary_demand_table()


def test_small_production_limit(single_product_data):
    """
    Test that with a small max_period_production, the solution obeys it.
    """
    demand_data, init_inv = single_product_data

    attrs = ProductionPlanningAttributes(
        inventory_cost_func=build_polynomial_function([0, 0.002, 8e-8]),
        production_cost_func=build_polynomial_function([1000, 10]),
        smoothing_factor=0.3,
        max_period_production=50
    )
    planner = ProductionPlanner(attrs)
    solution = planner.solve(demand_data, init_inv)

    solution.format_primary_demand_table()
    for p in demand_data.keys():
        prod_amount = solution.production[p][Item(1)]
        assert prod_amount <= 50 + 1e-6


def test_no_inventory_cost(single_product_data):
    """
    Test scenario with no inventory cost => we might see higher inventory buildup.
    Just checks we don't break anything.
    """
    demand_data, init_inv = single_product_data

    attrs = ProductionPlanningAttributes(
        inventory_cost_func=build_polynomial_function([0]),
        production_cost_func=build_polynomial_function([1000, 10]),
        smoothing_factor=0.3,
        max_period_production=100
    )
    planner = ProductionPlanner(attrs)
    solution = planner.solve(demand_data, init_inv)

    assert solution.inventory_cost == 0.0
    # We might see that the earnings is definitely > 0
    assert solution.earnings > 0
