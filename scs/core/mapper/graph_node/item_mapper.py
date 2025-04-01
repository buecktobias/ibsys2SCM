from scs.core.db.models.item_models import BoughtItemORM, ItemORM
from scs.core.domain.item_models import ItemDomain
from scs.core.mapper.base_mapper import BaseMapper
from scs.core.mapper.graph_node.bought_item_mapper import BoughtItemMapper


class ItemNodeMapper(BaseMapper[ItemORM, ItemDomain]):
    def __init__(self, bought_item_mapper: BoughtItemMapper, produced_item_mapper:):
        self.bought_item_mapper = bought_item_mapper
        self.produced_item_mapper = produced_item_mapper

    def convert_to_domain(self, orm_obj):
        if isinstance(orm_obj, BoughtItemORM):
            return
        pass

    def convert_to_orm(self, domain_obj):
        # ...placeholder mapping...
        pass
