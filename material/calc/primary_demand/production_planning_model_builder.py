from pyomo import environ as pyo
# noinspection PyUnresolvedReferences
from pyomo.core import ConcreteModel, Var, Constraint, NonNegativeReals

from material.calc.primary_demand.production_planning_attributes import ProductionPlanningAttributes
from material.core.resource_counter import ItemCounter
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
        self.attrs = attrs
        self.demand_forecast = demand_forecast
        self.init_inventory = init_inventory

        # Derive sets from the forecast:
        self._periods = sorted(demand_forecast.keys())  # e.g. [1,2,3,4]
        product_set = set()
        for period in self._periods:
            product_set.update(demand_forecast[period].keys())
        self._products: set[int] = product_set  # e.g. ['P1','P2']

    def build_pyomo_model(self):
        model = ConcreteModel("ProductionPlan")

        # 1) Variables
        # P[t, i] = production
        # Inv[t, i] = inventory
        # We'll iterate over self._periods, self._products
        model.P = Var(((t, i) for t in self._periods for i in self._products),
                      domain=NonNegativeReals)
        model.Inv = Var(((t, i) for t in self._periods for i in self._products),
                        domain=NonNegativeReals)

        # 2) Constraints
        # (a) Inventory balance
        def inv_balance_rule(model, t, i):
            if t == 0:
                # first period
                init_inv = self.init_inventory.get(i, 0.0)
                return model.Inv[t, i] == init_inv + model.P[t, i] - self.demand_forecast[t][i]
            else:
                t_prev = self._periods[t - 1]
                return model.Inv[t, i] == model.Inv[t_prev, i] + model.P[t, i] - self.demand_forecast[t][i]

        model.InvBalance = Constraint(list(model.P.keys()), rule=inv_balance_rule)

        # (b) Max production per period, if set
        if self.attrs.max_period_production is not None:
            def max_prod_rule(mdl, t):
                return sum(mdl.P[t, i] for i in self._products) <= self.attrs.max_period_production

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
            # sum_{i} [ inv_a + inv_b*( sum_{t}Inv[t,i] )^2 ]
            expr = 0.0
            for i in self._products:
                sum_inv_i = sum(mdl.Inv[t, i] for t in self._periods)
                expr += self.attrs.inv_a + self.attrs.inv_b * (sum_inv_i ** 2)
            return expr

        @model.Expression()
        def production_variance(mdl):
            """
            single factor for *all* products:
            sum_{i in products}( Var(P^i ) ) * smoothing_factor
            Var(P^i) = (1/|T|)* sum_{t} (P[t,i] - Pbar_i)^2
            Pbar_i = (1/|T|)* sum_{t} P[t,i]
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
