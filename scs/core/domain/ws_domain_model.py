from __future__ import annotations

from pydantic import BaseModel


class WorkstationDomain(BaseModel):
    id: int
    labour_cost_1: float
    labour_cost_2: float
    labour_cost_3: float
    labour_overtime_cost: float
    variable_machine_cost: float
    fixed_machine_cost: float
