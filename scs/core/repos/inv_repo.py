class InventoryResultItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_key(self, period: int, item_id: int) -> InventoryResultItemDomain:
        inv = self.session.query(InventoryResultItem).filter(
                InventoryResultItem.period == period,
                InventoryResultItem.item_id == item_id
        ).one()
        return InventoryResultItemDomain(
                period=inv.period,
                item_id=inv.item_id,
                quantity=inv.quantity
        )
