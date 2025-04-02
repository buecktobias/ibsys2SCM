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
