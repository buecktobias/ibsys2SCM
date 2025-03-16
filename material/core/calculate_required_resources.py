from collections import Counter

from graph.production_graph import MaterialProductFlowGraph
from resource_counter import ResourceCounter


class ResourceCalculator:
    def __init__(self, productions_graph: MaterialProductFlowGraph):
        self.productions_graph = productions_graph

    def calculate_required_resources_from_inventory(
            self, graph: MaterialProductFlowGraph, required_resources: ResourceCounter, inventory: ResourceCounter
    ) -> ResourceCounter:
        g = graph.material_graph

        def traverse(node: str, multiplier: int = 1) -> None:
            for pred in g.predecessors(node):
                edge_weight = g[pred][node].get("weight", 1)
                total_weight = edge_weight * multiplier
                available = inventory.items.get(pred, 0)
                needed = total_weight - available
                if needed <= 0:
                    continue
                required_resources[pred] += needed
                traverse(pred, needed)

        traverse(product_id, 1)
        return ResourceCounter(required_resources)

    def calculate_required_resources(self, product_id: str) -> ResourceCounter:
        # Call the inventory-based method with an empty inventory.
        empty_inventory = ResourceCounter(Counter())
        return self.calculate_required_resources_from_inventory(
            self.productions_graph, product_id, empty_inventory
        )
