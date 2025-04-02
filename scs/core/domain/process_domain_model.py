from __future__ import annotations

from collections import Counter

from scs.core.domain.item_models import GraphNode, Item, ProducedItem
from scs.core.domain.ws_domain_model import Workstation


class Process(GraphNode):
    process_duration: int
    setup_duration: int
    inputs: Counter[Item]
    workstation: Workstation
    output: ProducedItem
