from supply_chain_optimization.setup.production_graph_setup import create_full_production_graph
from supply_chain_optimization.visualization.mermaid_visualizations import NxToMermaid

if __name__ == '__main__':
    NxToMermaid(create_full_production_graph()).nx_to_mermaid("full_production_graph")
