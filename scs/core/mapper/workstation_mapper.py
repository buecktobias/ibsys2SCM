from scs.core.db.models.workstation_orm import WorkstationORM
from scs.core.domain.ws_domain_model import WorkstationDomain
from scs.core.mapper.base_mapper import BaseMapper


class WorkstationMapper(BaseMapper[WorkstationORM, WorkstationDomain]):
    def convert_to_domain(self, orm_obj: WorkstationORM) -> WorkstationDomain:
        return WorkstationDomain(
                id=orm_obj.id,
                labour_cost_1=orm_obj.labour_cost_1,
                labour_cost_2=orm_obj.labour_cost_2,
                labour_cost_3=orm_obj.labour_cost_3,
                fixed_machine_cost=orm_obj.fixed_machine_cost,
                variable_machine_cost=orm_obj.variable_machine_cost,
                labour_overtime_cost=orm_obj.labour_overtime_cost,
        )

    def convert_to_orm(self, domain_obj):
        pass
