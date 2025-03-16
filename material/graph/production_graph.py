import logging
from typing import Self

import networkx as nx

from material.graph.graph_nodes import Item, Process, StepItem
from material.graph.production_node_type import ProductionNodeType


class GraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.material_map: dict[str, Item] = {}

    def create_group(self, group_name: str):
        return BuilderSubgraph(self, group_name)

    def add_item(self, item_id: str):
        new_node = Item.from_node_id(item_id)
        self.material_map[item_id] = new_node
        if new_node.node_uid in self.graph.nodes:
            logging.warning(f"Node {new_node.node_uid} already exists in graph! This is not a problem,"
                            f" just check if it is intended. Skipping...")
            return
        self.graph.add_node(new_node.node_uid, data=new_node)

    def add_processing_item(self, final_group_material_result: int, step_number: int):
        new_node = StepItem(
            node_id=final_group_material_result,
            step_number=step_number,
            _node_type=ProductionNodeType.PROCESS
        )

        if new_node in self.graph.nodes:
            logging.warning(f"Node {new_node.node_uid} already exists in graph! This is not a problem,"
                            f" just check if it is intended. Skipping...")
            return
        self.graph.add_node(new_node.node_uid, data=new_node)

    def build(self):
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Graph must be directed acyclic!")
        return MaterialProductFlowGraph(self.graph)


class BuilderSubgraph:
    def __init__(self, graph_builder: GraphBuilder, group_name: str):
        self.graph_builder = graph_builder
        self.group_name = group_name

    def convert_input_dict(self, inputs: dict[str, int]) -> dict[Item, int]:
        return {self.graph_builder.material_map[k]: v for k, v in inputs.items()}

    def add_process(self,
                    workstation_id: int,
                    process_duration: int,
                    setup_duration: int,
                    inputs: dict[str, int] = None,
                    output: str = None
                    ):
        converted_inputs = self.convert_input_dict(inputs) if inputs is not None else None
        output_item = self.graph_builder.material_map[output] if output is not None else None

        new_process = Process(
            workstation_id=workstation_id,
            process_duration=process_duration,
            setup_duration=setup_duration,
            inputs=converted_inputs,
            output=output_item
        )

        if new_process.node_uid in self.graph_builder.graph.nodes:
            logging.warning(f"Node {new_process.node_uid} already exists in graph! This is not a problem,"
                            f" just check if it is intended. Skipping...")
            return

        self.graph_builder.graph.add_node(new_process.node_uid, data=new_process)
        for material, weight in converted_inputs.items():
            self.graph_builder.graph.add_node(material.node_uid, data=material)
            self.graph_builder.graph.add_edge(material.node_uid, new_process.node_uid, weight=weight)
        self.graph_builder.graph.add_node(output_item.node_uid, data=output_item)
        self.graph_builder.graph.add_edge(new_process.node_uid, output_item.node_uid, weight=1)


class MaterialProductFlowGraph:
    def __init__(self, graph=None):
        if graph is None:
            graph = nx.DiGraph()
        self.graph: nx.DiGraph = graph

    def get_graphs_nodes(self):
        nodes = []
        for _, data in self.graph.nodes(data=True):
            nodes.append(data)
        return nodes

    def __add__(self, material_production_graph: Self):
        combined_graph = nx.compose_all([self.graph, material_production_graph.graph])
        return MaterialProductFlowGraph(combined_graph)


if __name__ == '__main__':
    combined_graph = combine_graphs(production_graph1, production_graph2, production_graph3)
