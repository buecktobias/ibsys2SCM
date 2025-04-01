from scs.core.db.models.process_models import ProcessORM
from scs.core.domain.process_domain_model import ProcessDomain
from scs.core.mapper.base_mapper import BaseMapper
from scs.core.mapper.workstation_mapper import WorkstationMapper


class ProcessMapper(BaseMapper[ProcessORM, ProcessDomain]):
    def __init__(self, workstation_mapper: WorkstationMapper):
        self.workstation_mapper = workstation_mapper

    def convert_to_orm(self, domain_model: ProcessDomain) -> ProcessORM:
        raise NotImplementedError("Conversion from domain to ORM is not implemented.")

    def convert_to_domain(self, orm_model: ProcessORM) -> ProcessDomain:
        workstation_domain = self.workstation_mapper.convert_to_domain(orm_model.workstation)
        return ProcessDomain(
                id=orm_model.id,
                workstation=workstation_domain,
                setup_duration=orm_model.setup_duration_minutes,
                process_duration=orm_model.process_duration_minutes,
                inputs=orm_model.inputs,
                output=orm_model.outputs,
        )
