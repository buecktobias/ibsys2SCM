from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from scs.core.db.models.base import Base
from scs.core.db.types import DomainSimTime, PeriodTime


class OrderORM(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_kind: Mapped[str] = mapped_column(String(50))
    created_at_period: Mapped[int] = mapped_column(Integer)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    cash_flow_per_item: Mapped[int] = mapped_column(Integer)
    was_executed: Mapped[bool] = mapped_column(Boolean)

    item = relationship("Item")

    __mapper_args__ = {
            "polymorphic_on": order_kind,
            "polymorphic_identity": "order"
    }


class NormalOrderORM(OrderORM):
    __tablename__ = "normal_order"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "normal_order"}


class DirectOrderORM(OrderORM):
    __tablename__ = "direct_order"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    penalty: Mapped[float] = mapped_column(Float)
    __mapper_args__ = {"polymorphic_identity": "direct_order"}


class MaterialOrderORM(OrderORM):
    __tablename__ = "material_order"
    id: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    order_type: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {"polymorphic_identity": "material_order"}


class ItemProductionORM(Base):
    __tablename__ = "item_production"
    id: Mapped[int] = mapped_column(primary_key=True)
    producing_item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    producing_item = relationship("Item")
