from material.db.config import engine
from material.graph.production_graph.database_graph_loader import DatabaseGraphLoader
from material.graph.production_graph.production_graph import ProductionGraph
from material.graph.visualization.mermaid_visualizations import NxToMermaid

if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        loader = DatabaseGraphLoader(session)
        prod_graph = ProductionGraph(loader)

        # Prune singleton produced item nodes in the NX graph.
        prod_graph.prune_singleton_produced_items()

        # Build the visualization material graph (which will include only processes that remain in the pruned NX graph).
        viz_material_graph = prod_graph.build_visualization_material_graph()

        # Now pass both prod_graph._nx and viz_material_graph to your Mermaid exporter.
        mermaid_code = NxToMermaid(viz_material_graph).nx_to_mermaid("Graph New")
        print(mermaid_code)
