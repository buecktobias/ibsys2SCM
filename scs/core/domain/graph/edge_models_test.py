# test_edge_models.py
from collections import Counter

import pytest

from scs.core.domain.item_models import Item, ProducedItem
from scs.core.domain.process_domain_model import Process
from scs.core.domain.ws_domain_model import Workstation
from .edge_models import ProcessInputEdge, ProcessOutputEdge, WeightedEdge


def test_process_input_edge_initialization():
    edge = ProcessInputEdge(
            from_node=Item(id=11),
            to_node=Process(
                    id=11,
                    inputs=Counter({}),
                    workstation=Workstation(
                            id=11,
                            labour_overtime_cost=10,
                            labour_cost_3=2,
                            labour_cost_1=10,
                            fixed_machine_cost=20,
                            variable_machine_cost=22,
                            labour_cost_2=33
                    ),
                    output=ProducedItem(id=11),
                    process_duration=10,
                    setup_duration=10
            ),
            weight=10
    )
    assert edge.from_node is not None
    assert edge.to_node is not None
    assert edge.weight == 10


def test_process_output_edge_initialization_with_valid_weight(item_factory, process_factory):
    edge = ProcessOutputEdge(
            from_node=process_factory.create(id=202),
            to_node=item_factory.create_produced_item(id=101),
    )
    assert edge.from_node is not None
    assert edge.to_node is not None
    assert edge.weight == 1


def test_process_output_edge_invalid_weight_raises_error(item_factory, process_factory):
    with pytest.raises(ValueError):
        ProcessOutputEdge(
                from_node=process_factory.create(id=202),
                to_node=item_factory.create_produced_item(id=101),
                weight=2
        )


def test_process_input_edge_with_minimum_valid_values():
    item = Item(id=1)
    process = Process(
            id=1,
            inputs=Counter({}),
            workstation=Workstation(
                    id=1,
                    labour_overtime_cost=0,
                    labour_cost_3=0,
                    labour_cost_1=0,
                    fixed_machine_cost=0,
                    variable_machine_cost=0,
                    labour_cost_2=0
            ),
            output=ProducedItem(id=1),
            process_duration=0,
            setup_duration=0
    )
    edge = ProcessInputEdge(from_node=item, to_node=process, weight=0)

    assert isinstance(edge, ProcessInputEdge)
    assert isinstance(edge, WeightedEdge)
    assert edge.from_node == item
    assert edge.to_node == process
    assert edge.weight == 0
