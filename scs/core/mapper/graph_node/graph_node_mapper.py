from scs.core.db.models.graph.graph_node_orm import GraphNodeORM
from scs.core.db.models.process_models import ProcessORM
from scs.core.domain.item_models import GraphNodeDomain
from scs.core.domain.process_domain_model import ProcessDomain
from scs.core.mapper.base_mapper import BaseMapper
from scs.core.mapper.graph_node.process_mapper import ProcessMapper
from scs.core.repos.ws_repo import WorkstationRepository


class GraphNodeMapper(BaseMapper[GraphNodeORM, GraphNodeDomain]):
    def __init__(self, process_mapper: ProcessMapper, item_mapper: Item):
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

    def convert_to_orm(self, domain: GraphNodeDomain) -> GraphNodeORM:
        # ...placeholder mapping...
        return GraphNodeORM(id=domain.id)
