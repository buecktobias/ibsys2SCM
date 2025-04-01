from scs.core.db.models.item_models import ProducedItemORM
from scs.core.domain.item_models import ProducedItemDomain
from scs.core.mapper.base_mapper import BaseMapper


class ProducedItemMapper(BaseMapper[ProducedItemORM, ProducedItemDomain]):

    def convert_to_domain(self, orm_model: ProducedItemORM) -> ProducedItemDomain:
        return ProducedItemDomain(
                id=orm_model.id,
        )

    def convert_to_orm(self, domain_model: ProducedItemDomain) -> ProducedItemORM:
        raise NotImplementedError("Conversion from domain to ORM is not implemented.")
