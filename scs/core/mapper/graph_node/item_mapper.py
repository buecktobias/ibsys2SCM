from scs.core.db.item_models.bought_item_orm import BoughtItemORM
from scs.core.db.item_models.item_orm import ItemORM
from scs.core.domain.item_models import Item
from scs.core.mapper.base_mapper import BaseMapper
from scs.core.mapper.graph_node.bought_item_mapper import BoughtItemMapper


class ItemNodeMapper(BaseMapper[ItemORM, Item]):
    def __init__(self, bought_item_mapper: BoughtItemMapper, produced_item_mapper: BoughtItemORM):
        self.bought_item_mapper = bought_item_mapper
        self.produced_item_mapper = produced_item_mapper

    def convert_to_domain(self, orm_obj):
        if isinstance(orm_obj, BoughtItemORM):
            return
        pass

    def convert_to_orm(self, domain_obj):
        # ...placeholder mapping...
        pass
