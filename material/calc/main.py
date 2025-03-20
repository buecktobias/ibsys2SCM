from supply_chain_optimization.core.calculate_required_resources import ResourceCalculator
from supply_chain_optimization.core.resource_counter import ResourceCounter
from supply_chain_optimization.setup.production_graph_setup import create_full_production_graph


def calc_basic_demand():
    graph = create_full_production_graph()

    resource_calculator = ResourceCalculator(graph)

    current_inventory = ResourceCounter.from_id_map(
        graph,
        {
            1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100, 10: 100,
            11: 100, 12: 100, 13: 100, 14: 100, 15: 100, 16: 300, 17: 300, 18: 100, 19: 100, 20: 100,
            21: 300, 22: 300, 23: 300, 24: 6100, 25: 3600, 26: 300, 27: 1800, 28: 4500, 29: 100,
            30: 100, 31: 100, 32: 2700, 33: 900, 34: 22000, 35: 3600, 36: 900, 37: 900, 38: 300,
            39: 900, 40: 900, 41: 900, 42: 1800, 43: 1900, 44: 2700, 45: 900, 46: 900, 47: 900,
            48: 1800, 49: 100, 50: 100, 51: 100, 52: 600, 53: 22000, 54: 100, 55: 100, 56: 100,
            57: 600, 58: 22000, 59: 1800
        }

    )

    required = resource_calculator.calculate_required_resources_from_inventory(
        graph,
        ResourceCounter.from_id_map(graph, {
            "E1": 150,
            "E2": 150,
            "E3": 150
        }),
        current_inventory
    )

    required.print_sorted_resources()


if __name__ == '__main__':
    calc_basic_demand()
