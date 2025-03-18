import pytest
from collections import Counter

from material.core.resource_counter import ResourceCounter
from material.graph.nodes.graph_nodes import Item, Bought


@pytest.fixture
def items():
    a = Bought(1)
    b = Bought(2)
    c = Bought(3)
    return a, b, c


def test_add_resource_counter(items):
    a, b, _ = items
    rc1 = ResourceCounter(Counter({a: 2, b: 3}))
    rc2 = ResourceCounter(Counter({a: 1, b: 4}))
    rc_sum = rc1 + rc2
    assert rc_sum.counter[a] == 3
    assert rc_sum.counter[b] == 7


def test_sub_resource_counter(items):
    a, b, _ = items
    rc1 = ResourceCounter(Counter({a: 5, b: 3}))
    rc2 = ResourceCounter(Counter({a: 2, b: 1}))
    rc_sub = rc1 - rc2
    assert rc_sub.counter[a] == 3
    assert rc_sub.counter[b] == 2
    # Test removal of keys with zero or negative count
    rc3 = ResourceCounter(Counter({a: 1, b: 3}))
    rc_sub2 = rc1 - rc3
    assert a in rc_sub2.counter
    assert b not in rc_sub2.counter


def test_mul_resource_counter(items):
    a, b, _ = items
    rc = ResourceCounter(Counter({a: 2, b: 3}))
    rc_mul = rc * 3
    assert rc_mul.counter[a] == 6
    assert rc_mul.counter[b] == 9
    # Test right multiplication
    rc_mul2 = 2 * rc
    assert rc_mul2.counter[a] == 4
    assert rc_mul2.counter[b] == 6


def test_copy_and_update(items):
    a, b, _ = items
    rc1 = ResourceCounter(Counter({a: 2}))
    rc_copy = rc1.copy()
    # Copy should have the same counter but be a different instance.
    assert rc_copy.counter == rc1.counter
    assert rc_copy is not rc1

    rc2 = ResourceCounter(Counter({b: 3}))
    rc_updated = rc1.update(rc2)
    assert rc_updated.counter[a] == 2
    assert rc_updated.counter[b] == 3
