from dataclasses import dataclass

from tabulate import tabulate

from material.db.models.periodic_item_quantity import PeriodicItemQuantity


@dataclass
class ProductionSolutionData:
    """
    Dataclass capturing the final solution of the production planning optimization.
    """
    demand: PeriodicItemQuantity
    production: PeriodicItemQuantity
    inventory: PeriodicItemQuantity
    production_cost: float
    inventory_cost: float
    variance_penalty: float
    revenue: float
    earnings: float

    def format_primary_demand_table(self) -> str:
        """
        Print a GitHub-style markdown table showing:
          - Each product as a row
          - Each period as a column
          - Cell: "d=xx; p=xx; i=xx" with integer rounding
        """
        # Prepare table headers
        headers = ["Product"] + [f"Period {p}" for p in self.inventory.keys()]
        table = []

        for prod in self.production[list(self.production.keys())[0]].keys():
            row = [str(prod)]
            for p in self.inventory.keys():
                d_val = self.demand.get(p, {}).get(prod, None)
                p_val = self.production.get(p, {}).get(prod, None)
                i_val = self.inventory.get(p).get(prod)

                # Round to integers
                if d_val is not None:
                    d_int = int(round(d_val))
                    p_int = int(round(p_val))
                    i_int = int(round(i_val))
                    cell = f"d={d_int}; p={p_int}; i={i_int}"
                else:
                    cell = f"i={int(round(i_val))}"
                row.append(cell)
            table.append(row)

        return tabulate(table, headers=headers, tablefmt="github")

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

    def __str__(self):
        """
        String summary of the numeric solution data.
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
