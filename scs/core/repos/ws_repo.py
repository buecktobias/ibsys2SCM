from sqlalchemy.orm import Session
from scs.db.models import (
    Workstation, DemandForecast, BoughtItem, ProducedItem, MaterialGraphORM,
    Process, ProcessInput, ProcessOutput, SimulationConfig, Order, NormalOrder,
    DirectOrder, MaterialOrder, ItemProduction, WSCapa, WSUseInfo, InventoryResultItem
)
from scs.domain import (
    WorkstationDomain, DemandForecastDomain, BoughtItemDomain, ProducedItemDomain,
    MaterialGraphDomain, ProcessDomain, ProcessInputDomain, ProcessOutputDomain,
    SimulationConfigDomain, OrderDomain, NormalOrderDomain, DirectOrderDomain,
    MaterialOrderDomain, ItemProductionDomain, WSCapaDomain, WSUseInfoDomain,
    InventoryResultItemDomain, ItemDomain
)


class WorkstationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> WorkstationDomain:
        ws = self.session.query(Workstation).filter(Workstation.id == id).one()
        return WorkstationDomain(
                id=ws.id,
                labour_cost_1=ws.labour_cost_1,
                labour_cost_2=ws.labour_cost_2,
                labour_cost_3=ws.labour_cost_3,
                labour_overtime_cost=ws.labour_overtime_cost,
                variable_machine_cost=ws.variable_machine_cost,
                fixed_machine_cost=ws.fixed_machine_cost
        )
