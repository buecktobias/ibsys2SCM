from collections import Counter

from scs.core.db.models.item_models import Item
from scs.graph.core.production_graph import ProductionGraph


class ResourceCalculator:
    def __init__(self, productions_graph: ProductionGraph):
        self.productions_graph = productions_graph

    def _traverse_node(
            self,
            graph: ProductionGraph,
            required_resources: Counter[Item],
            inventory: Counter[Item],
            node_id: str,
            multiplier: int = 1,
    ) -> None:
        """
        Recursively traverses the predecessors of 'node' in the graph.
        For each predecessor, computes the total required amount, subtracts any available
        inventory, and updates the required_resources counter.
        """
        g = graph._nx
        for pred_key in g.predecessors(node_id):
            edge_weight = g[pred_key][node_id].get("weight", 1)
            total_weight = edge_weight * multiplier
            available = inventory[g.nodes[pred_key]["data"]]
            needed = total_weight - available
            required_resources[pred_node] += needed
            self._traverse_node(graph, required_resources, inventory, pred_node, needed)

    def calculate_required_resources_from_inventory(
            self,
            graph: MaterialProductGraph,
            required_resources: ResourceCounter,
            inventory: ResourceCounter,
    ) -> ResourceCounter:
        """
        Traverses the graph, updating required_resources based on available inventory.
        """
        # Iterate over a copy of the current required_resources entries.
        for node, quantity in list(required_resources):
            self._traverse_node(graph, required_resources, inventory, node, quantity)
        return required_resources

    def calculate_required_resources(self, product_id: str) -> ResourceCounter:
        """
        Calculates the total required resources for the product identified by product_id,
        assuming an empty inventory.
        """
        product_node = self.productions_graph.get_node_by_uid(product_id)
        empty_inventory = ResourceCounter(Counter({product_node: 0}))
        required = ResourceCounter(Counter({product_node: 1}))
        return self.calculate_required_resources_from_inventory(
                self.productions_graph, required, empty_inventory
        )
