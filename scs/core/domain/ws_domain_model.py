from __future__ import annotations

from pydantic import BaseModel


class Workstation(BaseModel):
    """
    Represents a workstation in the production system.
    Attributes:
        id: int
        labour_cost_1: float
        labour_cost_2: float
        labour_cost_3: float
        labour_overtime_cost: float
        variable_machine_cost: float
        fixed_machine_cost: float
    """
    id: int
    labour_cost_1: float
    labour_cost_2: float
    labour_cost_3: float
    labour_overtime_cost: float
    variable_machine_cost: float
    fixed_machine_cost: float
