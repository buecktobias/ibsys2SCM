from collections import defaultdict, Counter

from pyomo.environ import SolverFactory, value

from scs.calc.primary_production.lp_model.lp_model_builder import ProductionPlanningModelBuilder
from scs.calc.primary_production.lp_model.planner_attributes import ProductionPlanningAttributes
from scs.calc.primary_production.lp_model.planner_solution import ProductionSolutionData
from scs.db.models.item import Item
from scs.db.models.mixins.periodic_item_quantity import PeriodicItemQuantity


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
        prod_plan: dict[int, ItemCounter] = defaultdict(Counter[Item])
        inv_plan: dict[int, ItemCounter] = defaultdict(Counter[Item])

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
