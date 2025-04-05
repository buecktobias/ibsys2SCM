import random
from collections import Counter

from scs.core.domain.item_models import Item, ProducedItem
from scs.core.domain.process_domain_model import Process
from scs.core.domain.ws_domain_model import Workstation
from scs.tests.item_factory import ItemFactory
from scs.tests.workstation_factory import WorkstationFactory


class ProcessFactory:
    def __init__(self, workstation_factory: WorkstationFactory, item_factory: ItemFactory):
        self.workstation_factory = workstation_factory
        self.item_factory = item_factory

    def create(
            self,
            id: int | None = None,
            process_duration: int | None = None,
            setup_duration: int | None = None,
            inputs: Counter[Item] = None,
            workstation: Workstation = None,
            output: ProducedItem = None
    ):
        if inputs is None:
            inputs = Counter()

        if workstation is None:
            workstation = self.workstation_factory.create_workstation()

        if output is None:
            output = self.item_factory.create_produced_item()
        return Process(
                id=id or random.randint(1, 10 ** 8),
                process_duration=process_duration or random.randint(1, 10 ** 4),
                setup_duration=setup_duration or random.randint(1, 10 ** 4),
                inputs=inputs,
                workstation=workstation,
                output=output,
        )
