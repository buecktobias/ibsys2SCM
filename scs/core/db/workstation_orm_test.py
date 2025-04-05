from sqlalchemy.orm import Session

from scs.core.db.workstation_orm import WorkstationORM


def test_workstation(db_session: Session):
    ws = WorkstationORM(
            id=101,
            labour_cost_1=10, labour_cost_2=11, labour_cost_3=12,
            labour_overtime_cost=15, variable_machine_cost=20, fixed_machine_cost=30
    )
    db_session.add(ws)
    db_session.commit()
    assert db_session.get(WorkstationORM, ws.id)
