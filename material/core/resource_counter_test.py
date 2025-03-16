import pytest
from collections import Counter

from material.core.resource_counter import ResourceCounter
from material.graph.graph_nodes import Item


@pytest.fixture
def items():
    a = Item.from_node_id("K1")
    b = Item.from_node_id("K2")
    c = Item.from_node_id("K3")
    return a, b, c


def test_add_resource_counter(items):
    a, b, _ = items
    rc1 = ResourceCounter(Counter({a: 2, b: 3}))
    rc2 = ResourceCounter(Counter({a: 1, b: 4}))
    rc_sum = rc1 + rc2
    assert rc_sum.items[a] == 3
    assert rc_sum.items[b] == 7


def test_sub_resource_counter(items):
    a, b, _ = items
    rc1 = ResourceCounter(Counter({a: 5, b: 3}))
    rc2 = ResourceCounter(Counter({a: 2, b: 1}))
    rc_sub = rc1 - rc2
    assert rc_sub.items[a] == 3
    assert rc_sub.items[b] == 2
    # Test removal of keys with zero or negative count
    rc3 = ResourceCounter(Counter({a: 1, b: 3}))
    rc_sub2 = rc1 - rc3
    assert a in rc_sub2.items
    assert b not in rc_sub2.items


def test_mul_resource_counter(items):
    a, b, _ = items
    rc = ResourceCounter(Counter({a: 2, b: 3}))
    rc_mul = rc * 3
    assert rc_mul.items[a] == 6
    assert rc_mul.items[b] == 9
    # Test right multiplication
    rc_mul2 = 2 * rc
    assert rc_mul2.items[a] == 4
    assert rc_mul2.items[b] == 6


def test_getitem_and_iteration(items):
    a, b, c = items
    rc = ResourceCounter(Counter({a: 5, b: 3}))
    assert rc[a] == 5
    # Missing keys should return 0.
    assert rc[c] == 0
    # Iteration should yield all keys present.
    keys = list(iter(rc))
    assert set(keys) == {a, b}


def test_copy_and_update(items):
    a, b, _ = items
    rc1 = ResourceCounter(Counter({a: 2}))
    rc_copy = rc1.copy()
    # Copy should have the same items but be a different instance.
    assert rc_copy.items == rc1.items
    assert rc_copy is not rc1

    rc2 = ResourceCounter(Counter({b: 3}))
    rc_updated = rc1.update(rc2)
    assert rc_updated.items[a] == 2
    assert rc_updated.items[b] == 3
