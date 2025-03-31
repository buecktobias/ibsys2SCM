from __future__ import annotations

from collections import Counter

from scs.core.domain.item_models import GraphNodeDomain, ItemDomain, ProducedItemDomain
from scs.core.domain.ws_domain_model import WorkstationDomain


class ProcessDomain(GraphNodeDomain):
    process_duration: int
    setup_duration: int
    inputs: Counter[ItemDomain]
    workstation: WorkstationDomain
    output: ProducedItemDomain
