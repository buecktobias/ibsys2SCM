from enum import Enum
from typing import List

from pydantic import BaseModel


class GameDTO(BaseModel):
    id: int


class XMLFile(BaseModel):
    content: str  # or use UploadFile later for real uploads


class PeriodResultDTO(BaseModel):
    game_id: int
    period: int
    xml_file: XMLFile


class PrimaryPlanDTO(BaseModel):
    game_id: int
    period: int
    planned_items: List[str]


class ProductionDTO(BaseModel):
    game_id: int
    period: int
    article_id: str
    quantity: int
    priority: int


class OrderMode(str, Enum):
    normal = "normal"
    fast = "fast"


class OrderDTO(BaseModel):
    game_id: int
    period: int
    article_id: str
    quantity: int
    mode: OrderMode


class WorkstationCapacityDTO(BaseModel):
    game_id: int
    period: int
    workstation_id: int
    shifts: int
    overtime: int


class SimulationInputDTO(BaseModel):
    game_id: int
    period: int
    xml_file: XMLFile
