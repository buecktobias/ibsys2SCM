from collections import Counter
from production_graph import MaterialProductionFlowGraph, Type

from graph_setup_p1 import create_graph_p1
from graph_setup_p2 import create_graph_p2
from graph_setup_p3 import create_graph_p3

def calculate_required_resources(graph: MaterialProductionFlowGraph, product_id: str):
    required_resources = Counter()
    required_resources[product_id] = 1
    def traverse(node, multiplier=1):
        for pred in graph.graph.predecessors(node):
            edge_weight = graph.graph[pred][node].get('weight', 1)
            total_weight = edge_weight * multiplier
            node_type = graph.graph.nodes[pred].get('type')
            if node_type in [Type.BOUGHT, Type.PRODUCED]:
                required_resources[pred] += total_weight
            traverse(pred, total_weight)

    traverse(product_id)
    return required_resources




if __name__ == '__main__':
    graph_p1 = create_graph_p1()
    graph_p2 = create_graph_p2()
    graph_p3 = create_graph_p3()

    resources_p1 = calculate_required_resources(graph_p1, 'E1')
    resources_p2 = calculate_required_resources(graph_p2, 'E2')
    resources_p3 = calculate_required_resources(graph_p3, 'E3')


    def get_number_from_uid(uid: str):
        if "." in uid:
            return int(uid.split(".")[0])
        else:
            return int(uid[1:])

    def print_sorted_resources(resources_dict: dict[str, int]):
        for key in sorted(resources_dict.keys(), key=get_number_from_uid):
            print(f"{key}: {resources_dict[key]}")


    keys = resources_p1.keys() | resources_p2.keys() | resources_p3.keys()
    merged_resources = { key: 0 for key in keys }
    for key in keys:
        merged_resources[key] += resources_p1.get(key, 0) + resources_p2.get(key, 0) + resources_p3.get(key, 0)

    print_sorted_resources(merged_resources)
