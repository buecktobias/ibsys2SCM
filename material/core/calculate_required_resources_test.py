from collections import Counter

from material.core.calculate_required_resources import ResourceCalculator
from material.core.resource_counter import ResourceCounter
from material.setup.graph_setup_p1 import create_graph_p1
from material.setup.production_graph_setup import create_full_production_graph


# Test when there is no inventory: required resources should propagate through the graph.
def test_calculate_required_resources_no_inventory():
    graph_p1 = create_graph_p1()
    resource_calculator = ResourceCalculator(graph_p1)
    result = resource_calculator.calculate_required_resources("E1")
    result.print_sorted_resources()


# Test with some inventory: available quantity reduces the required amount.
def test_calculate_required_resources_with_inventory():
    # Create a simple graph:
    #   K1 --(weight=2)--> E1
    graph_p1 = create_full_production_graph()
    inventory = ResourceCounter(Counter(
        {
            graph_p1.get_node_by_uid("E10"): 4,
            graph_p1.get_node_by_uid("K24"): 12,
            graph_p1.get_node_by_uid("E51"): 1,
        }))
    resource_calculator = ResourceCalculator(graph_p1)
    result = resource_calculator.calculate_required_resources_from_inventory(
        graph_p1,
        ResourceCounter(
            Counter({
                graph_p1.get_node_by_uid("E1"): 1,
                graph_p1.get_node_by_uid("E2"): 1,
                graph_p1.get_node_by_uid("E3"): 1
            })),
        inventory
    )

    result.print_sorted_resources()
