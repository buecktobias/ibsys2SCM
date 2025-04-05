from collections import Counter

from pyomo import environ as pyo
# noinspection PyUnresolvedReferences
from pyomo.core import ConcreteModel, Constraint, NonNegativeReals, Var

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
