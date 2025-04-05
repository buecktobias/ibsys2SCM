import random

from scs.core.domain.ws_domain_model import Workstation


class WorkstationFactory:
    def create_workstation(
            self,
            id: int | None = None,
            labour_cost_1: float | None = None,
            labour_cost_2: float | None = None,
            labour_cost_3: float | None = None,
            labour_overtime_cost: float | None = None,
            variable_machine_cost: float | None = None,
            fixed_machine_cost: float | None = None,
    ):
        return Workstation(
                id=id or random.randint(1, 10 ** 8),
                labour_cost_1=labour_cost_1 or random.uniform(0, 100),
                labour_cost_2=labour_cost_2 or random.uniform(0, 100),
                labour_cost_3=labour_cost_3 or random.uniform(0, 100),
                labour_overtime_cost=labour_overtime_cost or random.uniform(0, 100),
                variable_machine_cost=variable_machine_cost or random.uniform(0, 100),
                fixed_machine_cost=fixed_machine_cost or random.uniform(0, 100),
        )
