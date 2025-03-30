class ItemProductionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> ItemProductionDomain:
        ip = self.session.query(ItemProduction).filter(ItemProduction.id == id).one()
        return ItemProductionDomain(
                id=ip.id,
                producing_item_id=ip.producing_item_id,
                quantity=ip.quantity,
                producing_item=ItemDomain(id=ip.producing_item.id)
        )
