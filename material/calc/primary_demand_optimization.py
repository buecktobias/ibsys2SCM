from ortools.sat.python import cp_model


def round_production_plan_to10(production_plan):
    for product, plan in production_plan.items():
        for i, p in enumerate(plan):
            production_plan[product][i] = round(p, -1)
    return production_plan


class ProductionPlanner:
    def __init__(self, order_forecast, initial_inventory, num_virtual_periods=2):
        self.order_forecast = order_forecast
        self.initial_inventory = initial_inventory
        self.num_products = len(order_forecast)
        self.num_actual_periods = len(order_forecast[0])
        self.num_virtual_periods = num_virtual_periods
        self.total_periods = self.num_actual_periods + self.num_virtual_periods
        self.extended_orders = self._extend_orders()

    def _extend_orders(self):
        ext = []
        for i in range(self.num_products):
            avg = sum(self.order_forecast[i]) // self.num_actual_periods
            ext.append(self.order_forecast[i] + [avg] * self.num_virtual_periods)
        return ext

    def build_model(self):
        model = cp_model.CpModel()
        max_prod = 250
        min_prod = 50
        max_inv = 1000000
        P = {}
        I = {}
        for i in range(self.num_products):
            for p in range(self.total_periods):
                P[i, p] = model.NewIntVar(min_prod, max_prod, f'P_{i}_{p}')
                I[i, p] = model.NewIntVar(0, max_inv, f'I_{i}_{p}')
        for i in range(self.num_products):
            model.Add(I[i, 0] == self.initial_inventory[i] + P[i, 0] - self.extended_orders[i][0])
            for p in range(1, self.total_periods):
                model.Add(I[i, p] == I[i, p - 1] + P[i, p] - self.extended_orders[i][p])
        total_production = model.NewIntVar(0, 100000000, 'total_production')
        model.Add(total_production == sum(P[i, p] for i in range(self.num_products) for p in range(self.total_periods)))

        prod_costs = []
        for p in range(self.total_periods):
            Q_p = model.NewIntVar(0, max_prod * self.num_products, f'TotalProd_{p}')
            model.Add(Q_p == sum(P[i, p] for i in range(self.num_products)))
            bp1 = model.NewBoolVar(f'b_prod1_{p}')
            bp2 = model.NewBoolVar(f'b_prod2_{p}')
            bp3 = model.NewBoolVar(f'b_prod3_{p}')
            model.Add(Q_p <= 299).OnlyEnforceIf(bp1)
            model.Add(Q_p >= 300).OnlyEnforceIf(bp1.Not())
            model.Add(Q_p >= 300).OnlyEnforceIf(bp2)
            model.Add(Q_p <= 399).OnlyEnforceIf(bp2)
            model.Add(Q_p >= 400).OnlyEnforceIf(bp3)
            model.Add(bp1 + bp2 + bp3 == 1)
            cost_prod_p = model.NewIntVar(0, max_prod * self.num_products * 200, f'prod_cost_{p}')
            model.Add(cost_prod_p == 20_000 + 150 * Q_p).OnlyEnforceIf(bp1)
            model.Add(cost_prod_p == 20_000 + 160 * Q_p).OnlyEnforceIf(bp2)
            model.Add(cost_prod_p == 20_000 + 180 * Q_p).OnlyEnforceIf(bp3)
            prod_costs.append(cost_prod_p)
        prod_cost_total = model.NewIntVar(0, 1000000, 'prod_cost_total')
        model.Add(prod_cost_total == sum(prod_costs))

        # Total production over all periods (for revenue calculation)
        total_production = model.NewIntVar(0, 10000, 'total_production')
        model.Add(total_production == sum(P[i, p] for i in range(self.num_products)
                                          for p in range(self.total_periods)))

        inv_costs = []
        for p in range(self.total_periods):
            T_p = model.NewIntVar(0, max_inv * self.num_products, f'TotalInv_{p}')
            model.Add(T_p == sum(I[i, p] for i in range(self.num_products)))
            b1 = model.NewBoolVar(f'b_inv1_{p}')
            b2 = model.NewBoolVar(f'b_inv2_{p}')
            b3 = model.NewBoolVar(f'b_inv3_{p}')
            model.Add(T_p <= 199).OnlyEnforceIf(b1)
            model.Add(T_p >= 200).OnlyEnforceIf(b1.Not())
            model.Add(T_p >= 200).OnlyEnforceIf(b2)
            model.Add(T_p <= 299).OnlyEnforceIf(b2)
            model.Add(T_p >= 300).OnlyEnforceIf(b3)
            model.Add(b1 + b2 + b3 == 1)
            cost_p = model.NewIntVar(0, 200000000, f'inv_cost_{p}')
            model.Add(cost_p == 2 * T_p).OnlyEnforceIf(b1)
            model.Add(cost_p == 4 * T_p).OnlyEnforceIf(b2)
            model.Add(cost_p == 30 * T_p).OnlyEnforceIf(b3)
            inv_costs.append(cost_p)
        inv_cost_total = model.NewIntVar(0, 1000000000, 'inv_cost_total')
        model.Add(inv_cost_total == sum(inv_costs))

        revenue = model.NewIntVar(0, 200000000000, 'revenue')
        model.Add(revenue == 200 * total_production)
        profit = model.NewIntVar(-10000000000, 10000000000, 'profit')
        model.Add(profit == revenue - prod_cost_total - inv_cost_total)
        model.Maximize(profit)
        return model, P, I, total_production, inv_cost_total, prod_cost_total, revenue, profit

    def plan_production(self):
        model, P, I, total_production, inv_cost_total, prod_cost, revenue, profit = self.build_model()
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            production_plan = {i: [solver.Value(P[i, p]) for p in range(self.total_periods)]
                               for i in range(self.num_products)}
            inventory_plan = {i: [solver.Value(I[i, p]) for p in range(self.total_periods)]
                              for i in range(self.num_products)}
            return {
                'production_plan': production_plan,
                'inventory_plan': inventory_plan,
                'total_production': solver.Value(total_production),
                'inv_cost_total': solver.Value(inv_cost_total),
                'prod_cost': solver.Value(prod_cost),
                'revenue': solver.Value(revenue),
                'profit': solver.Value(profit)
            }
        return None


if __name__ == '__main__':
    order_forecast = [
        [150, 150, 150, 150],
        [100, 100, 50, 50],
        [150, 100, 50, 100]
    ]
    initial_inventory = [100, 100, 100]
    planner = ProductionPlanner(order_forecast, initial_inventory, num_virtual_periods=2)
    result = planner.plan_production()
    if result:
        for product, plan in round_production_plan_to10(result['production_plan']).items():
            print(f"Product {product}: {plan}")
        for product, plan in result['inventory_plan'].items():
            print(f"Inv {product}: {plan}")
        print("Total Production:", result['total_production'])
        print("Inventory Cost Total:", result['inv_cost_total'])
        print("Production Cost:", result['prod_cost'])
        print("Revenue:", result['revenue'])
        print("Profit:", result['profit'])
    else:
        print("No solution found.")
