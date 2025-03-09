import time

import networkx as nx


def create_graph():
    G = nx.DiGraph()

    # Nodes – non-process (bought and produced) sorted by numeric value
    G.add_node("E4", type="produced")
    G.add_node("E7", type="produced")
    G.add_node("E10", type="produced")
    G.add_node("E13", type="produced")
    G.add_node("E18", type="produced")
    G.add_node("E26", type="produced")
    G.add_node("E49", type="produced")
    G.add_node("E50", type="produced")
    G.add_node("E51", type="produced")
    G.add_node("K21", type="bought")
    G.add_node("K25", type="bought")
    G.add_node("K26", type="bought")
    G.add_node("K27", type="bought")
    G.add_node("K28", type="bought")
    G.add_node("K32", type="bought")
    G.add_node("K35", type="bought")
    G.add_node("K36", type="bought")
    G.add_node("K37", type="bought")
    G.add_node("K38", type="bought")
    G.add_node("K39", type="bought")
    G.add_node("K47", type="bought")
    G.add_node("K52", type="bought")
    G.add_node("K53", type="bought")
    G.add_node("K59", type="bought")

    # Process nodes – sorted by letter (after the dot) then by the numeric part (before the dot)
    # Unique nodes (the later calls override earlier ones):
    #   letter A: 6.A, 7.A, 8.A, 9.A, 12.A, 13.A
    #   letter B: 7.B, 8.B, 9.B, 11.B, 12.B, 13.B
    #   letter M: 1.M
    #   letter Q: 2.Q
    #   letter R: 7.R
    #   letter S: 15.S
    #   letter X: 4.X
    #   letter Y: 3.Y
    G.add_node("6.D", type="process", workstation_id="6", process_duration=3, setup_duration=15)
    G.add_node("7.D", type="process", workstation_id="7", process_duration=2, setup_duration=20)
    G.add_node("8.D", type="process", workstation_id="8", process_duration=1, setup_duration=15)
    G.add_node("9.D", type="process", workstation_id="9", process_duration=3, setup_duration=15)
    G.add_node("12.G", type="process", workstation_id="12", process_duration=3, setup_duration=0)
    G.add_node("13.G", type="process", workstation_id="13", process_duration=2, setup_duration=0)
    G.add_node("7.C", type="process", workstation_id="7", process_duration=2, setup_duration=20)
    G.add_node("8.C", type="process", workstation_id="8", process_duration=1, setup_duration=15)
    G.add_node("9.C", type="process", workstation_id="9", process_duration=3, setup_duration=15)
    G.add_node("11.C", type="process", workstation_id="11", process_duration=3, setup_duration=10)
    G.add_node("12.C", type="process", workstation_id="12", process_duration=3, setup_duration=0)
    G.add_node("13.C", type="process", workstation_id="13", process_duration=2, setup_duration=0)
    G.add_node("1.w", type="process", workstation_id="1", process_duration=6, setup_duration=20)
    G.add_node("2.x", type="process", workstation_id="2", process_duration=5, setup_duration=30)
    G.add_node("7.H", type="process", workstation_id="7", process_duration=2, setup_duration=30)
    G.add_node("15.H", type="process", workstation_id="15", process_duration=3, setup_duration=15)
    G.add_node("4.z", type="process", workstation_id="4", process_duration=6, setup_duration=30)
    G.add_node("3.y", type="process", workstation_id="3", process_duration=5, setup_duration=20)

    # Edges sorted by the process letter key and then by flow order (edges in a chain appear before subsequent ones)
    # --- C
    G.add_edge("K39", "13.C", weight=1)
    G.add_edge("13.C", "12.C", weight=1)
    G.add_edge("12.C", "8.C", weight=1)
    G.add_edge("8.C", "7.C", weight=1)
    G.add_edge("K32", "7.C", weight=1)
    G.add_edge("7.C", "9.C", weight=1)
    G.add_edge("9.C", "E13", weight=1)

    # D
    G.add_edge("K28", "6.D", weight=3)
    G.add_edge("6.D", "8.D", weight=1)
    G.add_edge("K59", "8.D", weight=3)
    G.add_edge("8.D", "7.D", weight=1)
    G.add_edge("K32", "7.D", weight=2)
    G.add_edge("7.D", "9.D", weight=1)
    G.add_edge("9.D", "E18", weight=1)

    # E
    G.add_edge("K52", "10.E", weight=1)
    G.add_edge("K53", "10.E", weight=36)
    G.add_edge("10.E", "11.E", weight=1)
    G.add_edge("K35", "11.E", weight=1)
    G.add_edge("K37", "11.E", weight=2)
    G.add_edge("K38", "11.E", weight=1)
    G.add_edge("11.E", "E7", weight=1)





    # F ---
    G.add_edge("K52", "10.F", weight=1)
    G.add_edge("K53", "10.F", weight=36)
    G.add_edge("10.F", "11.F", weight=1)
    G.add_edge("K35", "11.F", weight=2)
    G.add_edge("K36", "11.F", weight=1)
    G.add_edge("11.F", "E4", weight=1)


    # G
    G.add_edge("K39", "13.G", weight=1)
    G.add_edge("13.G", "12.G", weight=1)
    G.add_edge("12.G", "8.G", weight=1)
    G.add_edge("8.G", "7.G", weight=1)
    G.add_edge("7.G", "9.G", weight=1)
    G.add_edge("9.G", "E10", weight=1)

    # H
    G.add_edge("7.H", "15.H", weight=1)
    G.add_edge("K21", "15.H", weight=1)
    G.add_edge("K24", "15.H", weight=1)
    G.add_edge("K27", "15.H", weight=1)
    G.add_edge("15.H", "E26", weight=1)

    # w
    G.add_edge("K24", "1.w", weight=2)
    G.add_edge("K24", "1.w", weight=2)
    G.add_edge("K25", "1.w", weight=2)
    G.add_edge("K26", "1.w", weight=2)
    G.add_edge("E13", "1.w", weight=1)
    G.add_edge("E18", "1.w", weight=1)
    G.add_edge("E7", "1.w", weight=1)
    G.add_edge("1.w", "E49", weight=1)

    # x
    G.add_edge("E49", "2.x", weight=1)
    G.add_edge("E4", "2.x", weight=1)
    G.add_edge("E10", "2.x", weight=1)
    G.add_edge("K24", "2.x", weight=2)
    G.add_edge("K25", "2.x", weight=2)
    G.add_edge("2.x", "E50", weight=1)

    # z ---
    G.add_edge("E17", "3.y", weight=1)
    G.add_edge("E16", "3.y", weight=1)
    G.add_edge("E50", "3.y", weight=1)
    G.add_edge("K24", "3.y", weight=1)
    G.add_edge("K27", "3.y", weight=1)
    G.add_edge("3.y", "E51", weight=1)

    return G



def nx_to_mermaid(G):
    lines = ["%%{init: {'theme': 'dark'}, 'themeVariables': {'darkMode': true}%%", "flowchart LR"]
    indent = "    "
    class_assignments = []

    subgraphs = {}
    for node, attr in G.nodes(data=True):
        t = attr.get("type")
        if t == "process":
            split_id = node.split(".")
            assert len(split_id) == 2
            process_class = split_id[1]
            if process_class not in subgraphs:
                subgraphs[process_class] = []

            subgraphs[process_class].append((node, attr))

    for node, attr in G.nodes(data=True):
        t = attr.get("type")
        class_assignments.append(indent + f'{node}:::{t}')
        if t in ["bought", "produced"]:
            lines.append(indent + f'{node}([{node}])')

    for name, nodes_attrs in subgraphs.items():
        lines.append(indent + f"subgraph {name}")
        for node, attr in nodes_attrs:
            ws = attr.get("workstation_id", "")
            proc = attr.get("process_duration", "")
            setup = attr.get("setup_duration", "")

            split_id = node.split(".")
            assert len(split_id) == 2
            ws_id = split_id[0]
            assert ws == ws_id

            process_class = split_id[1]

            label = (f"<div style='font-size:16px'><b>{node}</b></div>"
                     f"pt: {proc} - st: {setup}"
                     )
            lines.append(indent + f'{node}["{label}"]')
        lines.append(indent + "end")

    for u, v, attr in G.edges(data=True):
        w = attr.get("weight", "")
        lines.append(f'    {u} -->|{w}| {v}')
    # add style definitions (material design elegant colors)
    lines.append(indent +"%% Style definitions")
    lines.append(indent + "classDef bought fill:#455A64,stroke:#CFD8DC,stroke-width:2px,color:#CFD8DC;")
    lines.append(indent + "classDef produced fill:#263238,stroke:#ECEFF1,stroke-width:2px,color:#ECEFF1;")
    lines.append(indent + "classDef process fill:#1C313A,stroke:#B0BEC5,stroke-width:2px,color:#B0BEC5;")
    lines.extend(class_assignments)
    return "\n".join(lines)

def render_mermaid(diagram_code):
    html_template = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Mermaid Diagram</title>
    <style>
        body {{
            background-color: #121212;
            color: #ffffff;
        }}
        .mermaid-container {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .mermaid {{
            text-align: center;
            margin-top: 20px;
        }}
        svg {{
            width: 100%;
            height: 100%;
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script src="https://d3js.org/d3.v6.min.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function() {{
          mermaid.initialize({{ theme: 'dark', startOnLoad: true }});
          mermaid.init(undefined, document.querySelectorAll(".mermaid"));

          // Apply zoom and pan using d3.js
          setTimeout(() => {{
              const svg = document.querySelector("svg");
              if (!svg) return;
              const g = d3.select(svg).select("g");

              const zoom = d3.zoom()
                  .scaleExtent([0.5, 2])  // Zoom limits (min, max)
                  .on("zoom", (event) => {{
                      g.attr("transform", event.transform);
                  }});

              d3.select(svg).call(zoom);
          }}, 500);  // Delay to ensure Mermaid has rendered
      }});
    </script>
    <script>
      mermaid.initialize({{ theme: 'dark', startOnLoad: true }});
    </script>
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

def save_mmd(diagram_code):
    with open("diagram.mmd", "w", encoding="utf-8") as f:
        f.write(diagram_code)


def update():
    G = create_graph()
    mmd = nx_to_mermaid(G)
    save_mmd(mmd)
    render_mermaid(mmd)

def update_continuously():
    while True:
        update()
        time.sleep(10)


if __name__ == '__main__':
    update()

