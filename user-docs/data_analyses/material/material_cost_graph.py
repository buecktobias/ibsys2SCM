import re
import time
from dataclasses import dataclass
from enum import Enum

from graph_setup import create_graph
import networkx as nx
from process_util import Node, Process, get_graphs_nodes



def nx_to_mermaid(graph):
    lines = ["%%{init: {'theme': 'dark'}, 'themeVariables': {'darkMode': true}}%%", "flowchart LR"]
    indent = " " * 4
    class_assignments = []


    nodes = get_graphs_nodes(graph)

    unique_subgraphs = set([node.group for node in nodes])
    subgraphs = {
        group: [] for group in unique_subgraphs
    }


    for node in filter(lambda n: n is Process, nodes):
        subgraphs[node.group].append(node)

    for node in filter(lambda n: n is not Process, nodes):
        class_assignments.append(indent + f'{node.id}:::{node.type}')
        lines.append(indent + f'{node.id}([{node.id}])')


    sorted_subgraphs = sorted(subgraphs.items(), key=lambda x: x[0])

    for group, nodes in sorted_subgraphs:
        lines.append(indent + f"subgraph {group}")
        for node in nodes:

            label = (f"<div style='font-size:16px'><b>{node.id}</b></div>"
                     f"<small>{node.process_duration} - {node.setup_duration}</small>"
                     )
            lines.append(indent * 2 + f'{node.id}["{label}"]')
            class_assignments.append(indent + f'{node.id}:::{node.type}')
        lines.append(indent + "end")
        lines.append("")

    for u, v, attr in graph.edges(data=True):
        w = attr.get("weight", "")
        lines.append(indent + f'{u} -->|{w}| {v}')
    # add style definitions (material design elegant colors)
    lines.append(indent +"%% Style definitions")
    lines.append(indent + "classDef bought fill:#455A64,stroke:#CFD8DC,stroke-width:2px,color:#CFD8DC;")
    lines.append(indent + "classDef produced fill:#263238,stroke:#ECEFF1,stroke-width:2px,color:#ECEFF1;")
    lines.append(indent + "classDef process fill:#1C313A,stroke:#B0BEC5,stroke-width:2px,color:#B0BEC5;")
    lines.extend(class_assignments)
    return "\n".join(lines)


def save_html(mermaid_code):
    with open("template.html") as f:
        html = f.read()

    result = re.sub(r"{{ mermaidContent }}", mermaid_code, html)

    with open("diagram.html", "w", encoding="utf-8") as f:
        f.write(result)

def save_mmd(diagram_code):
    with open("diagram.mmd", "w", encoding="utf-8") as f:
        f.write(diagram_code)


def update():
    graph = create_graph()
    mmd = nx_to_mermaid(graph)
    save_mmd(mmd)
    save_html(mmd)

def update_continuously():
    while True:
        update()
        time.sleep(10)


if __name__ == '__main__':
    update()

