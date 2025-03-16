from collections import Counter
from production_graph import MaterialProductFlowGraph, NodeType, MaterialProductionsGraph
from resource_counter import ResourceCounter
from graph_setup_p1 import create_graph_p1
from graph_setup_p2 import create_graph_p2
from graph_setup_p3 import create_graph_p3

class ResourceCalculater:
    def __init__(self, productions_graph: MaterialProductionsGraph):
        self.productions_graph = productions_graph

    def calculate_required_resources(self, product_id: str):
        required_resources = Counter()
        required_resources[product_id] = 1
        def traverse(node, multiplier=1):
            for pred in graph.graph.predecessors(node):
                edge_weight = graph.graph[pred][node].get('weight', 1)
                total_weight = edge_weight * multiplier
                node_type = graph.graph.nodes[pred].get('type')
                if node_type in [NodeType.BOUGHT, NodeType.PRODUCED]:
                    required_resources[pred] += total_weight
                traverse(pred, total_weight)

        traverse(product_id)
        return required_resources


    def calculate_required_resources_from_inventory(self, graph: MaterialProductFlowGraph, product_id: str, inventory: ResourceCounter):
        required_resources = Counter()
        required_resources[product_id] = 1
        def traverse(node, multiplier=1):
            for pred in graph.graph.predecessors(node):
                edge_weight = graph.graph[pred][node].get('weight', 1)
                total_weight = edge_weight * multiplier

                needed = total_weight - inventory.items[pred]
                if needed <= 0:
                    continue

                required_resources[pred] += needed
                traverse(pred, needed)

        traverse(product_id, 1)
        return ResourceCounter(required_resources)




def test_having_inventory():
    graph_p1 = create_graph_p1()
    graph_p2 = create_graph_p2()
    graph_p3 = create_graph_p3()

    material_graph = MaterialProductionsGraph(graph_p1, graph_p2, graph_p3)
    res_calc = ResourceCalculater(material_graph)


    inventory = ResourceCounter(Counter({'E17': 1, 'K43': 1, 'K44': 1, 'K45': 1, 'K46': 1}))

    resources_p1 = res_calc.calculate_required_resources_from_inventory(graph_p1, 'E1', inventory)


    resources_p1.print_sorted_resources()


if __name__ == '__main__':
    test_having_inventory()

