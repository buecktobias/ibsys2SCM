from material.setup.production_graph_setup import create_full_production_graph
from material.visualization.mermaid_visualizations import NxToMermaid

if __name__ == '__main__':
    NxToMermaid(create_full_production_graph()).nx_to_mermaid("full_production_graph")
