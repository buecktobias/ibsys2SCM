from __future__ import annotations

from collections import Counter
from typing import Optional

from pydantic import BaseModel

from scs.core.domain.orders.iorder import InvChange, IOrder
from scs.core.domain.periodic_item_quantities import PeriodicItemQuantity


class WorkstationDomain(BaseModel):
    id: int
    labour_cost_1: float
    labour_cost_2: float
    labour_cost_3: float
    labour_overtime_cost: float
    variable_machine_cost: float
    fixed_machine_cost: float


class DemandForecastDomain(BaseModel):
    periodic_item_quantity: PeriodicItemQuantity


class GraphNodeDomain(BaseModel):
    id: int


class ItemDomain(GraphNodeDomain):
    id: int


class BoughtItemDomain(ItemDomain):
    base_price: float
    discount_amount: int
    mean_order_duration: float
    order_std_dev: float
    base_order_cost: float


class ProducedItemDomain(ItemDomain):
    pass


class ProcessDomain(GraphNodeDomain):
    workstation_id: int
    process_duration: int
    setup_duration: int
    inputs: Counter[ItemDomain]
    workstation: WorkstationDomain
    output: ProducedItemDomain


class NormalOrderDomain(IOrder):
    pass


class DirectOrderDomain(IOrder):
    penalty: float


class MaterialOrderDomain(IOrder):
    order_type: str


class ItemProductionDomain(InvChange):
    producing_item: ProducedItemDomain
    quantity: int
    period: int


class WSCapaDomain(BaseModel):
    workstation: WorkstationDomain
    period: int
    shifts: int
    overtime: int


class WSUseInfoDomain(BaseModel):
    workstation: WorkstationDomain
    period: int
    setup_events: int
    idletime_minutes: int
    time_needed_minutes: int


class Inventory(BaseModel):
    periodic_item_quantity: PeriodicItemQuantity
