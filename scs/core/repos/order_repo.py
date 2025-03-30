class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> OrderDomain:
        order = self.session.query(Order).filter(Order.id == id).one()
        base = OrderDomain(
                id=order.id,
                order_kind=order.order_kind,
                created_at=order.created_at_period,
                item_id=order.item_id,
                quantity=order.quantity,
                cash_flow_per_item=order.cash_flow_per_item,
                was_executed=order.was_executed,
                item=ItemDomain(id=order.item.id) if order.item else None
        )
        if order.order_kind == "normal_order":
            return NormalOrderDomain(**base.dict())
        if order.order_kind == "direct_order":
            return DirectOrderDomain(**base.dict(), penalty=order.penalty)
        if order.order_kind == "material_order":
            return MaterialOrderDomain(**base.dict(), order_type=order.order_type)
        return base
