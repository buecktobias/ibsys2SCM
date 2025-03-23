from pyomo import environ as pyo
# noinspection PyUnresolvedReferences
from pyomo.core import ConcreteModel, Var, Constraint, NonNegativeReals

from material.calc.primary_demand.production_planning_attributes import ProductionPlanningAttributes
from material.core.resource_counter import ItemCounter
from material.db.models.item import Item
from material.db.models.periodic_item_quantity import PeriodicItemQuantity


class ProductionPlanningModelBuilder:
    """
    Responsible for taking the planning data (forecasts, inventory, cost attributes)
    and building a Pyomo model.
    """

    def __init__(self,
                 attrs: ProductionPlanningAttributes,
                 demand_forecast: PeriodicItemQuantity,
                 init_inventory: ItemCounter
                 ):
        """
        :param attrs: ProductionPlanningAttributes dataclass instance
        :param demand_forecast: e.g. {1: {Item1: 50, Item2:30}, 2:{...}}
        :param init_inventory: e.g. {Item1: 50, Item2:30}
        """
        if 0 in demand_forecast:
            raise ValueError("Period 0 is reserved for initial inventory, so it should not be in the forecast.")

        if 1 not in demand_forecast:
            raise ValueError("Period 1 must be in the forecast.")

        if len(init_inventory) != len(demand_forecast[1]):
            raise ValueError("Initial inventory and demand forecast must have the same products.")

        self.attrs: ProductionPlanningAttributes = attrs
        self.demand_forecast: PeriodicItemQuantity = demand_forecast
        self.init_inventory: ItemCounter = init_inventory

        # Derive sets from the forecast:
        self._periods = sorted(demand_forecast.keys())
        self._products: list[Item] = []
        for period in self._periods:
            self._products.extend(demand_forecast[period].keys())
        self._products = sorted(set(self._products))

    @property
    def extended_periods(self):
        """
        Extend the periods by 1 to include the initial inventory period.
        """
        return [0] + self._periods

    def build_pyomo_model(self):
        model: ConcreteModel = ConcreteModel("ProductionPlan")

        # 1) Variables
        # P[period, item] = production
        # Inv[period, item] = inventory
        # We'll iterate over self._periods, self._products
        model.P = Var(((t, i) for t in self._periods for i in self._products),
                      domain=NonNegativeReals)
        model.Inv = Var(((t, i) for t in self.extended_periods for i in self._products),
                        domain=NonNegativeReals)

        # Set initial inventory
        for item, init_inv in self.init_inventory.items():
            model.Inv[0, item] = init_inv

        # 2) Constraints
        # (a) Inventory balance
        def inv_balance_rule(model: ConcreteModel, period: int, item: Item):
            return (model.Inv[period, item] ==
                    model.Inv[period - 1, item] + model.P[period, item] - self.demand_forecast[period][item])

        model.InvBalance = Constraint(list(model.P.keys()), rule=inv_balance_rule)

        # (b) Max production per period, if set
        def max_prod_rule(model: ConcreteModel, period: int):
            return sum(model.P[period, product] for product in self._products) <= self.attrs.max_period_production

        model.MaxProd = Constraint(self._periods, rule=max_prod_rule)

        # 3) Expressions

        @model.Expression()
        def total_production(mdl):
            return sum(mdl.P[t, i] for t in self._periods for i in self._products)

        @model.Expression()
        def production_cost(mdl):
            # fixed + var * total_production
            return (self.attrs.prod_fixed
                    + self.attrs.prod_var * mdl.total_production)

        @model.Expression()
        def inventory_cost(mdl):
            # sum_{item} [ inv_a + inv_b*( sum_{period}Inv[period,item] )^2 ]
            expr = 0.0
            for i in self._products:
                sum_inv_i = sum(mdl.Inv[t, i] for t in self._periods)
                expr += self.attrs.inv_a + self.attrs.inv_b * (sum_inv_i ** 2)
            return expr

        @model.Expression()
        def production_variance(mdl):
            """
            single factor for *all* products:
            sum_{item in products}( Var(P^item ) ) * smoothing_factor
            Var(P^item) = (1/|T|)* sum_{period} (P[period,item] - Pbar_i)^2
            Pbar_i = (1/|T|)* sum_{period} P[period,item]
            """
            Tlen = float(len(self._periods))
            total_var = 0.0
            for i in self._products:
                pbar_i = (1.0 / Tlen) * sum(mdl.P[t, i] for t in self._periods)
                sum_sq = 0.0
                for t in self._periods:
                    sum_sq += (mdl.P[t, i] - pbar_i) ** 2
                var_i = (1.0 / Tlen) * sum_sq
                total_var += var_i
            return self.attrs.smoothing_factor * total_var

        @model.Expression()
        def revenue(mdl):
            # Hard-coded example if you want a uniform price
            # or in real usage, you'd store a separate param for each product
            # For now let's just do 200 * total_production
            return 200.0 * mdl.total_production

        def obj_rule(mdl):
            # Maximize profit = revenue - (all cost terms)
            return (mdl.revenue
                    - (mdl.production_cost
                       + mdl.inventory_cost
                       + mdl.production_variance))

        model.Obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)
        return model
