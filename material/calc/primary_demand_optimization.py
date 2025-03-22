from ortools.sat.python import cp_model


class ProductionPlanner:
    def __init__(self, order_forecast: list[list[int]], initial_inventory: list[int], num_virtual_periods=2):
        self.order_forecast: list[list[int]] = order_forecast
        self.initial_inventory: list[int] = initial_inventory
        self.num_virtual_periods = num_virtual_periods

        self._extend_orders()

    def _extend_orders(self):
        average_orders = [sum(order) / len(order) for order in self.order_forecast]

        for i in range(len(self.order_forecast)):
            self.order_forecast[i].extend([int(average_orders[i])] * self.num_virtual_periods)

    @property
    def num_products(self):
        return len(self.initial_inventory)

    @property
    def total_periods(self):
        return len(self.order_forecast[0])

    def plan_production(self):
        model = cp_model.CpModel()
        max_prod = 10_000
        max_inv = 10_000
        P = {}
        I = {}
        for i in range(len(self.initial_inventory)):
            for p in range(len(self.order_forecast[0])):
                P[i, p] = model.NewIntVar(0, max_prod, f'P_{i}_{p}')
                I[i, p] = model.NewIntVar(0, max_inv, f'I_{i}_{p}')
        for i in range(self.num_products):
            model.Add(I[i, 0] == self.initial_inventory[i] + P[i, 0] - self.order_forecast[i][0])
            for p in range(1, self.total_periods):
                model.Add(I[i, p] == I[i, p - 1] + P[i, p] - self.order_forecast[i][p])

        total_production = model.NewIntVar(0, 100_000, 'total_production')
        model.Add(total_production == sum(P[i, p] for i in range(self.num_products) for p in range(self.total_periods)))

        # Inventory cost piecewise function:
        # If total_inventory < 200 then cost = total_inventory * 2,
        # if 200 <= total_inventory < 400 then cost = total_inventory * 10,
        # if total_inventory >= 400 then cost = total_inventory * 20.
        revenue = model.NewIntVar(0, 200_0000, 'revenue')
        model.Add(revenue == 200)

        profit = model.NewIntVar(-1_000_000, 1_000_000, 'profit')
        model.Maximize(profit)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            production_plan = {}
            for i in range(self.num_products):
                production_plan[i] = [solver.Value(P[i, p]) for p in range(self.total_periods)]
            return production_plan
        return None


if __name__ == '__main__':
    order_forecast = [
        [150, 150, 150, 150],
        [100, 100, 50, 50],
        [150, 50, 50, 50]
    ]
    initial_inventory = [100, 100, 100]
    planner = ProductionPlanner(order_forecast, initial_inventory, num_virtual_periods=2)
    plan = planner.plan_production()
    if plan:
        for i, prod in plan.items():
            print(f"Product {i}: {prod}")
    else:
        print("No solution found.")
