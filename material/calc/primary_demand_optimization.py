import abc

from pyomo.environ import ConcreteModel, Var, Constraint, Objective, SolverFactory, NonNegativeReals, exp, value

from material.core.resource_counter import ItemCounter
from material.db.models.periodic_item_quantity import PeriodicItemQuantity


class PrimaryDemandOptimization(abc.ABC):
    @abc.abstractmethod
    def get_production_plan(self) -> PeriodicItemQuantity:
        pass


class PrimaryDemandOptimizationModel(PrimaryDemandOptimization):
    def __init__(self,
                 current_primary_inventory: ItemCounter,
                 demand_forecast: PeriodicItemQuantity,
                 ):
        self.demand_forecast: PeriodicItemQuantity = demand_forecast
        self.current_primary_inventory: ItemCounter = current_primary_inventory
        self.inventories = {}
        self.optimization_model = ConcreteModel("MultiProductProduction")

    def build_model(self):
        """
        Create a Pyomo model that:
        - Has variables: P[t,i], I[t,i]
        - Constrains inventory: I[t,i] = I[t-1,i] + P[t,i] - D[t,i]
        - Has a cost-based objective that includes:
            * Production cost
            * Inventory cost (quadratic)
            * Production variance penalty
        - Maximizes profit = Revenue - costs, or Minimizes negative profit
        """

        # -- Sets in the model (we'll store as lists for iteration) --

        # -- Variables --
        # P[t,i] production
        m.P = Var(((t, i) for t in m.T for i in m.I), domain=NonNegativeReals)
        # I[t,i] inventory
        m.Inv = Var(((t, i) for t in m.T for i in m.I), domain=NonNegativeReals)

        # -- Constraints --

        # (1) Inventory balance
        def inv_balance_rule(mdl, t, i):
            idx_t = m.T.index(t)
            if idx_t == 0:
                # first period
                init_inv = self.init_inventory.get(i, 0.0)
                return mdl.Inv[t, i] == init_inv + mdl.P[t, i] - self.demand[t][i]
            else:
                # previous period
                tprev = m.T[idx_t - 1]
                return mdl.Inv[t, i] == mdl.Inv[tprev, i] + mdl.P[t, i] - self.demand[t][i]

        m.InvBalance = Constraint(m.P.keys(), rule=inv_balance_rule)

        # (2) Max production per period (if set)
        if self.max_period_production is not None:
            def max_production_rule(mdl, t):
                return sum(mdl.P[t, i] for i in m.I) <= self.max_period_production

            m.MaxProd = Constraint(m.T, rule=max_production_rule)

        # -- We define some expressions for sums needed in objective --

        # Sum of total production across all products and periods
        def total_production_expr(mdl):
            return sum(mdl.P[t, i] for t in m.T for i in m.I)

        m.TotalProduction = pyo.Expression(rule=total_production_expr)

        # Inventory cost expression
        # We'll do a single aggregated approach: sum over products of [a + b * ( totalInv_i )^2]
        # But we must define "totalInv_i" = sum of I[t,i] over all periods t or just final inventory?
        # Let's do sum of all end-of-period inventories for that product as a proxy
        #   totalInv_i = sum_{t} Inv[t,i]
        # Then cost = a + b*( totalInv_i^2 ) per product
        def inv_cost_expr(mdl):
            cost = 0
            for i in m.I:
                totinv_i = sum(mdl.Inv[t, i] for t in m.T)
                cost += self.inventory_a + self.inventory_b * (totinv_i ** 2)
            return cost

        m.InventoryCost = pyo.Expression(rule=inv_cost_expr)

        # Production cost expression
        # as specified: ProdCost = fixed_cost + var_cost * ( total production )
        def prod_cost_expr(mdl):
            return self.prod_fixed_cost + self.prod_var_cost * mdl.TotalProduction

        m.ProductionCost = pyo.Expression(rule=prod_cost_expr)

        # Production variance penalty
        # For each product i: Var(P^i) = (1/T)* sum_{t}( P[t,i] - Pbar_i )^2
        # We'll define an expression for Pbar_i = (1/T)* sum_{t} P[t,i]
        # Then define a sum-of-squares, multiply by factor_i
        # We'll store partial expressions for clarity
        def avg_production_expr(mdl, i):
            return (1.0 / len(m.T)) * sum(mdl.P[t, i] for t in m.T)

        # We'll create dict-of-Expressions for Pbar_i
        m.Pbar = pyo.Expression(m.I, rule=lambda mdl, i: avg_production_expr(mdl, i))

        def variance_expr(mdl):
            # sum_{i in I} [ factor_i * Var(P^i ) ]
            # Var(P^i) = (1/T)* sum_{t}( P[t,i] - Pbar_i )^2
            var_sum = 0
            for i in m.I:
                factor_i = self.variance_factor.get(i, 0.0)
                # compute var(P^i)
                # We'll multiply the sum-of-squares by (1/ T) inside
                sum_sq = 0
                for t in m.T:
                    sum_sq += (mdl.P[t, i] - mdl.Pbar[i]) ** 2
                # var_i = (1/ T)* sum_sq
                var_i = sum_sq / len(m.T)
                var_sum += factor_i * var_i
            return var_sum

        m.ProductionVariance = pyo.Expression(rule=variance_expr)

        # Let's define revenue for completeness, if you want:
        #   e.g. revenue = 200 * total produced
        # but the user might want multi-product different revenues => up to you
        # We'll do a simple approach:  self.revenue_unit[i]? or single number?
        # Let's skip or do a placeholder revenue?

        m.Revenue = pyo.Expression(expr=0.0)  # or define your own if needed

        # -- Objective: Maximize profit = revenue - (ProductionCost + InventoryCost + ProductionVariance) --
        def obj_rule(mdl):
            return mdl.Revenue - (mdl.ProductionCost + mdl.InventoryCost + mdl.ProductionVariance)

        m.Obj = pyo.Objective(rule=obj_rule, sense=maximize)

        return m

    def solve(self):
        """
        Build and solve the model with Pyomo Ipopt or another suitable solver
        """
        m = self.build_model()
        solver = pyo.SolverFactory('ipopt')  # because we have squares => nonlinear
        result = solver.solve(m, tee=False)
        # Extract solution
        production_plan = {}
        inventory_plan = {}

        for (t, i) in m.P.keys():
            production_plan[(t, i)] = value(m.P[t, i])
        for (t, i) in m.Inv.keys():
            inventory_plan[(t, i)] = value(m.Inv[t, i])

        # Evaluate cost components:
        total_prod_cost = value(m.ProductionCost)
        total_inv_cost = value(m.InventoryCost)
        total_var_cost = value(m.ProductionVariance)
        total_obj = value(m.Obj)

        return {
            'production': production_plan,
            'inventory': inventory_plan,
            'production_cost': total_prod_cost,
            'inventory_cost': total_inv_cost,
            'variance_penalty': total_var_cost,
            'objective': total_obj
        }


class MultiProductProductionOptimizer:
    """
    A multi-period, multi-product production planning model using Pyomo.
    """

    def __init__(self, periods, products, demand, init_inventory):
        """
        :param periods: list of period indices (e.g. [1,2,3,4])
        :param products: list of product IDs (e.g. ['P1','P2'])
        :param demand: dict of dict, e.g. demand[period][product] = quantity
        :param init_inventory: dict of product-> initial inventory
        """
        self.periods = periods
        self.products = products
        self.demand = demand
        self.init_inventory = init_inventory

        self.inventory_a = 0.0
        self.inventory_b = 0.01
        self.prod_fixed_cost = 0.0
        self.prod_var_cost = 0.0
        self.max_period_production = None
        self.variance_factor = {}

    def set_inventory_cost_func(self, a, b):
        """
        Inventory cost = sum_{prod} [ a + b * ( total inventory for prod )^2 ]
        across all periods or at the end.
        (You can adapt details in build_model.)
        """
        self.inventory_a = a
        self.inventory_b = b

    def set_production_cost(self, fixed_cost, var_cost):
        """
        Production cost = fixed_cost + var_cost * ( total production )
        ( Possibly across all periods. )
        """
        self.prod_fixed_cost = fixed_cost
        self.prod_var_cost = var_cost

    def set_max_period_production(self, max_pp):
        """
        A limit on the total production across all products for each period.
        e.g. sum_{prod} P_{t,prod} <= max_pp
        """
        self.max_period_production = max_pp

    def set_product_wise_production_variance_penalty_factor(self, factor_dict):
        """
        factor_dict: e.g. {'P1':0.5, 'P2':0.3}
        We'll penalize variance for each product i as factor_i * Var(P^i).
        """
        self.variance_factor = factor_dict

    def build(self):
        return PrimaryDemandOptimizationModel(self.current_primary_inventory, self.demand_forecast)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///mydb.sqlite')
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        planner = ProductionPlannerPyomo(session, num_virtual_periods=0)
        result = planner.solve()
        print(result)
