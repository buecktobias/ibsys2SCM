class ProcessRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> ProcessDomain:
        proc = self.session.query(Process).filter(Process.id == id).one()
        mg_repo = MaterialGraphRepository(self.session)
        ws_repo = WorkstationRepository(self.session)
        inputs = [ProcessInputDomain(
                process_id=inp.process_id,
                quantity=inp.quantity,
                process=None
        ) for inp in proc.inputs]
        out = None
        if proc.output:
            out = ProcessOutputDomain(
                    process_id=proc.output.process_id,
                    item_id=proc.output.item_id,
                    item=ItemDomain(id=proc.output.item.id),
                    process=None
            )
        return ProcessDomain(
                id=proc.id,
                graph_id=proc.graph_id,
                workstation_id=proc.workstation_id,
                process_duration=proc.process_duration_minutes,
                setup_duration=proc.setup_duration_minutes,
                graph=mg_repo.get_by_id(proc.graph_id),
                inputs=inputs,
                workstation=ws_repo.get_by_id(proc.workstation_id),
                output=out
        )
