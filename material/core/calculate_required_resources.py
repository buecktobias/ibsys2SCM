from collections import Counter

from material.core.resource_counter import ResourceCounter
from material.graph.nodes.graph_nodes import Node
from material.graph.production_graph.material_product_graph import MaterialProductGraph


class ResourceCalculator:
    def __init__(self, productions_graph: MaterialProductGraph):
        self.productions_graph = productions_graph

    def traverse_node(
            self,
            graph: MaterialProductGraph,
            required_resources: ResourceCounter,
            inventory: ResourceCounter,
            node: Node,
            multiplier: int = 1,
    ) -> None:
        """
        Recursively traverses the predecessors of 'node' in the graph.
        For each predecessor, computes the total required amount, subtracts any available
        inventory, and updates the required_resources counter.
        """
        g = graph.nx_graph
        for pred_key in g.predecessors(node.label):
            pred_node = graph.get_node_by_uid(pred_key)
            edge_weight = g[pred_key][node.label].get("weight", 1)
            total_weight = edge_weight * multiplier
            available = inventory[pred_node]
            needed = total_weight - available
            required_resources[pred_node] += needed
            self.traverse_node(graph, required_resources, inventory, pred_node, needed)

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
            self.traverse_node(graph, required_resources, inventory, node, quantity)
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
