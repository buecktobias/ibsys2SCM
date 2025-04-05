---
##../scs\conftest.py:
import logging
import os
import random
from pathlib import Path
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from scs.core.db.base import Base
from scs.core.db.item_models.produced_item_orm import ProducedItemORM
from scs.tests.item_factory import ItemFactory
from scs.tests.process_factory import ProcessFactory
from scs.tests.workstation_factory import WorkstationFactory

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
logging.basicConfig(
format="%(asctime)s [%(levelname)s] %(message)s",
datefmt="%Y-%m-%d %H:%M:%S",
level=logging.DEBUG
)

@pytest.fixture(scope="session")
def test_engine():
from sqlalchemy import create_engine

    engine = create_engine("sqlite:///test.db")
    yield engine
    engine.dispose()

@pytest.fixture(scope="session")
def engine() -> Generator[Engine, Any, None]:
"""Sets up the database tables before all tests and tears them down afterwards."""
sqlite_path = "test.db"
database_url = f"sqlite:///{sqlite_path}"
engine: Engine = create_engine(database_url)
Base.metadata.create_all(engine)
yield engine
Base.metadata.drop_all(engine)
engine.dispose()
delete_test_db(sqlite_path)

def delete_test_db(path: Path | str):
"""Deletes the test.db file if it exists."""
if os.path.exists(path):
os.remove(path)

@pytest.fixture(scope="session")
def db_session(engine) -> Generator[Session, Any, None]:
"""Provides a transaction-scoped SQLAlchemy session for each test."""
with Session(engine) as session:
yield session
session.rollback()

@pytest.fixture(scope="session")
def random_produced_item():
return ProducedItemORM(id=random.randint(1, 10 ** 8))

@pytest.fixture(scope="session")
def item_factory():
return ItemFactory()

@pytest.fixture(scope="session")
def workstation_factory():
return WorkstationFactory()

@pytest.fixture(scope="session")
def process_factory(item_factory, workstation_factory):
return ProcessFactory(
item_factory=item_factory,
workstation_factory=workstation_factory
)

---

---
##../scs\__init__.py:

---
---
##../scs\api\dto_models.py:
from enum import Enum
from typing import List

from pydantic import BaseModel

class GameDTO(BaseModel):
id: int

class XMLFile(BaseModel):
content: str # or use UploadFile later for real uploads

class PeriodResultDTO(BaseModel):
game_id: int
period: int
xml_file: XMLFile

class PrimaryPlanDTO(BaseModel):
game_id: int
period: int
planned_items: List[str]

class ProductionDTO(BaseModel):
game_id: int
period: int
article_id: str
quantity: int
priority: int

class OrderMode(str, Enum):
normal = "normal"
fast = "fast"

class OrderDTO(BaseModel):
game_id: int
period: int
article_id: str
quantity: int
mode: OrderMode

class WorkstationCapacityDTO(BaseModel):
game_id: int
period: int
workstation_id: int
shifts: int
overtime: int

class SimulationInputDTO(BaseModel):
game_id: int
period: int
xml_file: XMLFile

---
---
##../scs\api\routes.py:
---
##../scs\api\__init__.py:

---
---
##../scs\calc\calculate_required_resources.py:
from collections import Counter

from scs.core.db.item_models import ItemORM
from scs.core.domain.production_graph import ProductionGraph

class ResourceCalculator:
def __init__(self, productions_graph: ProductionGraph):
self.productions_graph = productions_graph

    def _traverse_node(
            self,
            graph: ProductionGraph,
            required_resources: Counter[ItemORM],
            inventory: Counter[ItemORM],
            node_id: str,
            multiplier: int = 1,
    ) -> None:
        """
        Recursively traverses the predecessors of 'node' in the graph.
        For each predecessor, computes the total required amount, subtracts any available
        inventory, and updates the required_resources counter.
        """
        g = graph._nx
        for pred_key in g.predecessors(node_id):
            edge_weight = g[pred_key][node_id].get("weight", 1)
            total_weight = edge_weight * multiplier
            available = inventory[g.nodes[pred_key]["data"]]
            needed = total_weight - available
            required_resources[pred_node] += needed
            self._traverse_node(graph, required_resources, inventory, pred_node, needed)

    def calculate_required_resources_from_inventory(
            self,
            graph: MaterialProductGraph,
            required_resources: ResourceCounter,
            inventory: ResourceCounter,
    ) -> ResourceCounter:
        """
        Traverses the graph, updating required_resources based on available inventory.
        """
        # Iterate over a copy of the current required_resources entries.
        for node, quantity in list(required_resources):
            self._traverse_node(graph, required_resources, inventory, node, quantity)
        return required_resources

    def calculate_required_resources(self, product_id: str) -> ResourceCounter:
        """
        Calculates the total required resources for the product identified by product_id,
        assuming an empty inventory.
        """
        product_node = self.productions_graph.get_node_by_uid(product_id)
        empty_inventory = ResourceCounter(Counter({product_node: 0}))
        required = ResourceCounter(Counter({product_node: 1}))
        return self.calculate_required_resources_from_inventory(
                self.productions_graph, required, empty_inventory
        )

---
---
##../scs\calc\main.py:
from supply_chain_optimization.core.calculate_required_resources import ResourceCalculator
from supply_chain_optimization.core.resource_counter import ResourceCounter
from supply_chain_optimization.setup.production_graph_setup import create_full_production_graph

def calc_basic_demand():
graph = create_full_production_graph()

    resource_calculator = ResourceCalculator(graph)

    current_inventory = ResourceCounter.from_id_map(
            graph,
            {
                    1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100, 10: 100,
                    11: 100, 12: 100, 13: 100, 14: 100, 15: 100, 16: 300, 17: 300, 18: 100, 19: 100, 20: 100,
                    21: 300, 22: 300, 23: 300, 24: 6100, 25: 3600, 26: 300, 27: 1800, 28: 4500, 29: 100,
                    30: 100, 31: 100, 32: 2700, 33: 900, 34: 22000, 35: 3600, 36: 900, 37: 900, 38: 300,
                    39: 900, 40: 900, 41: 900, 42: 1800, 43: 1900, 44: 2700, 45: 900, 46: 900, 47: 900,
                    48: 1800, 49: 100, 50: 100, 51: 100, 52: 600, 53: 22000, 54: 100, 55: 100, 56: 100,
                    57: 600, 58: 22000, 59: 1800
            }

    )

    required = resource_calculator.calculate_required_resources_from_inventory(
            graph,
            ResourceCounter.from_id_map(
                    graph, {
                            "E1": 150,
                            "E2": 150,
                            "E3": 150
                    }
            ),
            current_inventory
    )

    required.print_sorted_resources()

if __name__ == '__main__':
calc_basic_demand()

---
---
##../scs\calc\__init__.py:

---
---
##../scs\calc\primary_production\math_function_builder.py:
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

---
---
##../scs\calc\primary_production\primary_production_test.py:
from collections import Counter

import pytest

from scs.calc.primary_production.lp_model.planner_attributes import ProductionPlanningAttributes
from scs.calc.primary_production.lp_model.planner_solution import ProductionSolutionData
from scs.calc.primary_production.lp_model.production_planner import ProductionPlanner
from scs.calc.primary_production.math_function_builder import build_polynomial_function
from scs.core.domain.item_models import Item, ProducedItem
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity
from scs.core.domain.periodic_quantities.periodic_item_quantities_builder import PeriodicItemQuantityBuilder

# noinspection PyUnresolvedReferences

@pytest.fixture
def single_product_data():
"""
Simple scenario: 1 product, 2 periods
"""
demand_data: PeriodicItemQuantity = PeriodicItemQuantity(
{
1: Counter[Item]({ProducedItem(id=1): 80}),
2: Counter[Item]({ProducedItem(id=1): 50})
}
)
init_inv = Counter[Item]({ProducedItem(id=1): 10})
return demand_data, init_inv

@pytest.fixture
def multi_product_data():
"""
More complex scenario: 2 products, 3 periods
"""
builder = PeriodicItemQuantityBuilder()
demand_data: PeriodicItemQuantity = (
builder
.add_product(ProducedItem(id=1), [80, 100, 50, 100])
.add_product(ProducedItem(id=2), [0, 0, 0, 100])
.add_product(ProducedItem(id=3), [50, 0, 0, 100])
.build()
)
init_inv = Counter[Item](
{
ProducedItem(id=1): 100,
ProducedItem(id=2): 50,
ProducedItem(id=3): 0
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
    total_production = solution.production.sum()
    assert total_production >= 0

def test_multi_product_optimization(multi_product_data):
demand_data: PeriodicItemQuantity = (
PeriodicItemQuantityBuilder()
.add_product(ProducedItem(id=1), [80, 100, 50, 100])
.add_product(ProducedItem(id=2), [0, 0, 0, 100])
.add_product(ProducedItem(id=3), [50, 0, 100, 10])
.build()
)
init_inv = Counter[Item](
{
ProducedItem(id=1): 100,
ProducedItem(id=2): 50,
ProducedItem(id=3): 0
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
    for period in demand_data.get_periods():
        prod_amount = solution.production.get_value_for_item(period, ProducedItem(id=1))
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
    assert solution.earnings > 0

---
---
##../scs\calc\primary_production\production_parameter_test.py:
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

---
---
##../scs\calc\primary_production\__init__.py:

---
---
##../scs\calc\primary_production\lp_model\lp_model_builder.py:
from collections import Counter

from pyomo import environ as pyo

# noinspection PyUnresolvedReferences

from pyomo.core import ConcreteModel, Var, Constraint, NonNegativeReals

from scs.calc.primary_production.lp_model.planner_attributes import ProductionPlanningAttributes
from scs.core.domain.item_models import Item
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity

class ProductionPlanningModelBuilder:
def __init__(
self,
attrs: ProductionPlanningAttributes,
demand_forecast: PeriodicItemQuantity,
init_inventory: Counter[Item]
):

        self._attrs: ProductionPlanningAttributes = attrs
        self._demand_forecast: PeriodicItemQuantity = demand_forecast
        self._init_inventory: Counter[Item] = init_inventory

    @property
    def _periods(self):
        return sorted(self._demand_forecast.get_periods())

    @property
    def _products(self):
        return self._demand_forecast.get_unique_items()

    @property
    def highest_period(self):
        return self._demand_forecast.highest_period

    @property
    def _extended_periods(self):
        return [0] + self._periods

    def _add_dummy_periods(self):
        average_item_demands: Counter[Item] = Counter(
                {
                        item: round(count) for item, count in self._demand_forecast.get_average_values().items()
                }
        )
        for i in range(self._attrs.dummy_periods):
            self._demand_forecast.add_period(average_item_demands)

    def build_pyomo_model(self) -> ConcreteModel:
        model = ConcreteModel("ProductionPlan")
        self._add_dummy_periods()
        self._create_variables(model)
        self._set_initial_inventory(model)
        self._create_constraints(model)
        self._create_expressions(model)
        self._create_objective(model)
        return model

    def _get_models_production(self, model, period, item) -> int:
        return model.P[period, item]

    def _get_models_inventory(self, model, period, item) -> int:
        return model.Inv[period, item]

    def _get_normalized_demand(self, period, item) -> int:
        return round(self._demand_forecast.get_value_for_item(period, item) / 10)

    def _create_variables(self, model: ConcreteModel) -> None:
        model.P = Var(
                ((t, i) for t in self._periods for i in self._products),
                domain=NonNegativeReals
        )
        model.Inv = Var(
                ((t, i) for t in self._extended_periods for i in self._products),
                domain=NonNegativeReals
        )

    def _set_initial_inventory(self, model: ConcreteModel) -> None:
        def init_inv_rule(mdl, item):
            return mdl.Inv[0, item] == int(self._init_inventory[item] / 10)

        model.InitInv = Constraint(self._products, rule=init_inv_rule)

    def _create_constraints(self, model: ConcreteModel) -> None:
        def inv_balance_rule(mdl, period, item):
            previous_inventory = self._get_models_inventory(model, period - 1, item)
            current_production = self._get_models_production(model, period, item)
            current_demand = self._get_normalized_demand(period, item)
            return (
                    mdl.Inv[period, item] == previous_inventory + current_production - current_demand
            )

        model.InvBalance = Constraint(list(model.P.keys()), rule=inv_balance_rule)

        def max_prod_rule(mdl, period):
            return sum(
                    self._get_models_production(mdl, period, p) * 10 for p in
                    self._products
            ) <= self._attrs.max_period_production

        model.MaxProd = Constraint(self._periods, rule=max_prod_rule)

    def _create_expressions(self, model: ConcreteModel) -> None:
        @model.Expression()
        def total_production(mdl):
            return sum(self._get_models_production(mdl, t, i) * 10 for t in self._periods for i in self._products)

        @model.Expression()
        def production_cost(mdl):
            expr = 0.0
            for t in self._periods:
                total_production_t = sum(self._get_models_production(mdl, t, i) * 10 for i in self._products)
                expr += self._attrs.production_cost_func(total_production_t)
            return expr

        @model.Expression()
        def inventory_cost(mdl):
            expr = 0.0
            for t in self._periods:
                total_inv_t = sum(self._get_models_inventory(mdl, t, i) * 10 for i in self._products)
                expr += self._attrs.inventory_cost_func(total_inv_t)
            return expr

        @model.Expression()
        def production_variance(mdl):
            t_len = float(len(self._periods))
            total_var = 0.0
            for i in self._products:
                avg_p = sum(self._get_models_production(mdl, t, i) for t in self._periods) / t_len
                sum_sq = sum((self._get_models_production(mdl, t, i) - avg_p) ** 2 for t in self._periods)
                total_var += (1.0 / t_len) * sum_sq
            return self._attrs.smoothing_factor * total_var * 10

        @model.Expression()
        def revenue(mdl):
            return 200.0 * mdl.total_production  # example uniform price

    def _create_objective(self, model: ConcreteModel) -> None:
        def obj_rule(mdl):
            return (
                    mdl.revenue -
                    (mdl.production_cost + mdl.inventory_cost + mdl.production_variance)
            )

        model.Obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

---
---
##../scs\calc\primary_production\lp_model\planner_attributes.py:
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

---
---
##../scs\calc\primary_production\lp_model\planner_solution.py:
from dataclasses import dataclass

from tabulate import tabulate

from scs.calc.primary_production.lp_model.planner_attributes import ProductionPlanningAttributes
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity

@dataclass
class ProductionSolutionData:
"""
Dataclass capturing the final solution of the production planning optimization.
"""
production_plan_attributes: ProductionPlanningAttributes
demand: PeriodicItemQuantity
production: PeriodicItemQuantity
inventory: PeriodicItemQuantity
production_cost: float
inventory_cost: float
variance_penalty: float
revenue: float
earnings: float

    def format_primary_demand_table(self, with_dummy=False) -> str:
        periods = self.inventory.get_periods() if with_dummy else self.inventory.get_periods()[
                                                                  :-self.production_plan_attributes.dummy_periods]

        headers = ["Product"] + [f"Period {p}" for p in periods]
        table = []

        second_header_row = [""] + [" | ".join(["D  ", " P ", " I "]) for _ in periods]

        table.append(second_header_row)
        for prod in sorted(self.production.get_unique_items()):
            row = [str(prod.id)]
            for p in periods:
                i_val = self.inventory.get_value_for_item(p, prod)
                inv_formatted = str(round(i_val)).rjust(3)
                if p == 0:
                    demand_formatted = "-".ljust(3)
                    production_formatted = "-".rjust(3)
                else:
                    d_val = self.demand.get_value_for_item(p, prod)
                    p_val = self.production.get_value_for_item(p, prod)
                    demand_formatted = str(int(round(d_val))).ljust(3)
                    production_formatted = str(int(round(p_val))).rjust(3)
                cell = " | ".join(
                        [demand_formatted, production_formatted, inv_formatted]
                )
                row.append(cell)
            table.append(row)

        return (tabulate(table, headers=headers, tablefmt="github")
                + "\n\n D: Demand, P: Production, I: Inventory")

    def get_full_summary(self):
        s = f"""
        Production Solution Data:
        
        {self.format_primary_demand_table()}
        
        Production Cost: {self.production_cost:.2f}
        Inventory Cost: {self.inventory_cost:.2f}
        Variance Penalty: {self.variance_penalty:.2f}
        Revenue: {self.revenue:.2f}
        Earnings: {self.earnings:.2f}
        """
        return '\n'.join(line.lstrip() for line in s.splitlines())

    def get_production_program(self):
        return self.production.get_counters(1)

    def __str__(self):
        """
        String summary of the numeric solution _data.
        """
        return (
                f"ProductionSolutionData(\n"
                f"  demand={self.demand},\n"
                f"  production_cost={self.production_cost:.2f},\n"
                f"  inventory_cost={self.inventory_cost:.2f},\n"
                f"  variance_penalty={self.variance_penalty:.2f},\n"
                f"  revenue={self.revenue:.2f},\n"
                f"  earnings={self.earnings:.2f}\n"
                f")"
        )

---
---
##../scs\calc\primary_production\lp_model\production_planner.py:
from collections import defaultdict, Counter

from pyomo.environ import SolverFactory, value

from scs.calc.primary_production.lp_model.lp_model_builder import ProductionPlanningModelBuilder
from scs.calc.primary_production.lp_model.planner_attributes import ProductionPlanningAttributes
from scs.calc.primary_production.lp_model.planner_solution import ProductionSolutionData
from scs.core.domain.item_models import Item
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity

class ProductionPlanner:
"""
Orchestrates:

- receiving cost/limit attributes,
- building the Pyomo model (via ProductionPlanningModelBuilder),
- solving,
- returning a ProductionSolutionData dataclass with results.
  """

  def __init__(self, attrs: ProductionPlanningAttributes):
  """
  :param attrs: ProductionPlanningAttributes containing:
  fixed_inv_cost, variable_linear_cost, prod_fixed, prod_var, smoothing_factor, max_period_production
  """
  self.attrs = attrs
  self.model = None
  self.solver_results = None

  def solve(
  self,
  demand_forecast: PeriodicItemQuantity,
  init_inventory: Counter[Item]
  ) -> ProductionSolutionData:
  """
  Build and solve the production plan with the given demand and inventory.

        :param demand_forecast: e.g. {1:{Item1:80, Item2:40}, 2:{Item1:50,...},...}
        :param init_inventory: e.g. {'P1':10,'P2':5}
        :return: ProductionSolutionData with production, inventory, costs, revenue, earnings
        """

        # 1) Build the pyomo model
        builder = ProductionPlanningModelBuilder(
                attrs=self.attrs,
                demand_forecast=demand_forecast,
                init_inventory=init_inventory
        )
        self.model = builder.build_pyomo_model()

        # 2) Solve
        solver = SolverFactory('ipopt')
        self.solver_results = solver.solve(self.model, tee=False)

        model = self.model
        prod_plan: dict[int, Counter[Item]] = defaultdict(Counter[Item])
        inv_plan: dict[int, Counter[Item]] = defaultdict(Counter[Item])

        for (t, i) in model.P.keys():
            prod_plan[t][i] = int(round(value(model.P[t, i]))) * 10

        for (t, i) in model.Inv.keys():
            inv_plan[t][i] = int(round(value(model.Inv[t, i]))) * 10

        return ProductionSolutionData(
                production_plan_attributes=self.attrs,
                demand=demand_forecast,
                production=PeriodicItemQuantity(prod_plan),
                inventory=PeriodicItemQuantity(inv_plan),
                production_cost=value(model.production_cost),
                inventory_cost=value(model.inventory_cost),
                variance_penalty=value(model.production_variance),
                revenue=value(model.revenue),
                earnings=value(model.Obj),
        )

---
---
##../scs\calc\primary_production\lp_model\__init__.py:

---
---
##../scs\config\config.py:
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg:app_user:1234@localhost:6543/postgres")

---
---
##../scs\config\__init__.py:

---
---
##../scs\core\__init__.py:

---
---
##../scs\core\db\base.py:
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
pass

---
---
##../scs\core\db\workstation_orm.py:
from __future__ import annotations

from sqlalchemy.orm import Mapped

from scs.core.db.base import Base
from scs.core.db.mixins.id_mixin import IdMixin

class WorkstationORM(IdMixin, Base):
__tablename__ = "workstation"
labour_cost_1: Mapped[float]
labour_cost_2: Mapped[float]
labour_cost_3: Mapped[float]
labour_overtime_cost: Mapped[float]
variable_machine_cost: Mapped[float]
fixed_machine_cost: Mapped[float]

---
---
##../scs\core\db\workstation_orm_test.py:
from sqlalchemy.orm import Session

from scs.core.db.workstation_orm import WorkstationORM

def test_workstation(db_session: Session):
ws = WorkstationORM(
id=101,
labour_cost_1=10, labour_cost_2=11, labour_cost_3=12,
labour_overtime_cost=15, variable_machine_cost=20, fixed_machine_cost=30
)
db_session.add(ws)
db_session.commit()
assert db_session.get(WorkstationORM, ws.id)

---
---
##../scs\core\db\__init__.py:
from .mixins import IdMixin, PeriodMixin, QuantityMixin
from .periodic import DemandForecastItemORM, InventoryItemORM
from .process_models import ProcessInputORM, ProcessORM, ProcessOutputORM

---
---
##../scs\core\db\graph\graph_node_orm.py:
from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.base import Base

class GraphNodeORM(Base):
"""
Represents a GraphNode in the database.

    This class defines the structure and behavior of a graph node within the database,
    using SQLAlchemy ORM. It inherits from IdMixin and Base, providing common identifiers
    and base functionalities. The class includes mapping for polymorphic behavior to
    differentiate between various graph node types.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        type (Mapped[str]): The type field for distinguishing polymorphic identity,
            stored as a string with a maximum length of 50 characters.
        __mapper_args__ (dict): Dictionary containing configuration for polymorphic
            behavior. Specifies the polymorphic identity as 'graph_node' and the
            polymorphic discriminator as 'type'.
    """
    __tablename__ = "graph_node"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
            "polymorphic_identity": "graph_node",
            "polymorphic_on": "type",
    }

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

---
---
##../scs\core\db\graph\graph_node_orm_test.py:
from scs.core.db.graph.graph_node_orm import GraphNodeORM
from scs.core.db.item_models.produced_item_orm import ProducedItemORM

def test_insert_and_retrieve_graph_node(db_session):

# Assign

graph_node = ProducedItemORM(id=101)
db_session.add(graph_node)
db_session.commit()

    # Act
    retrieved_node = db_session.get(GraphNodeORM, graph_node.id)

    # Assert
    assert retrieved_node is not None
    assert retrieved_node.id == graph_node.id
    assert retrieved_node.type == ProducedItemORM.__tablename__

---
---
##../scs\core\db\graph\material_graph_orm.py:
from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.base import Base
from scs.core.db.mixins.id_mixin import IdMixin
from scs.core.db.process_models import ProcessORM

class MaterialGraphORM(IdMixin, Base):
"""
Represents a material graph structure and its relationships in the database.

    This class models a material graph used for representing hierarchical structures
    of materials and the associated processes within a database. It provides fields
    and relationships to manage parent-child structures and link related processes.
    The `material_graph` table serves as the database table corresponding to this
    class.

    Attributes:
        __tablename__ (str): Name of the database table to which this class is mapped.
        name (Mapped[str]): Name of the material graph.
        parent_graph_id (Mapped[Optional[int]]): Foreign key referencing the parent
            material graph's ID. Enables hierarchical relationships.
        parent_graph (Mapped[MaterialGraphORM]): Relationship to the parent graph.
            Represents the parent material graph in the hierarchy.
        subgraphs (Mapped[list[MaterialGraphORM]]): Relationship to child material
            graphs. Lists all subgraphs associated with the current graph.
        processes (Mapped[list[ProcessORM]]): Relationship to processes associated
            with the material graph. Links the material graph to its processes.
    """
    __tablename__ = "material_graph"
    name: Mapped[str]
    parent_graph_id: Mapped[Optional[int]] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="SET NULL")
    )

    parent_graph: Mapped[MaterialGraphORM] = relationship(
            back_populates="subgraphs", remote_side=lambda: MaterialGraphORM.id, lazy="joined"
    )
    subgraphs: Mapped[list[MaterialGraphORM]] = relationship(back_populates="parent_graph", lazy="joined")
    processes: Mapped[list[ProcessORM]] = relationship(back_populates="graph", lazy="joined")

---
---
##../scs\core\db\graph\material_graph_orm_test.py:
from sqlalchemy.orm import Session

from scs.core.db.graph.material_graph_orm import MaterialGraphORM

def test_create_and_fetch_graph(db_session: Session):
new_graph = MaterialGraphORM(id=123, name="Real DB Graph")
db_session.add(new_graph)
db_session.commit()

    fetched = db_session.get(MaterialGraphORM, 123)
    assert fetched is not None
    assert isinstance(fetched, MaterialGraphORM)
    assert fetched.name == "Real DB Graph"

    db_session.delete(fetched)
    db_session.commit()

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scs.core.db.base import Base
from scs.core.db.graph.material_graph_orm import MaterialGraphORM
from scs.core.db.process_models.process_orm import ProcessORM

def test_material_graph_creation(db_session: Session):
"""Tests if a MaterialGraphORM object can be successfully created and added to the database."""
material_graph = MaterialGraphORM(name="Test Graph")
db_session.add(material_graph)
db_session.commit()

    fetched_graphs = db_session.query(MaterialGraphORM).all()
    assert len(fetched_graphs) == 1, "Expected one material graph in the database."
    assert fetched_graphs[0].name == "Test Graph", "Material graph name does not match."

def test_material_graph_hierarchy(db_session: Session):
"""Tests if hierarchical relationships between material graphs are correctly handled."""
parent_graph = MaterialGraphORM(name="Parent Graph")
child_graph = MaterialGraphORM(name="Child Graph", parent_graph=parent_graph)

    db_session.add(parent_graph)
    db_session.add(child_graph)
    db_session.commit()

    fetched_parent = db_session.query(MaterialGraphORM).filter_by(name="Parent Graph").one()
    # noinspection PydanticTypeChecker
    assert len(fetched_parent.subgraphs) == 1, "Expected one child graph linked to the parent graph."
    assert fetched_parent.subgraphs[0].name == "Child Graph", "Child graph name does not match."

def test_material_graph_process_association(db_session: Session):
"""Tests if processes can be correctly associated with a material graph."""
material_graph = MaterialGraphORM(name="Graph with Process")
process = ProcessORM(graph=material_graph, workstation_id=1, process_duration_minutes=10, setup_duration_minutes=10)

    db_session.add(material_graph)
    db_session.add(process)
    db_session.commit()

    fetched_graph = db_session.query(MaterialGraphORM).filter_by(name="Graph with Process").one()
    # noinspection PydanticTypeChecker
    assert len(fetched_graph.processes) == 1, "Expected one process associated with the material graph."
    assert fetched_graph.processes[0].id == process.id, "Associated process ID does not match."

---
---
##../scs\core\db\graph\__init__.py:

---
---
##../scs\core\db\item_models\bought_item_orm.py:
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.item_models.item_orm import ItemORM

class BoughtItemORM(ItemORM):
"""
Represents an ORM mapping for a bought item in the database.

    This class serves as a data model for a purchased item, including its pricing,
    discount, and ordering-related statistics. It inherits mappings and behavior
    from ItemORM and integrates additional attributes. The class also defines
    mapping to the corresponding database table for ORM usage.

    Attributes:
        __tablename__ (str): The name of the corresponding database table.
        __mapper_args__ (dict): Defines specific SQLAlchemy ORM mapper arguments,
            such as polymorphic identity.

        id (int): The primary key of the bought item, referencing the ItemORM ID
            with cascading updates on changes.
        base_price (float): The base price of the bought item before any discount.
        discount_amount (int): The discount amount applied to the base price.
        mean_order_duration (float): The average duration (e.g., in days) it takes
            for an order of this item to be processed or completed.
        order_std_dev (float): The standard deviation of ordering durations, giving
            insights into the consistency of order times.
        base_order_cost (float): The baseline cost associated with fulfilling
            orders for the item.

    """
    __tablename__ = "bought_item"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id, onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    base_price: Mapped[float]
    discount_amount: Mapped[int]
    mean_order_duration: Mapped[float]
    order_std_dev: Mapped[float]
    base_order_cost: Mapped[float]

---
---
##../scs\core\db\item_models\item_orm.py:
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.graph.graph_node_orm import GraphNodeORM

class ItemORM(GraphNodeORM):
"""
Represents a database model for an item which extends the GraphNodeORM model.

    This class defines the "item" table with attributes such as id and type. It
    uses SQLAlchemy's ORM features including mapped columns and table constraints.
    The class assumes a polymorphic identity for distinguishing between object
    types in a single table inheritance scenario. This model is particularly
    useful for representing specialized graph nodes classified as items.

    Attributes:
        id (int): The primary key of the item, inheriting a foreign key
            constraint from the graph node table.
        type (str): A string value representing the type of the item, stored
            as a column with a maximum length of 50 characters.
    """
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(
            ForeignKey("graph_node.id", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True
    )

    __mapper_args__ = {
            "polymorphic_identity": __tablename__,
    }

---
---
##../scs\core\db\item_models\item_orm_test.py:
from sqlalchemy.orm import Session

from scs.core.db.item_models.bought_item_orm import BoughtItemORM
from scs.core.db.item_models.item_orm import ItemORM
from scs.core.db.item_models.produced_item_orm import ProducedItemORM

def test_create_and_fetch_item(db_session: Session):
new_item = ProducedItemORM(id=999)
db_session.add(new_item)
db_session.commit()

    fetched = db_session.get(ItemORM, 999)
    assert fetched is not None
    assert fetched.id == 999

    db_session.delete(fetched)
    db_session.commit()

def test_item_bought_produced(db_session: Session):
produced = ProducedItemORM(id=1002207)
db_session.add(produced)
db_session.commit()

    bought = BoughtItemORM(
            id=101207, base_price=100.0, discount_amount=10,
            mean_order_duration=3.0, order_std_dev=0.5, base_order_cost=25.0
    )
    db_session.add_all([bought, produced])
    db_session.commit()

    assert db_session.get(BoughtItemORM, bought.id)
    assert db_session.get(ProducedItemORM, produced.id)

---
---
##../scs\core\db\item_models\produced_item_orm.py:
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.item_models.item_orm import ItemORM

class ProducedItemORM(ItemORM):
"""
Represents a produced item within the database.

    This class is a mapped dataclass that extends the functionality of the
    ItemORM to represent a specific type of item, identified as a
    produced item. Used in the database schema with polymorphic identity.

    Attributes:
        __tablename__ (str): Name of the table in the database for
            produced items.
        __mapper_args__ (dict): Mapping arguments defining the polymorphic
            identity for this class.
        id (Mapped[int]): Primary key of the produced item, with a foreign
            key reference to the ItemORM base class.
    """
    __tablename__ = "produced_item"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id, onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

---
---
##../scs\core\db\item_models\__init__.py:

---
---
##../scs\core\db\mixins\id_mixin.py:
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from scs.core.db.base import Base

class IdMixin(Base):
"""
A mixin class for providing an ID attribute to models.

    This class adds a primary key ID column to any SQLAlchemy model that inherits
    it. It is marked as abstract and is designed to be used as a base class
    for creating models that require a primary key ID field.

    Attributes:
        id (int): The primary key ID attribute for the model. It is mapped to an
            integer field and serves as the primary key.
    """
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

---
---
##../scs\core\db\mixins\periodic_quantity_test.py:
import random
from collections import Counter

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from scs.core.db.graph.graph_node_orm import GraphNodeORM
from scs.core.db.item_models.produced_item_orm import ProducedItemORM
from scs.core.db.periodic.demand_forecast_item_orm import DemandForecastItemORM

# Database connection setup

def populate_db_with_test_data(session: Session, id1: int, id2: int):
"""Populates the database with test data for items and demand forecasts."""

# Define test items and demand forecast data

    session.query(GraphNodeORM).delete()
    session.query(ProducedItemORM).delete()
    session.query(DemandForecastItemORM).delete()
    test_items = [ProducedItemORM(id=id1), ProducedItemORM(id=id2)]
    test_demand_forecasts = [
            DemandForecastItemORM(item_id=id1, period=1, quantity=10),
            DemandForecastItemORM(item_id=id2, period=1, quantity=20),
            DemandForecastItemORM(item_id=id1, period=2, quantity=100),
            DemandForecastItemORM(item_id=id2, period=2, quantity=20),
    ]
    # Populate the database
    session.add_all(test_items)
    session.commit()
    session.add_all(test_demand_forecasts)

def test_populate_db_with_test_data(db_session: Session):
"""Tests if the database is populated with the correct test data."""
id1 = random.randint(1, 100 ** 9)
id2 = random.randint(1, 10 ** 9)
populate_db_with_test_data(db_session, id1, id2)

    test_items = db_session.query(ProducedItemORM).all()
    assert len(test_items) == 2, "Expected 2 test items in the database."

    demand_forecasts = db_session.query(DemandForecastItemORM).all()
    assert len(demand_forecasts) == 4, "Expected 4 demand forecast items in the database."

@pytest.mark.skip(reason="Not yet implemented.")
def test_demand_forecast_retrieval(db_session: Session, engine: Engine):
"""Tests retrieval and validation of demand forecast data."""
engine.begin()

# Setup database with predefined test data

id1 = random.randint(1, 10 ** 9)
id2 = random.randint(1, 10 ** 9)
populate_db_with_test_data(db_session, id1, id2)

    forecast_result = db_session.query(DemandForecastItemORM).all()
    # Fetch result and validate
    forecast_dict = {
            forecast.period: Counter({forecast.item_id: forecast.quantity for forecast in forecast_result})
            for forecast in forecast_result
    }
    print(forecast_dict)  # Print for debugging purposes
    expected_result = {
            1: Counter({id1: 10, id2: 20}),
            2: Counter({id1: 100, id2: 20}),
    }

    assert forecast_dict == expected_result, "Forecast data does not match the expected result."

---
---
##../scs\core\db\mixins\period_mixin.py:
from sqlalchemy.orm import Mapped, mapped_column

class PeriodMixin:
"""
Provides functionality for managing and representing a period.

    This mixin class is designed to be used with SQLAlchemy ORM to manage entities
    that require a period column. The 'period' attribute is defined as the primary
    key. This mixin can be inherited by other classes to share period-related
    functionality.

    Attributes:
        period (int): Represents the period, acting as the primary key in the
            table.
    """
    period: Mapped[int] = mapped_column(primary_key=True)

---
---
##../scs\core\db\mixins\quantity_mixin.py:
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from scs.core.db.base import Base
from scs.core.db.item_models.item_orm import ItemORM

class QuantityMixin(Base):
__abstract__ = True
item_id: Mapped[int] = mapped_column(ForeignKey(ItemORM.id), primary_key=True)
quantity: Mapped[int] = mapped_column(default=0)

    @declared_attr
    def item(self) -> Mapped[ItemORM]:
        return relationship(
                ItemORM,
                lazy="joined"
        )

---
---
##../scs\core\db\mixins\__init__.py:
from scs.core.db.mixins.id_mixin import IdMixin
from scs.core.db.mixins.period_mixin import PeriodMixin
from scs.core.db.mixins.quantity_mixin import QuantityMixin

---
---
##../scs\core\db\periodic\demand_forecast_item_orm.py:
from __future__ import annotations

from scs.core.db.base import Base
from scs.core.db.mixins.period_mixin import PeriodMixin
from scs.core.db.mixins.quantity_mixin import QuantityMixin

class DemandForecastItemORM(PeriodMixin, QuantityMixin, Base):
"""
Represents the ORM model for the demand forecast.

    This class maps to the 'demand_forecast' table in the database and extends the
    functionality provided by PeriodMixin, QuantityMixin, and Base classes. It is
    used for storing and managing demand forecast data along with associated period
    information and quantity details.

    Attributes:
        __tablename__ (str): Name of the table in the database represented by this
            ORM model, which is "demand_forecast".
    """
    __tablename__ = "demand_forecast"

---
---
##../scs\core\db\periodic\demand_forecast_item_orm_test.py:
import pytest
from scs.core.db.periodic.demand_forecast_item_orm import DemandForecastItemORM

def test_demand_forecast_item_orm_table_name():
assert DemandForecastItemORM.__tablename__ == "demand_forecast"

def test_demand_forecast_item_orm_period_column():

# Arrange, Act

instance = DemandForecastItemORM()

    # Assert
    assert hasattr(instance, 'period'), "Attribute 'period' is not present in the ORM model."

def test_demand_forecast_item_orm_quantity_column():

# Arrange, Act

instance = DemandForecastItemORM()

    # Assert
    assert hasattr(instance, 'quantity'), "Attribute 'quantity' is not present in the ORM model."

@pytest.mark.usefixtures("db_session")
def test_demand_forecast_item_orm_inserts_to_db(db_session):

# Arrange

instance = DemandForecastItemORM(period=202310, item_id=1001, quantity=50)

    # Act
    db_session.add(instance)
    db_session.commit()
    result = db_session.query(DemandForecastItemORM).filter_by(period=202310).one()

    # Assert
    assert result.period == 202310
    assert result.item_id == 1001
    assert result.quantity == 50

---
---
##../scs\core\db\periodic\inventory_item_orm.py:
from __future__ import annotations

from scs.core.db.base import Base
from scs.core.db.mixins.period_mixin import PeriodMixin

class InventoryItemORM(PeriodMixin, Base):
"""
Represents an Inventory Item ORM (Object-Relational Mapping) model.

    Attributes:
        __tablename__ (str): The name of the database table associated with this model.
    """
    __tablename__ = "inventory"

---
---
##../scs\core\db\periodic\inventory_item_orm_test.py:
import pytest
from scs.core.db.periodic.inventory_item_orm import InventoryItemORM

def test_inventory_item_orm_table_name():
assert InventoryItemORM.__tablename__ == "inventory"

def test_inventory_item_orm_inherits_base():
from scs.core.db.base import Base
assert issubclass(InventoryItemORM, Base)

def test_inventory_item_orm_inherits_period_mixin():
from scs.core.db.mixins.period_mixin import PeriodMixin
assert issubclass(InventoryItemORM, PeriodMixin)

def test_inventory_item_orm_period_column(db_session):

# Assign

inventory_item = InventoryItemORM(period=5)

    # Act
    db_session.add(inventory_item)
    db_session.commit()

    # Assert
    fetched_item = db_session.query(InventoryItemORM).filter_by(period=5).first()
    assert fetched_item is not None
    assert fetched_item.period == 5

---
---
##../scs\core\db\periodic\__init__.py:
from scs.core.db.periodic.demand_forecast_item_orm import DemandForecastItemORM
from scs.core.db.periodic.inventory_item_orm import InventoryItemORM

---
---
##../scs\core\db\process_models\process_input_orm.py:
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.base import Base
from scs.core.db.mixins.quantity_mixin import QuantityMixin

class ProcessInputORM(QuantityMixin, Base):
"""
Represents the ORM model for process input in the database.

    The ProcessInputORM class defines a model for storing input data associated with a
    process. It manages the relationship between processes and their inputs, allowing for
    joined loading and updates or deletions to be cascaded properly, ensuring seamless
    interaction with the underlying database.

    Attributes:
        __tablename__ (str): The name of the database table for this ORM model.
        process_id (int): The identifier of the associated process, acting as the primary key.
        process (ProcessORM): The relationship to the ProcessORM object, representing the
            associated process with joined loading.
    """
    __tablename__ = "process_input"
    process_id: Mapped[int] = mapped_column(
            ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    # noinspection PyUnresolvedReferences
    process: Mapped["ProcessORM"] = relationship(back_populates="inputs", lazy="joined")

---
---
##../scs\core\db\process_models\process_input_orm_test.py:
import pytest
from scs.core.db.process_models.process_input_orm import ProcessInputORM

@pytest.mark.usefixtures("db_session")
class TestProcessInputORM:

    def test_process_input_creation(self, db_session):
        # Assign
        new_process_input = ProcessInputORM(
                process_id=1,
                item_id=1001,
                quantity=10,
        )

        # Act
        db_session.add(new_process_input)
        db_session.commit()
        retrieved = db_session.query(ProcessInputORM).filter_by(process_id=1).one_or_none()

        # Assert
        assert retrieved is not None
        assert retrieved.process_id == 1
        assert retrieved.quantity == 10

    def test_process_input_cascades_on_delete(self, db_session):
        # Test setup must include creation of related ProcessORM (not implemented).
        # Ensures `ondelete="CASCADE"` works correctly with database handling.
        pass

    def test_process_relationship(self, db_session):
        # Test setup must include creation of related ProcessORM and respective relationship verification.
        pass

---
---
##../scs\core\db\process_models\process_orm.py:
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.graph.graph_node_orm import GraphNodeORM
from scs.core.db.workstation_orm import WorkstationORM

class ProcessORM(GraphNodeORM):
__tablename__ = "process"
__mapper_args__ = {"polymorphic_identity": "process"}

    id: Mapped[int] = mapped_column(
            ForeignKey(GraphNodeORM.id, onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True
    )
    graph_id: Mapped[int] = mapped_column(
            ForeignKey("material_graph.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    workstation_id: Mapped[int] = mapped_column(
            ForeignKey("workstation.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    process_duration_minutes: Mapped[int]
    setup_duration_minutes: Mapped[int]

    # noinspection PyUnresolvedReferences
    graph: Mapped["MaterialGraphORM"] = relationship(back_populates="processes", uselist=False, lazy="joined")
    # noinspection PyUnresolvedReferences
    inputs: Mapped[list["ProcessInputORM"]] = relationship(back_populates="process", lazy="joined")
    workstation: Mapped[WorkstationORM] = relationship(lazy="joined")
    # noinspection PyUnresolvedReferences
    output: Mapped["ProcessOutputORM"] = relationship(back_populates="process", uselist=False, lazy="joined")

---
---
##../scs\core\db\process_models\process_orm_test.py:

---
---
##../scs\core\db\process_models\process_output_orm.py:
from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.base import Base

class ProcessOutputORM(Base):
__tablename__ = "process_output"
process_id: Mapped[int] = mapped_column(
ForeignKey("process.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
)
item_id: Mapped[int] = mapped_column(
ForeignKey("item.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
)

    # noinspection PyUnresolvedReferences
    item: Mapped["ItemORM"] = relationship(lazy="joined")
    # noinspection PyUnresolvedReferences
    process: Mapped["ProcessORM"] = relationship(back_populates="output", lazy="joined")

---
---
##../scs\core\db\process_models\__init__.py:
from scs.core.db.process_models.process_input_orm import ProcessInputORM
from scs.core.db.process_models.process_orm import ProcessORM
from scs.core.db.process_models.process_output_orm import ProcessOutputORM

---
---
##../scs\core\domain\item_models.py:
from __future__ import annotations

import abc
import decimal
import logging

from pydantic import BaseModel, Field

class GraphNode(BaseModel, abc.ABC):
id: int = Field(ge=0, title="Unique identifier for a Graph Node", description="Used in the in the Material Graph")

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Item(GraphNode, abc.ABC):
pass

class BoughtItem(Item):
"""
Represents an item that has been bought.
Attributes:
base_price (float):
discount_amount (float):
mean_order_duration (float):
order_std_dev (float):
base_order_cost (float):
"""
base_price: decimal.Decimal = Field(ge=0, title="Base price of the item")
discount_amount: decimal.Decimal = Field(ge=0, title="Discount amount applied to the base price")
mean_order_duration: float = Field(ge=0, title="Average duration (in periods) it takes for an order of this item")
order_std_dev: float = Field(ge=0, title="Standard deviation of ordering durations (in periods)")
base_order_cost: float = Field(ge=0, title="Baseline cost associated with fulfilling orders for the item")

class ProducedItem(Item):
"""
Represents a produced item that extends the base functionality of an item.
Attributes:
id (int): unique identifier for the item.
"""
pass

---
---
##../scs\core\domain\process_domain_model.py:
from __future__ import annotations

from collections import Counter

from scs.core.domain.item_models import GraphNode, Item, ProducedItem
from scs.core.domain.ws_domain_model import Workstation

class Process(GraphNode):
process_duration: int
setup_duration: int
inputs: Counter[Item]
workstation: Workstation
output: ProducedItem

---
---
##../scs\core\domain\production_graph.py:
import networkx as nx

from scs.core.domain.graph.edge_models import WeightedEdge
from scs.core.domain.item_models import BoughtItem, GraphNode, ProducedItem
from scs.core.domain.process_domain_model import Process

class ProductionGraph:
def __init__(
self,
nx_di_graph: nx.DiGraph,
node_id_dict: dict[int, Process | BoughtItem | ProducedItem],
):
self._nx: nx.DiGraph = nx_di_graph
self._node_id_dict = node_id_dict

    def get_node_by_id(self, node_id: int) -> GraphNode:
        return self._node_id_dict[node_id]

    @property
    def nx_graph(self) -> nx.DiGraph:
        return self._nx

    @property
    def node_ids(self):
        return self.nx_graph.nodes

    @property
    def edges(self) -> list[WeightedEdge]:
        return [
                WeightedEdge(
                        from_node=self.get_node_by_id(from_node),
                        to_node=self.get_node_by_id(to_node),
                        weight=weight
                ) for from_node, to_node, weight in
                self.nx_graph.edges(data="weight", default=1)
        ]

    def out_degree(self, node: GraphNode) -> int:
        node_id = node.id
        return self.nx_graph.out_degree(node_id)

---
---
##../scs\core\domain\ws_domain_model.py:
from __future__ import annotations

from pydantic import BaseModel

class Workstation(BaseModel):
"""
Represents a workstation in the production system.
Attributes:
id: int
labour_cost_1: float
labour_cost_2: float
labour_cost_3: float
labour_overtime_cost: float
variable_machine_cost: float
fixed_machine_cost: float
"""
id: int
labour_cost_1: float
labour_cost_2: float
labour_cost_3: float
labour_overtime_cost: float
variable_machine_cost: float
fixed_machine_cost: float

---
---
##../scs\core\domain\__init__.py:

---
---
##../scs\core\domain\graph\edge_models.py:
import abc
from dataclasses import dataclass

from scs.core.domain.item_models import GraphNode, Item, ProducedItem
from scs.core.domain.process_domain_model import Process

@dataclass(frozen=True)
class WeightedEdge[T_from: GraphNode, T_to: GraphNode](abc.ABC):
"""
Represents a weighted edge connecting two nodes in a graph.

    This class is used to encapsulate the connection between two graph nodes. The
    connection includes the "from" node, the "to" node, and the weight of the edge
    representing the cost or distance of the connection. It is designed to be used
    as part of a graph data structure, where edges connect nodes and store
    additional information about the relationship between them.

    Attributes:
        from_node (T_from): The graph node where the edge originates.
        to_node (T_to): The graph node where the edge terminates.
        weight (int): The weight or cost associated with traversing this edge from
            the "from_node" to the "to_node".
    """
    from_node: T_from
    to_node: T_to
    weight: int

@dataclass(frozen=True)
class ProcessInputEdge(WeightedEdge[Item, Process]):
"""Represents an edge in a weighted graph connecting an Item and a Process.

    This class defines a frozen dataclass to model the edge between an Item
    and a Process in a weighted graph. It inherits properties and behavior from
    the base class WeightedEdge, leveraging the frozen attribute of the
    dataclass decorator to ensure immutability.
    Attributes:
    from_node (Item): The graph node where the edge originates.
    to_node (Process): The graph node where the edge terminates.
    weight (int): The weight or cost associated with traversing this edge from
        the "from_node" to the "to_node".
    """
    pass

@dataclass(frozen=True)
class ProcessOutputEdge(WeightedEdge[Process, ProducedItem]):
"""
Represents an edge in a graph that connects a process node to a produced item node.

    This class is used to define a weighted edge between a process (source) and a
    produced item (destination) in a graph representation. It is immutable and
    inherits from `WeightedEdge` with `Process` as the source type and
    `ProducedItem` as the destination type.

    Attributes:
    from_node (Process): The graph node where the edge originates.
    to_node (Produced): The graph node where the edge terminates.
    weight (int): The weight is 1;
    """
    weight: int = 1

    def __post_init__(self):
        if self.weight != 1:
            raise ValueError("Weight of ProcessOutputEdge must be 1.")

---
---
##../scs\core\domain\graph\edge_models_test.py:

# test_edge_models.py

from collections import Counter

import pytest

from scs.core.domain.item_models import Item, ProducedItem
from scs.core.domain.process_domain_model import Process
from scs.core.domain.ws_domain_model import Workstation
from .edge_models import ProcessInputEdge, ProcessOutputEdge, WeightedEdge

def test_process_input_edge_initialization():
edge = ProcessInputEdge(
from_node=Item(id=11),
to_node=Process(
id=11,
inputs=Counter({}),
workstation=Workstation(
id=11,
labour_overtime_cost=10,
labour_cost_3=2,
labour_cost_1=10,
fixed_machine_cost=20,
variable_machine_cost=22,
labour_cost_2=33
),
output=ProducedItem(id=11),
process_duration=10,
setup_duration=10
),
weight=10
)
assert edge.from_node is not None
assert edge.to_node is not None
assert edge.weight == 10

def test_process_output_edge_initialization_with_valid_weight(item_factory, process_factory):
edge = ProcessOutputEdge(
from_node=process_factory.create(id=202),
to_node=item_factory.create_produced_item(id=101),
)
assert edge.from_node is not None
assert edge.to_node is not None
assert edge.weight == 1

def test_process_output_edge_invalid_weight_raises_error(item_factory, process_factory):
with pytest.raises(ValueError):
ProcessOutputEdge(
from_node=process_factory.create(id=202),
to_node=item_factory.create_produced_item(id=101),
weight=2
)

def test_process_input_edge_with_minimum_valid_values():
item = Item(id=1)
process = Process(
id=1,
inputs=Counter({}),
workstation=Workstation(
id=1,
labour_overtime_cost=0,
labour_cost_3=0,
labour_cost_1=0,
fixed_machine_cost=0,
variable_machine_cost=0,
labour_cost_2=0
),
output=ProducedItem(id=1),
process_duration=0,
setup_duration=0
)
edge = ProcessInputEdge(from_node=item, to_node=process, weight=0)

    assert isinstance(edge, ProcessInputEdge)
    assert isinstance(edge, WeightedEdge)
    assert edge.from_node == item
    assert edge.to_node == process
    assert edge.weight == 0

---
---
##../scs\core\domain\graph\graph_validator.py:
---
##../scs\core\domain\graph\graph_validator_test.py:
import networkx as nx
import pytest

from scs.core.domain.graph.edge_models import ProcessInputEdge
from scs.core.domain.graph.graph_validator import GraphValidator
from scs.core.domain.item_models import ProducedItem
from scs.core.domain.production_graph import ProductionGraph

class DummyNode(ProducedItem):
def __init__(self, id):
super().__init__(id=id)

@pytest.fixture
def simple_graph():

# Nodes

nodes = {
1: DummyNode(1),
2: DummyNode(2),
3: DummyNode(3)
}

    # Graph
    g = nx.DiGraph()
    g.add_edge(1, 2, weight=1)
    g.add_edge(2, 3, weight=1)

    return ProductionGraph(g, nodes)

def test_no_cycle_valid(simple_graph):
validator = GraphValidator(simple_graph)
validator.validate()  # Should not raise

def test_cycle_detection():
g = nx.DiGraph()
g.add_edge(1, 2, weight=1)
g.add_edge(2, 3, weight=1)
g.add_edge(3, 1, weight=1)

    nodes = {i: DummyNode(i) for i in [1, 2, 3]}
    graph = ProductionGraph(g, nodes)

    validator = GraphValidator(graph)

    with pytest.raises(ValueError):
        validator.validate()

def test_isolated_node_detection():
g = nx.DiGraph()
g.add_edge(1, 2)
g.add_node(3)  # isolated

    nodes = {i: DummyNode(i) for i in [1, 2, 3]}
    graph = ProductionGraph(g, nodes)

    validator = GraphValidator(graph)

    with pytest.raises(ValueError):
        validator.validate()

def test_invalid_out_degree(monkeypatch):
g = nx.DiGraph()
g.add_edge(1, 2, weight=1)
g.add_edge(1, 3, weight=1)  # node 1 has two outgoing edges

    nodes = {i: DummyNode(i) for i in [1, 2, 3]}
    graph = ProductionGraph(g, nodes)

    # Patch edges to simulate ProcessInputEdge
    # noinspection PyUnusedLocal
    @property
    def mock_edges(self):
        return [ProcessInputEdge(from_node=nodes[1], to_node=nodes[2], weight=1)]

    monkeypatch.setattr(ProductionGraph, "edges", mock_edges)

    validator = GraphValidator(graph)

    with pytest.raises(RuntimeError):
        validator.validate()

---
---
##../scs\core\domain\graph\nx_graph_builder.py:
import networkx as nx

from scs.core.domain.item_models import GraphNode
from scs.core.domain.process_domain_model import Process

class NxGraphBuilder:
def __init__(self):
self.graph = nx.DiGraph()

    def add_edge(self, from_node: GraphNode, to_node: GraphNode, weight: int = 1):
        self.graph.add_node(from_node)
        self.graph.add_node(to_node)
        self.graph.add_edge(from_node.id, to_node.id, weight=weight)

    def build_from_database(self, processes: list[Process]) -> nx.DiGraph:
        for process in processes:
            for inp, quantity in process.inputs.items():
                self.add_edge(inp, process, weight=quantity)
            self.add_edge(process, process.output)
        return self.graph

---
---
##../scs\core\domain\graph\__init__.py:

---
---
##../scs\core\domain\periodic_quantities\periodic_item_quantities.py:
import dataclasses
from collections import Counter
from typing import Iterable

from scs.core.domain.item_models import Item

@dataclasses.dataclass
class PeriodicItemQuantity:
_data: dict[int, dict[Item, int]]

    def has_continuous_periods(self) -> bool:
        return all(
                [
                        period in self.get_periods()
                        for period in range(self.lowest_period, self.highest_period + 1)
                ]
        )

    def __assert_each_period_has_same_items(self):
        items = self.get_unique_items()
        if any(items != set(self._data[period].keys()) for period in self.get_periods()):
            raise ValueError(f"Items are not the same in every period !")

    def __post_init__(self):
        self.__assert_each_period_has_same_items()

    @property
    def highest_period(self):
        return max(self.get_periods())

    @property
    def lowest_period(self):
        return min(self.get_periods())

    def cut_off_periods_lower_than(self, period_cutoff: int):
        assert self.has_continuous_periods()
        new_data: dict[int, dict[Item, int]] = {}
        for period, item_counts in self._data.items():
            if period >= period_cutoff:
                new_data[period] = item_counts
        return PeriodicItemQuantity(new_data)

    def with_starting_period(self, starting_period: int = 1):
        assert self.has_continuous_periods()
        new_data: dict[int, dict[Item, int]] = {}
        for period, item_counts in self._data.items():
            new_data[(period - self.lowest_period) + starting_period] = self._data[period]
        return PeriodicItemQuantity(new_data)

    def has_period(self, period: int) -> bool:
        return period in self._data

    def add_period(self, item_counts: dict[Item, int]):
        self._data[self.highest_period + 1] = item_counts

    def get_counters(self, period: int) -> Counter[Item]:
        return Counter(self._data[period])

    def get_value_for_item(self, period: int, item: Item) -> int:
        return self._data[period][item]

    def get_unique_items(self) -> set[Item]:
        items = set()
        for item_counter in self._data.values():
            items.update(item_counter.keys())
        return items

    def get_periods(self) -> list[int]:
        return sorted(self._data.keys())

    def get_average_value(self, item: Item) -> float:
        return sum(self._data[t][item] for t in self.get_periods()) / len(self.get_periods())

    def get_average_values(self) -> dict[Item, float]:
        return {item: self.get_average_value(item) for item in self.get_unique_items()}

    def sum(self):
        return sum(sum(item_counts.values()) for item_counts in self._data.values())

    def items(self) -> Iterable[tuple[int, dict[Item, int]]]:
        return self._data.items()

---
---
##../scs\core\domain\periodic_quantities\periodic_item_quantities_builder.py:
from collections import Counter

from scs.core.domain.item_models import Item
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity

class PeriodicItemQuantityBuilder:
def __init__(self):
self.periodic_item_quantity: dict[int, dict[Item, int]] = {}

    def add_product(self, item: Item, product_counts: list[int]):
        for period, count in enumerate(product_counts):
            period += 1
            if period not in self.periodic_item_quantity:
                self.periodic_item_quantity[period] = Counter[Item]()
            self.periodic_item_quantity[period][item] = count
        return self

    def build(self):
        return PeriodicItemQuantity(self.periodic_item_quantity)

---
---
##../scs\core\domain\periodic_quantities\__init__.py:

---
---
##../scs\core\mapper\base_mapper.py:
import abc

from pydantic import BaseModel

from scs.core.db.base import Base

class BaseMapper[T_ORM: Base, T_Domain: BaseModel](abc.ABC):
"""
Base class for mappers that convert between ORM models and domain models.
"""

    @abc.abstractmethod
    def convert_to_domain(self, orm_model: T_ORM) -> T_Domain:
        """
        Convert an ORM model to its domain representation.
        :param orm_model: The ORM model to convert.
        :return: The domain representation of the ORM model.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abc.abstractmethod
    def convert_to_orm(self, domain_model: T_Domain) -> T_ORM:
        """
        Convert a domain model to its ORM representation.
        :param domain_model: The domain model to convert.
        :return: The ORM representation of the domain model.
        """
        raise NotImplementedError("Subclasses must implement this method.")

---
---
##../scs\core\mapper\workstation_mapper.py:
from scs.core.db.workstation_orm import WorkstationORM
from scs.core.domain.ws_domain_model import Workstation
from scs.core.mapper.base_mapper import BaseMapper

class WorkstationMapper(BaseMapper[WorkstationORM, Workstation]):
def convert_to_domain(self, orm_obj: WorkstationORM) -> Workstation:
return Workstation(
id=orm_obj.id,
labour_cost_1=orm_obj.labour_cost_1,
labour_cost_2=orm_obj.labour_cost_2,
labour_cost_3=orm_obj.labour_cost_3,
fixed_machine_cost=orm_obj.fixed_machine_cost,
variable_machine_cost=orm_obj.variable_machine_cost,
labour_overtime_cost=orm_obj.labour_overtime_cost,
)

    def convert_to_orm(self, domain_obj):
        pass

---
---
##../scs\core\mapper\__init__.py:

---
---
##../scs\core\mapper\graph_node\bought_item_mapper.py:
from scs.core.db.item_models import BoughtItemORM
from scs.core.domain.item_models import BoughtItem
from scs.core.mapper.base_mapper import BaseMapper

class BoughtItemMapper(BaseMapper[BoughtItemORM, BoughtItem]):
def convert_to_domain(self, orm_obj: BoughtItemORM) -> BoughtItem:
return BoughtItem(
id=orm_obj.id,
base_price=orm_obj.base_price,
discount_amount=orm_obj.discount_amount,
mean_order_duration=orm_obj.mean_order_duration,
order_std_dev=orm_obj.order_std_dev,
base_order_cost=orm_obj.base_order_cost,
)

    def convert_to_orm(self, domain_obj):
        raise NotImplementedError("Conversion from domain to ORM is not implemented.")

---
---
##../scs\core\mapper\graph_node\graph_node_mapper.py:
from scs.core.db.graph.graph_node_orm import GraphNodeORM
from scs.core.db.process_models import ProcessORM
from scs.core.domain.item_models import GraphNode
from scs.core.domain.process_domain_model import Process
from scs.core.mapper.base_mapper import BaseMapper
from scs.core.mapper.graph_node.process_mapper import ProcessMapper

class GraphNodeMapper(BaseMapper[GraphNodeORM, GraphNode]):
def __init__(self, process_mapper: ProcessMapper, item_mapper: Item):
self.workstation_repository = workstation_repository

    def convert_to_domain(self, node: GraphNodeORM):
        """
        Convert a graph node to its domain representation.
        :param node: The graph node to convert.
        :return: The domain representation of the graph node.
        """
        if not isinstance(node, GraphNodeORM):
            raise TypeError(f"Expected GraphNodeORM, got {type(node)}")

        if isinstance(node, ProcessORM):
            return Process(
                    id=node.id,
                    workstation=self.workstation_repository.get_by_id()
            )

    def convert_to_orm(self, domain: GraphNode) -> GraphNodeORM:
        # ...placeholder mapping...
        return GraphNodeORM(id=domain.id)

---
---
##../scs\core\mapper\graph_node\item_mapper.py:
from scs.core.db.item_models.bought_item_orm import BoughtItemORM
from scs.core.db.item_models.item_orm import ItemORM
from scs.core.domain.item_models import Item
from scs.core.mapper.base_mapper import BaseMapper
from scs.core.mapper.graph_node.bought_item_mapper import BoughtItemMapper

class ItemNodeMapper(BaseMapper[ItemORM, Item]):
def __init__(self, bought_item_mapper: BoughtItemMapper, produced_item_mapper: BoughtItemORM):
self.bought_item_mapper = bought_item_mapper
self.produced_item_mapper = produced_item_mapper

    def convert_to_domain(self, orm_obj):
        if isinstance(orm_obj, BoughtItemORM):
            return
        pass

    def convert_to_orm(self, domain_obj):
        # ...placeholder mapping...
        pass

---
---
##../scs\core\mapper\graph_node\process_mapper.py:
from scs.core.db.process_models import ProcessORM
from scs.core.domain.process_domain_model import Process
from scs.core.mapper.base_mapper import BaseMapper
from scs.core.mapper.workstation_mapper import WorkstationMapper

class ProcessMapper(BaseMapper[ProcessORM, Process]):
def __init__(self, workstation_mapper: WorkstationMapper):
self.workstation_mapper = workstation_mapper

    def convert_to_orm(self, domain_model: Process) -> ProcessORM:
        raise NotImplementedError("Conversion from domain to ORM is not implemented.")

    def convert_to_domain(self, orm_model: ProcessORM) -> Process:
        workstation_domain = self.workstation_mapper.convert_to_domain(orm_model.workstation)
        return Process(
                id=orm_model.id,
                workstation=workstation_domain,
                setup_duration=orm_model.setup_duration_minutes,
                process_duration=orm_model.process_duration_minutes,
                inputs=orm_model.inputs,
                output=orm_model.outputs,
        )

---
---
##../scs\core\mapper\graph_node\produced_item_mapper.py:
from scs.core.db.item_models import ProducedItemORM
from scs.core.domain.item_models import ProducedItem
from scs.core.mapper.base_mapper import BaseMapper

class ProducedItemMapper(BaseMapper[ProducedItemORM, ProducedItem]):

    def convert_to_domain(self, orm_model: ProducedItemORM) -> ProducedItem:
        return ProducedItem(
                id=orm_model.id,
        )

    def convert_to_orm(self, domain_model: ProducedItem) -> ProducedItemORM:
        raise NotImplementedError("Conversion from domain to ORM is not implemented.")

---
---
##../scs\core\mapper\graph_node\__init__.py:

---
---
##../scs\core\repos\bought_item_repo.py:
from sqlalchemy.orm import Session

from scs.core.db.item_models.bought_item_orm import BoughtItemORM
from scs.core.repos.mixins.id_repo_mixin import IdRepoMixin

class BoughtItemRepository(IdRepoMixin[BoughtItemORM]):
def __init__(self, session: Session):
self.session = session

---
---
##../scs\core\repos\demand_forecast_repo.py:
from sqlalchemy.orm import Session

from scs.core.db.periodic.demand_forecast_item_orm import DemandForecastItemORM
from scs.core.repos.mixins.period_qty_mixin import PeriodQtyMixin

class DemandForecastRepository(PeriodQtyMixin[DemandForecastItemORM]):
def __init__(self, session: Session):
self.session = session

    def get_forecast_starting_with(self, first_period: int):
        return (
                DemandForecastItemORM
                .get_periodic_item_quantity(self.session)
                .cut_off_periods_lower_than(first_period)
                .with_starting_period()
        )

---
---
##../scs\core\repos\inv_repo.py:
from collections import Counter

import sqlalchemy

from scs.core.db.periodic import InventoryItemORM
from scs.core.domain.item_models import Item

class InventoryRepo:
def __init__(self, session: sqlalchemy.orm.Session):
self.session = session

    def get_inventory_for_period(self, period: int) -> Counter[Item]:
        """
        Get the inventory for a specific period.

        :param period: The period for which to get the inventory.
        :return: A Counter of Item objects with their quantities.
        """
        return InventoryItemORM.load_as_counter(self.session, period)

---
---
##../scs\core\repos\mat_graph_repository.py:
import typing

from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.graph.material_graph_orm import MaterialGraphORM
from scs.core.db.process_models import ProcessORM

class MaterialGraphRepository:
def __init__(self, session: Session):
self.session = session

    def load_processes(self):
        return self.session.execute(
                select(ProcessORM)
        ).unique().scalars().all()

    def load_bought_items(self):
        return self.session.execute(
                select(BoughtItemORM)
        ).unique().scalars().all()

    def load_produced_items(self):
        return self.session.execute(
                select(ProducedItemORM)
        ).unique().scalars().all()

    def get_graph_node_dict(self) -> dict[int, ProcessORM | BoughtItemORM | ProducedItemORM]:
        return {typing.cast(int, graph_node.id): graph_node for graph_node in
                list(self.load_bought_items()) + list(self.load_processes()) + list(self.load_produced_items())}

    def get_item(self, item_id: int) -> ItemORM:
        item = self.session.get(ItemORM, item_id)
        if item is None:
            raise ValueError(f"Item {item_id} not found")
        return typing.cast(item, ItemORM)

    def load_material_graph_root(self) -> MaterialGraphORM:
        stmt = select(MaterialGraphORM).where(MaterialGraphORM.parent_graph_id.is_(None))
        root = self.session.execute(stmt).unique().scalars().one_or_none()
        if root is None:
            raise ValueError("No root MaterialGraph found (parent_graph_id IS NULL)")
        return root

---
---
##../scs\core\repos\process_repository.py:
class ProcessRepository:
def __init__(self, session: Session):
self.session = session

    def get_by_id(self, id: int) -> ProcessDomain:
        proc = self.session.query(Process).filter(Process.id == id).one()
        mg_repo = MaterialGraphRepository(self.session)
        ws_repo = WorkstationRepository(self.session)
        inputs = [ProcessInputDomain(
                process_id=inp.process_id,
                quantity=inp.quantity,
                process=None
        ) for inp in proc.inputs]
        out = None
        if proc.output:
            out = ProcessOutputDomain(
                    process_id=proc.output.process_id,
                    item_id=proc.output.item_id,
                    item=ItemDomain(id=proc.output.item.id),
                    process=None
            )
        return ProcessDomain(
                id=proc.id,
                graph_id=proc.graph_id,
                workstation_id=proc.workstation_id,
                process_duration=proc.process_duration_minutes,
                setup_duration=proc.setup_duration_minutes,
                graph=mg_repo.get_by_id(proc.graph_id),
                inputs=inputs,
                workstation=ws_repo.get_by_id(proc.workstation_id),
                output=out
        )

---
---
##../scs\core\repos\ws_repo.py:
from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.workstation_orm import WorkstationORM
from scs.core.domain.ws_domain_model import Workstation

class WorkstationRepository:
def __init__(self, session: Session):
self.session = session

    def get_by_id(self, id: int) -> Workstation:
        ws = self.session.execute(select(WorkstationORM).filter_by(id=id)).scalars().one()
        return Workstation(
                id=ws.id,
                labour_cost_1=ws.labour_cost_1,
                labour_cost_2=ws.labour_cost_2,
                labour_cost_3=ws.labour_cost_3,
                labour_overtime_cost=ws.labour_overtime_cost,
                variable_machine_cost=ws.variable_machine_cost,
                fixed_machine_cost=ws.fixed_machine_cost
        )

---
---
##../scs\core\repos\__init__.py:

---
---
##../scs\core\repos\mixins\id_repo_mixin.py:
import abc

import sqlalchemy

from scs.core.db.mixins import IdMixin

class IdRepoMixin[T: IdMixin](abc.ABC):
def __init__(self, session: sqlalchemy.orm.Session):
self.session = session

    def find_by_id(self, id: int) -> T | None:
        return self.session.execute(
                sqlalchemy.select(T).filter_by(id=id)
        ).scalars().one_or_none()

---
---
##../scs\core\repos\mixins\period_qty_mixin.py:
import collections
from collections import Counter
from typing import Optional

from scs.core.db.mixins.period_mixin import PeriodMixin
from scs.core.db.mixins.quantity_mixin import QuantityMixin
from scs.core.domain.item_models import Item
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity
from scs.core.repos.mixins.period_repo_mixin import PeriodRepoMixin

class PeriodQtyMixin[T: (PeriodMixin, QuantityMixin)](PeriodRepoMixin[T]):
def load_as_counter(self, period: Optional[int] = None) -> Counter[Item]:
rows: collections.Iterable[T] = self.find_by_period(period)
return Counter({row.item: row.quantity for row in rows})

    def get_periodic_item_quantity(self) -> PeriodicItemQuantity:
        # Load all rows and convert them to a PeriodicItemQuantity
        return PeriodicItemQuantity(
                {
                        period: self.load_as_counter(period)
                        for period in self.unique_periods()
                }
        )

---
---
##../scs\core\repos\mixins\period_repo_mixin.py:
import abc
import collections
import typing
from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.mixins.period_mixin import PeriodMixin

class PeriodRepoMixin[T: PeriodMixin](abc.ABC):
def __init__(self, session: Session):
self.session: Session = session

    def find_by_period(self, period: int) -> collections.Iterable[T]:
        return self.session.execute(
                select(T).filter_by(period=period)
        ).scalars().all()

    def unique_periods(self) -> Iterable[int]:
        all_ts: Iterable[T] = self.session.execute(select(T)).scalars().all()
        return {typing.cast(int, row.period) for row in all_ts}

---
---
##../scs\core\repos\mixins\__init__.py:

---
---
##../scs\di\__init__.py:

---
---
##../scs\graph\__init__.py:

---
---
##../scs\graph\core\production_graph_prune.py:
class NetworkXGraphPrune:
def prune_singleton_produced_items(self):
to_remove = []
for node in list(self.nx.node_ids):
node_data = self.nx.node_ids[node].get("data")

# Only consider nodes representing an ItemORM that is produced.

if isinstance(node_data, Item):
in_edges = list(self.nx.in_edges(node, data="weight"))
out_edges = list(self.nx.out_edges(node, data="weight"))

# Only prune produced items with exactly one incoming and one outgoing edge, both with weight 1.

if len(in_edges) == 1 and len(out_edges) == 1:
if in_edges[0][2] == 1 and out_edges[0][2] == 1:
pred = in_edges[0][0]
succ = out_edges[0][1]

# Reconnect predecessor to successor.

self.nx.add_edge(pred, succ, weight=1)
to_remove.append(node)
self.nx.remove_nodes_from(to_remove)

---
---
##../scs\graph\core\__init__.py:

---
---
##../scs\graph\visualization\main.py:
from material.db.config import engine
from material.graph.production_graph.database_graph_loader import DatabaseGraphLoader
from material.graph.production_graph.production_graph import ProductionGraph
from material.graph.visualization.mermaid_visualizations import NxToMermaid

if __name__ == '__main__':
from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        loader = DatabaseGraphLoader(session)
        prod_graph = ProductionGraph(loader)

        # Prune singleton produced item nodes in the NX graph.
        prod_graph.prune_singleton_produced_items()

        # Build the visualization material graph (which will include only processes that remain in the pruned NX graph).
        viz_material_graph = prod_graph.build_visualization_material_graph()

        # Now pass both prod_graph._nx and viz_material_graph to your Mermaid exporter.
        mermaid_code = NxToMermaid(viz_material_graph).nx_to_mermaid("Graph New")
        print(mermaid_code)

---
---
##../scs\graph\visualization\mermaid_visualizations.py:
import abc
import re
import typing
from abc import abstractmethod
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass

import networkx as nx
import yaml

from material.db.models.models import MaterialGraphORM, BoughtItem, Process, ProducedItem

class VisualizationMaterialGraph:
def __init__(self, orm_node: MaterialGraphORM, nx_graph: nx.DiGraph):
self.id = orm_node.id
self.name = orm_node.name
self.processes = []
for process in orm_node.processes:
process_node_id = f"{process.id}"
if nx_graph.has_node(process_node_id):
self.processes.append(process)
self.subgraphs = [
VisualizationMaterialGraph(child, nx_graph)
for child in orm_node.subgraphs
]

class MermaidContent(abc.ABC):
@abstractmethod
def get_mermaid_content(self):
pass

@dataclass
class ClassDef(MermaidContent):
name: str
fill: str
stroke: str
stroke_width: str
color: str

    def get_mermaid_content(self):
        return (f"classDef {self.name} "
                f"fill:{self.fill},"
                f"stroke:{self.stroke},"
                f"stroke-width:{self.stroke_width},"
                f"color:{self.color}")

class MermaidClass(MermaidContent):
def __init__(self, class_def: ClassDef):
self.class_def = class_def
self.nodes = []

    def assign_node(self, node_uid):
        return self.nodes.append(node_uid)

    def get_mermaid_content(self):
        return f"{self.class_def.get_mermaid_content()}\n class {', '.join(self.nodes)} {self.class_def.name}"

class MermaidStringBuilder(MermaidContent):
def __init__(self, indent_level=0):
self._lines = []
self._indent_level = indent_level
self._indent_str = "    "  # 4 spaces per indent level

    def init_mermaid(self, settings: dict[str, str | dict], diagram_type: str):
        self.add_lines(self.create_settings_lines(settings))
        self.add_line(diagram_type)
        self._indent_level += 1

    def create_settings_lines(self, settings: dict[str, str]) -> list[str]:
        return ["---"] + yaml.dump(settings).split("\n") + ["---"] + [""]

    def add_line(self, content):
        self._lines.append(f"{self._indent_str * self._indent_level}{content}")

    def add_lines(self, contents: list[str]):
        for content in contents:
            self.add_line(content)

    @contextmanager
    def create_subgraph(self, subgraph_name: str, direction="TB"):
        """Creates a subgraph context."""
        self.add_line(f"subgraph {subgraph_name}")
        self.add_line(f"direction {direction}")
        self._indent_level += 1
        try:
            yield self
        finally:
            self._indent_level -= 1
            self.add_line("end")

    def add_node(self, node_id: str, label: str):
        """Adds a node to the diagram."""
        self.add_line(f"{node_id}[\"{label}\"]")

    def add_rounded_node(self, node_id: str, label: str):
        """Adds a rounded node to the diagram."""
        self.add_line(f"{node_id}(({label}))")

    def add_arrow(self, from_node: str, to_node: str, label: str = ""):
        """Adds an arrow between two nodes, with an optional label."""
        arrow = f"{from_node} --{label}--> {to_node}" if label else f"{from_node} --> {to_node}"
        self.add_line(f"{arrow}")

    def get_mermaid_content(self):
        return "\n".join(self._lines)

class NxToMermaid:
def __init__(self, graph: VisualizationMaterialGraph):
self.graph: VisualizationMaterialGraph = graph
self.mermaid = MermaidStringBuilder()
self.duplicate_bought_nodes: Counter[BoughtItem] = Counter()
settings = {
"title": "Material Flow",
"config": {
"theme": "dark",
"themeVariables": {"darkMode": True},
"flowchart": {
"curve": "linear",
"defaultRenderer": "elk",
},
}
}
self.mermaid.init_mermaid(settings, "flowchart LR")
self.class_defs: dict[str, MermaidClass] = {}
self._unique_nodes: set[str] = set()

    def _add_process_node(self, node: Process):
        label = f"<b>{node.workstation_id}</b>"
        node_id = str(node.id)
        if node_id not in self._unique_nodes:
            self._unique_nodes.add(node_id)
            self.mermaid.add_node(node_id, label)
        return node_id

    def _add_produced_item_node(self, produced_item: ProducedItem):
        node_id = "E" + str(produced_item.item_id)
        if node_id not in self._unique_nodes:
            self._unique_nodes.add(node_id)
            self.mermaid.add_rounded_node(node_id, node_id)
        return node_id

    def __get_unique_bought_node_id(self, node: BoughtItem):
        current_count = self.duplicate_bought_nodes.get(node, 0)
        self.duplicate_bought_nodes[node] = current_count + 1
        return "K" + str(node.item_id) + f"{current_count}"

    def _add_bought_item_node(self, bought_item: BoughtItem):
        node_id = self.__get_unique_bought_node_id(bought_item)
        self.mermaid.add_rounded_node(node_id, str(bought_item.item_id))
        return node_id

    def add_item(self, item):
        if item.is_bought():
            return self._add_bought_item_node(item.bought)
        elif item.is_produced():
            return self._add_produced_item_node(item.produced)
        raise ValueError(f"Item type {type(item)} not recognized")

    def add_class_assignment(self, node_id: str, class_id: str):
        self.class_defs[class_id].assign_node(node_id)

    def add_class_definition(self, class_def: ClassDef):
        self.class_defs[class_def.name] = MermaidClass(class_def)

    def add_processes(self, processes: typing.Collection[Process]):
        for process in processes:
            self._add_process_node(process)
            for input_item in process.inputs:
                input_item_id = self.add_item(input_item.item)
                self.mermaid.add_arrow(input_item_id, str(process.id))
            output_item_id = self.add_item(process.output.item)
            self.mermaid.add_arrow(str(process.id), output_item_id)

    def add_subgraph(self, subgraph: VisualizationMaterialGraph):
        with self.mermaid.create_subgraph(subgraph.name):
            self.add_processes(subgraph.processes)
            for sub_graph in subgraph.subgraphs:
                self.add_subgraph(sub_graph)

    def get_mermaid_content(self):
        for subgraph in self.graph.subgraphs:
            self.add_subgraph(subgraph)
        return self.mermaid.get_mermaid_content()

    def save_html(self, mermaid_code, graph_name):
        with open(f"diagrams/template.html", encoding="utf-8") as f:
            html = f.read()
        result = re.sub(r"{{\s*mermaidContent\s*}}", mermaid_code, html)
        result = re.sub(r"{{\s*diagram_title\s*}}", graph_name, result)
        with open(f"diagrams/diagram_{graph_name}.html", "w", encoding="utf-8") as f:
            f.write(result)

    def save_mmd(self, diagram_code, graph_name):
        with open(f"diagrams/diagram_{graph_name}.mmd", "w", encoding="utf-8") as f:
            f.write(diagram_code)

    def nx_to_mermaid(self, name: str):
        content = self.get_mermaid_content()
        self.save_mmd(content, name)
        self.save_html(content, name)

---
---
##../scs\graph\visualization\__init__.py:

---
---
##../scs\tests\item_factory.py:
import random
from decimal import Decimal

from scs.core.domain.item_models import BoughtItem, ProducedItem

class ItemFactory:
def create_bought_item(
self,
id: int | None = None,
base_price: int | None = None,
discount_amount: int | None = None,
mean_order_duration: float | None = None,
order_std_dev: float | None = None,
base_order_cost: int | None = None
) -> BoughtItem:
return BoughtItem(
id=id or random.randint(1, 10 ** 8),
base_price=base_price or Decimal(random.randint(1, 10 ** 1)),
discount_amount=discount_amount or Decimal(random.randint(1, 10 ** 4)),
mean_order_duration=mean_order_duration or random.random(),
order_std_dev=order_std_dev or random.random(),
base_order_cost=base_order_cost or random.randint(1, 10 ** 4),
)

    def create_produced_item(self, id: int | None = None) -> ProducedItem:
        return ProducedItem(
                id=id or random.randint(1, 10 ** 8),
        )

---
---
##../scs\tests\process_factory.py:
import random
from collections import Counter

from scs.core.domain.item_models import Item, ProducedItem
from scs.core.domain.process_domain_model import Process
from scs.core.domain.ws_domain_model import Workstation
from scs.tests.item_factory import ItemFactory
from scs.tests.workstation_factory import WorkstationFactory

class ProcessFactory:
def __init__(self, workstation_factory: WorkstationFactory, item_factory: ItemFactory):
self.workstation_factory = workstation_factory
self.item_factory = item_factory

    def create(
            self,
            id: int | None = None,
            process_duration: int | None = None,
            setup_duration: int | None = None,
            inputs: Counter[Item] = None,
            workstation: Workstation = None,
            output: ProducedItem = None
    ):
        if inputs is None:
            inputs = Counter()

        if workstation is None:
            workstation = self.workstation_factory.create_workstation()

        if output is None:
            output = self.item_factory.create_produced_item()
        return Process(
                id=id or random.randint(1, 10 ** 8),
                process_duration=process_duration or random.randint(1, 10 ** 4),
                setup_duration=setup_duration or random.randint(1, 10 ** 4),
                inputs=inputs,
                workstation=workstation,
                output=output,
        )

---
---
##../scs\tests\workstation_factory.py:
import random

from scs.core.domain.ws_domain_model import Workstation

class WorkstationFactory:
def create_workstation(
self,
id: int | None = None,
labour_cost_1: float | None = None,
labour_cost_2: float | None = None,
labour_cost_3: float | None = None,
labour_overtime_cost: float | None = None,
variable_machine_cost: float | None = None,
fixed_machine_cost: float | None = None,
):
return Workstation(
id=id or random.randint(1, 10 ** 8),
labour_cost_1=labour_cost_1 or random.uniform(0, 100),
labour_cost_2=labour_cost_2 or random.uniform(0, 100),
labour_cost_3=labour_cost_3 or random.uniform(0, 100),
labour_overtime_cost=labour_overtime_cost or random.uniform(0, 100),
variable_machine_cost=variable_machine_cost or random.uniform(0, 100),
fixed_machine_cost=fixed_machine_cost or random.uniform(0, 100),
)

---
---
##../scs\tests\__init__.py:

---