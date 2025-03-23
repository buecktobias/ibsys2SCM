from collections import defaultdict

from pyomo.environ import SolverFactory, value

from material.calc.primary_demand.primary_production_solution_data import ProductionSolutionData
from material.calc.primary_demand.production_planning_attributes import ProductionPlanningAttributes
from material.calc.primary_demand.production_planning_model_builder import ProductionPlanningModelBuilder
from material.core.resource_counter import ItemCounter
from material.db.models.periodic_item_quantity import PeriodicItemQuantity


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
           inv_a, inv_b, prod_fixed, prod_var, smoothing_factor, max_period_production
        """
        self.attrs = attrs
        self.model = None
        self.solver_results = None

    def solve(self,
              demand_forecast: PeriodicItemQuantity,
              init_inventory: ItemCounter
              ) -> ProductionSolutionData:
        """
        Build and solve the production plan with the given demand and inventory.

        :param demand_forecast: e.g. {1:{'P1':80,'P2':40}, 2:{'P1':50,...},...}
        :param init_inventory: e.g. {'P1':10,'P2':5}
        :return: ProductionSolutionData with production, inventory, costs, revenue, objective
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
        prod_plan: dict[int, ItemCounter] = defaultdict(ItemCounter)
        inv_plan: dict[int, ItemCounter] = defaultdict(ItemCounter)

        for (t, i) in model.P.keys():
            prod_plan[t][i] = int(round(value(model.P[t, i])))

        for (t, i) in model.Inv.keys():
            inv_plan[t][i] = int(round(value(model.Inv[t, i])))

        sol_data = ProductionSolutionData(
            demand=demand_forecast,
            production=PeriodicItemQuantity(prod_plan),
            inventory=PeriodicItemQuantity(inv_plan),
            production_cost=value(model.production_cost),
            inventory_cost=value(model.inventory_cost),
            variance_penalty=value(model.production_variance),
            revenue=value(model.revenue),
            objective=value(model.Obj)
        )
        return sol_data
