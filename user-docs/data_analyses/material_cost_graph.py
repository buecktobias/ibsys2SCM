import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle
from graphviz import Digraph
import networkx as nx
import webbrowser
import os


def create_graph():
    G = nx.DiGraph()

    # Add nodes (Processes, Bought Items, Produced Items)
    G.add_node("K39", type="bought")
    G.add_node("K32", type="bought")

    G.add_node("13.A", type="process", workstation_id="13", process_duration=2, setup_duration=0)
    G.add_node("12.A", type="process", workstation_id="12", process_duration=3, setup_duration=0)
    G.add_node("8.A", type="process", workstation_id="8", process_duration=1, setup_duration=15)
    G.add_node("7.A", type="process", workstation_id="7", process_duration=2, setup_duration=20)
    G.add_node("9.A", type="process", workstation_id="9", process_duration=3, setup_duration=15)

    G.add_node("E13", type="produced")

    # Add edges with weights
    G.add_edge("K39", "13.A", weight=1)
    G.add_edge("13.A", "12.A", weight=1)
    G.add_edge("12.A", "8.A", weight=1)
    G.add_edge("8.A", "7.A", weight=1)
    G.add_edge("K32", "7.A", weight=1)
    G.add_edge("7.A", "9.A", weight=1)
    G.add_edge("9.A", "E13", weight=1)

    # Add nodes (Processes, Bought Items, Produced Items)
    G.add_node("K28", type="bought")
    G.add_node("K59", type="bought")

    G.add_node("6.A", type="process", workstation_id="6", process_duration=3, setup_duration=15)
    G.add_node("8.B", type="process", workstation_id="8", process_duration=3, setup_duration=20)
    G.add_node("7.B", type="process", workstation_id="7", process_duration=2, setup_duration=20)
    G.add_node("9.B", type="process", workstation_id="9", process_duration=2, setup_duration=15)

    G.add_node("E18", type="produced")

    # Add edges with weights
    G.add_edge("K28", "6.A", weight=3)
    G.add_edge("6.A", "8.B", weight=1)
    G.add_edge("K59", "8.B", weight=3)
    G.add_edge("8.B", "7.B", weight=1)
    G.add_edge("K32", "7.B", weight=2)  # K32 already exists from previous code
    G.add_edge("7.B", "9.B", weight=1)
    G.add_edge("9.B", "E18", weight=1)

    # Add nodes (Processes, Bought Items, Produced Items)
    G.add_node("K52", type="bought")
    G.add_node("K53", type="bought")
    G.add_node("K35", type="bought")
    G.add_node("K37", type="bought")
    G.add_node("K38", type="bought")

    G.add_node("10.A", type="process", workstation_id="10", process_duration=4, setup_duration=20)
    G.add_node("11.A", type="process", workstation_id="11", process_duration=3, setup_duration=20)

    G.add_node("E7", type="produced")

    # Add edges with weights
    G.add_edge("K52", "10.A", weight=1)
    G.add_edge("K53", "10.A", weight=36)
    G.add_edge("10.A", "11.A", weight=1)
    G.add_edge("K35", "11.A", weight=1)
    G.add_edge("K37", "11.A", weight=2)
    G.add_edge("K38", "11.A", weight=1)
    G.add_edge("11.A", "E7", weight=1)

    return G

def nx_to_mermaid(G):
    lines = ["flowchart LR"]
    for node, attr in G.nodes(data=True):
        t = attr.get("type")
        if t == "bought":
            lines.append(f'    {node}(("{node}"))')
        elif t == "produced":
            lines.append(f'    {node}(("{node}"))')
        elif t == "process":
            ws = attr.get("workstation_id", "")
            proc = attr.get("process_duration", "")
            setup = attr.get("setup_duration", "")
            label = f"{ws}<br>{node}<br>{proc}/{setup}"
            lines.append(f'    {node}["{label}"]')
    for u, v, attr in G.edges(data=True):
        w = attr.get("weight", "")
        lines.append(f'    {u} -->|{w}| {v}')
    return "\n".join(lines)

def render_mermaid(diagram_code):
    html_template = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Mermaid Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{ startOnLoad: true }});</script>
  </head>
  <body>
    <div class="mermaid">
{diagram_code}
    </div>
  </body>
</html>
"""
    with open("diagram.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    webbrowser.open("file://" + os.path.abspath("diagram.html"))


if __name__ == '__main__':
    G = create_graph()
    mmd = nx_to_mermaid(G)
    render_mermaid(mmd)
