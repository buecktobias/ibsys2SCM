from collections import Counter

from pyomo import environ as pyo
# noinspection PyUnresolvedReferences
from pyomo.core import ConcreteModel, Var, Constraint, NonNegativeReals

from material.calc.primary_demand.production_planning_attributes import ProductionPlanningAttributes
from material.core.resource_counter import ItemCounter
from material.db.models.periodic_item_quantity import PeriodicItemQuantity


class ProductionPlanningModelBuilder:
    def __init__(
            self,
            attrs: ProductionPlanningAttributes,
            demand_forecast: PeriodicItemQuantity,
            init_inventory: ItemCounter
    ):
        if 0 in demand_forecast.keys():
            raise ValueError("Forecast for period 0 not allowed (reserved for init inventory).")
        if 1 not in demand_forecast.keys():
            raise ValueError("Forecast must include period 1.")
        if len(init_inventory) != len(demand_forecast[1]):
            raise ValueError("Initial inventory and period-1 forecast must have same products.")

        self._attrs = attrs
        self._demand_forecast = demand_forecast
        self._init_inventory = init_inventory

    @property
    def _periods(self):
        return sorted(self._demand_forecast.keys())

    @property
    def _products(self):
        products_set = set()
        for period in self._periods:
            products_set.update(self._demand_forecast[period].keys())
        return sorted(products_set)

    @property
    def highest_period(self):
        return max(self._periods)

    @property
    def _extended_periods(self):
        return [0] + self._periods

    def _add_demand_period(self, periods_demand: ItemCounter):
        self._demand_forecast[self.highest_period + 1] = periods_demand

    def _add_dummy_periods(self, model: ConcreteModel):
        average_item_demands: ItemCounter = Counter({
            item: int(round(sum(self._demand_forecast[t][item] for t in self._periods) / len(self._periods)))
            for item in self._products
        })

    def build_pyomo_model(self) -> ConcreteModel:
        model = ConcreteModel("ProductionPlan")
        self._create_variables(model)
        self._set_initial_inventory(model)
        self._create_constraints(model)
        self._create_expressions(model)
        self._create_objective(model)
        return model

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
            return mdl.Inv[0, item] == self._init_inventory[item]

        model.InitInv = Constraint(self._products, rule=init_inv_rule)

    def _create_constraints(self, model: ConcreteModel) -> None:
        def inv_balance_rule(mdl, period, item):
            previous_inventory = mdl.Inv[period - 1, item]
            current_production = mdl.P[period, item]
            current_demand = self._demand_forecast[period][item]
            return (
                    mdl.Inv[period, item] == previous_inventory + current_production - current_demand
            )

        model.InvBalance = Constraint(list(model.P.keys()), rule=inv_balance_rule)

        def max_prod_rule(mdl, period):
            return sum(mdl.P[period, p] for p in self._products) <= self._attrs.max_period_production

        model.MaxProd = Constraint(self._periods, rule=max_prod_rule)

    def _create_expressions(self, model: ConcreteModel) -> None:
        @model.Expression()
        def total_production(mdl):
            return sum(mdl.P[t, i] for t in self._periods for i in self._products)

        @model.Expression()
        def production_cost(mdl):
            return self._attrs.production_cost_func(mdl.total_production)

        @model.Expression()
        def inventory_cost(mdl):
            expr = 0.0
            for t in self._periods:
                total_inv_t = sum(mdl.Inv[t, i] for i in self._products)
                expr += self._attrs.inventory_cost_func(total_inv_t)
            return expr

        @model.Expression()
        def production_variance(mdl):
            t_len = float(len(self._periods))
            total_var = 0.0
            for i in self._products:
                avg_p = sum(mdl.P[t, i] for t in self._periods) / t_len
                sum_sq = sum((mdl.P[t, i] - avg_p) ** 2 for t in self._periods)
                total_var += (1.0 / t_len) * sum_sq
            return self._attrs.smoothing_factor * total_var

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
