class MaterialGraphRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> MaterialGraphDomain:
        mg = self.session.query(MaterialGraphORM).filter(MaterialGraphORM.id == id).one()
        parent = None
        if mg.parent_graph:
            parent = MaterialGraphDomain(
                    id=mg.parent_graph.id,
                    name=mg.parent_graph.name,
                    parent_graph_id=mg.parent_graph.parent_graph_id,
                    parent_graph=None,
                    subgraphs=[],
                    processes=[]
            )
        subs = [MaterialGraphDomain(
                id=sub.id,
                name=sub.name,
                parent_graph_id=sub.parent_graph_id,
                parent_graph=None,
                subgraphs=[],
                processes=[]
        ) for sub in mg.subgraphs]
        procs = []
        return MaterialGraphDomain(
                id=mg.id,
                name=mg.name,
                parent_graph_id=mg.parent_graph_id,
                parent_graph=parent,
                subgraphs=subs,
                processes=procs
        )
