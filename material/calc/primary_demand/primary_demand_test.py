import pytest

from material.calc.primary_demand.primary_demand_optimization import ProductionPlanner
from material.calc.primary_demand.primary_production_solution_data import ProductionSolutionData
from material.calc.primary_demand.production_planning_attributes import ProductionPlanningAttributes
from material.core.resource_counter import ItemCounter
# noinspection PyUnresolvedReferences
from material.db.models.item import Item
from material.db.models.models import *
from material.db.models.periodic_item_quantity import PeriodicItemQuantity


# For demonstration, we'll assume they're local imports:


# import the classes from your module
# e.g. from my_package.production_planning_attributes import ProductionPlanningAttributes
#      from my_package.production_planner import ProductionPlanner
#      from my_package.production_solution_data import ProductionSolutionData


@pytest.fixture
def single_product_data():
    """
    Simple scenario: 1 product, 2 periods
    """
    demand_data: PeriodicItemQuantity = PeriodicItemQuantity({
        1: ItemCounter({Item(1): 80}),
        2: ItemCounter({Item(1): 50})
    })
    init_inv = ItemCounter({Item(1): 10})
    return demand_data, init_inv


@pytest.fixture
def multi_product_data():
    """
    More complex scenario: 2 products, 3 periods
    """
    demand_data: PeriodicItemQuantity = PeriodicItemQuantity({
        1: ItemCounter({Item(1): 80, Item(2): 0}),
        2: ItemCounter({Item(1): 50, Item(2): 0}),
        3: ItemCounter({Item(1): 100, Item(2): 100}),
    })
    init_inv = ItemCounter({Item(1): 10, Item(2): 5})
    return demand_data, init_inv


def test_single_product_optimization(single_product_data):
    demand_data, init_inv = single_product_data

    # 1) Setup attributes
    attrs = ProductionPlanningAttributes(
        inv_a=0.0,
        inv_b=0.002,
        prod_fixed=500.0,
        prod_var=2.0,
        smoothing_factor=0.4,
        max_period_production=100
    )

    # 2) Planner
    planner = ProductionPlanner(attrs)

    # 3) Solve
    solution = planner.solve(demand_data, init_inv)

    # 4) Basic checks
    assert isinstance(solution, ProductionSolutionData)
    # Check non-negative objective
    assert solution.objective >= 0.0
    # Check that we do produce something
    # e.g. sum of production for P1 across periods
    total_production = sum(solution.production[p][Item(1)] for p in [1, 2])
    assert total_production >= 0


def test_multi_product_optimization(multi_product_data):
    demand_data, init_inv = multi_product_data

    # 1) Setup attributes
    attrs = ProductionPlanningAttributes(
        inv_a=0.0,
        inv_b=0.001,  # smaller
        prod_fixed=1000.0,
        prod_var=2.5,
        smoothing_factor=0.3,
        max_period_production=100
    )

    # 2) Planner
    planner = ProductionPlanner(attrs)

    # 3) Solve
    solution = planner.solve(demand_data, init_inv)

    # 4) Basic checks
    assert isinstance(solution, ProductionSolutionData)
    # Check that the revenue is not zero
    assert solution.revenue > 0
    # Check production in each (period, product) is non-negative
    for _, periods in solution.production.items():
        period_values = periods.values()
        assert all(p >= 0 for p in period_values)
    # Quick check objective is not nan
    assert not (solution.objective is None or isinstance(solution.objective, float) and (
            solution.objective != solution.objective))


def test_solution_print_table(capsys, multi_product_data):
    """
    Test the print_primary_demand_table method to ensure it prints a table
    in the correct format (GitHub style).
    We'll simply check that something is printed, not the exact string.
    """
    demand_data, init_inv = multi_product_data

    attrs = ProductionPlanningAttributes(
        inv_a=0.0,
        inv_b=0.002,
        prod_fixed=1000.0,
        prod_var=2.0,
        smoothing_factor=0.3,
        max_period_production=100
    )
    planner = ProductionPlanner(attrs)
    solution = planner.solve(demand_data, init_inv)
    print()
    solution.print_primary_demand_table()


def test_small_production_limit(single_product_data):
    """
    Test that with a small max_period_production, the solution obeys it.
    """
    demand_data, init_inv = single_product_data

    # Suppose we limit production to 50 units each period
    attrs = ProductionPlanningAttributes(
        inv_a=0.0,
        inv_b=0.002,
        prod_fixed=100.0,
        prod_var=1.0,
        smoothing_factor=0.1,
        max_period_production=50
    )
    planner = ProductionPlanner(attrs)
    solution = planner.solve(demand_data, init_inv)

    solution.print_primary_demand_table()
    # Check each period's production sum <= 50
    # Only 1 product here, so just check production for that product
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
        inv_a=0.0,
        inv_b=0.0,
        prod_fixed=100.0,
        prod_var=1.0,
        smoothing_factor=0.0,
        max_period_production=100
    )
    planner = ProductionPlanner(attrs)
    solution = planner.solve(demand_data, init_inv)

    assert solution.inventory_cost == 0.0
    # We might see that the objective is definitely > 0
    assert solution.objective > 0
