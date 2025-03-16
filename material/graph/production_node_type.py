from enum import Enum


class ProductionNodeType(Enum):
    BOUGHT = "K"
    PRODUCED = "E"
    FINAL_PRODUCT = "P"
    PROCESS = "PR"
