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
    objective: float

    def print_primary_demand_table(self) -> None:
        """
        Print a GitHub-style markdown table showing:
          - Each product as a row
          - Each period as a column
          - Cell: "d=xx; p=xx; i=xx" with integer rounding
        """
        # Prepare table headers
        headers = ["Product"] + [f"Period {p}" for p in self.production.keys()]
        table = []

        for prod in self.production[list(self.production.keys())[0]].keys():
            row = [str(prod)]
            for p in self.production.keys():
                d_val = self.demand[p].get(prod, 0.0)
                p_val = self.production[p].get(prod, 0.0)
                i_val = self.inventory[p].get(prod, 0.0)

                # Round to integers
                d_int = int(round(d_val))
                p_int = int(round(p_val))
                i_int = int(round(i_val))

                cell = f"d={d_int}; p={p_int}; i={i_int}"
                row.append(cell)
            table.append(row)

        # Print using tabulate in GitHub style
        print(tabulate(table, headers=headers, tablefmt="github"))

    def __str__(self):
        """
        String summary of the numeric solution data.
        """
        return (
            f"ProductionSolutionData(\n"
            f"  production_cost={self.production_cost:.2f},\n"
            f"  inventory_cost={self.inventory_cost:.2f},\n"
            f"  variance_penalty={self.variance_penalty:.2f},\n"
            f"  revenue={self.revenue:.2f},\n"
            f"  objective={self.objective:.2f}\n"
            f")"
        )
