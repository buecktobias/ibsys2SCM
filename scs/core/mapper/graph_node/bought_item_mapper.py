from scs.core.db.models.item_models import BoughtItemORM
from scs.core.domain.item_models import BoughtItemDomain
from scs.core.mapper.base_mapper import BaseMapper


class BoughtItemMapper(BaseMapper[BoughtItemORM, BoughtItemDomain]):
    def convert_to_domain(self, orm_obj: BoughtItemORM) -> BoughtItemDomain:
        return BoughtItemDomain(
                id=orm_obj.id,
                base_price=orm_obj.base_price,
                discount_amount=orm_obj.discount_amount,
                mean_order_duration=orm_obj.mean_order_duration,
                order_std_dev=orm_obj.order_std_dev,
                base_order_cost=orm_obj.base_order_cost,
        )

    def convert_to_orm(self, domain_obj):
        raise NotImplementedError("Conversion from domain to ORM is not implemented.")
