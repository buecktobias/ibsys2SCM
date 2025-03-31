from scs.core.db.models.graph_models import GraphNodeORM
from scs.core.db.models.process_models import ProcessORM
from scs.core.domain.process_domain_model import ProcessDomain
from scs.core.repos.ws_repo import WorkstationRepository


class GraphNodeMapper:
    def __init__(self, workstation_repository: WorkstationRepository):
        self.workstation_repository = workstation_repository

    def convert_to_domain(self, node: GraphNodeORM):
        """
        Convert a graph node to its domain representation.
        :param node: The graph node to convert.
        :return: The domain representation of the graph node.
        """
        if not isinstance(node, GraphNodeORM):
            raise TypeError(f"Expected GraphNodeORM, got {type(node)}")

        if isinstance(node, ProcessORM):
            return ProcessDomain(
                    id=node.id,
                    workstation=self.workstation_repository.get_by_id()
            )
