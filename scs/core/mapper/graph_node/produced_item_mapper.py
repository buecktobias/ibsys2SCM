from scs.core.db.item_models import ProducedItemORM
from scs.core.domain.item_models import ProducedItem
from scs.core.mapper.base_mapper import BaseMapper


class ProducedItemMapper(BaseMapper[ProducedItemORM, ProducedItem]):

    def convert_to_domain(self, orm_model: ProducedItemORM) -> ProducedItem:
        return ProducedItem(
                id=orm_model.id,
        )

    def convert_to_orm(self, domain_model: ProducedItem) -> ProducedItemORM:
        raise NotImplementedError("Conversion from domain to ORM is not implemented.")
