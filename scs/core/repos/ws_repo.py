from sqlalchemy import select
from sqlalchemy.orm import Session

from scs.core.db.models.workstation_orm import WorkstationORM
from scs.core.domain.ws_domain_model import WorkstationDomain


class WorkstationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> WorkstationDomain:
        ws = self.session.execute(select(WorkstationORM).filter_by(id=id)).scalars().one()
        return WorkstationDomain(
                id=ws.id,
                labour_cost_1=ws.labour_cost_1,
                labour_cost_2=ws.labour_cost_2,
                labour_cost_3=ws.labour_cost_3,
                labour_overtime_cost=ws.labour_overtime_cost,
                variable_machine_cost=ws.variable_machine_cost,
                fixed_machine_cost=ws.fixed_machine_cost
        )
