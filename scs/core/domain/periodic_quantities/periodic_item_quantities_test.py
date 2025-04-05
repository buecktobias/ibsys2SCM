from collections import Counter

import pytest

from scs.core.domain.item_models import Item
from scs.core.domain.periodic_quantities.periodic_item_quantities import PeriodicItemQuantity


@pytest.fixture
def sample_periodic_item_quantity():
    item1 = Item(id=1)
    item2 = Item(id=2)
    data = {
            1: {item1: 10, item2: 20},
            2: {item1: 15, item2: 25},
            3: {item1: 5, item2: 15}
    }
    return PeriodicItemQuantity(data)


def test_empty_periods_no_items():
    empty_data = {}
    with pytest.raises(ValueError):
        PeriodicItemQuantity(empty_data)

    single_empty_period = {1: {}}
    with pytest.raises(ValueError):
        PeriodicItemQuantity(single_empty_period)

    multiple_empty_periods = {1: {}, 2: {}, 3: {}}
    with pytest.raises(ValueError):
        PeriodicItemQuantity(multiple_empty_periods)

    item = Item(id=1)
    valid_data = {1: {item: 0}}
    piq = PeriodicItemQuantity(valid_data)
    assert piq.get_unique_items() == {item}
    assert piq.get_periods() == [1]
    assert piq.sum() == 0


def test_add_period(sample_periodic_item_quantity):
    # Arrange
    item1 = Item(id=1)
    item2 = Item(id=2)
    new_period_data = {item1: 30, item2: 35}
    expected_highest_period = sample_periodic_item_quantity.highest_period + 1

    # Act
    sample_periodic_item_quantity.add_period(new_period_data)

    # Assert
    assert sample_periodic_item_quantity.has_period(expected_highest_period)
    assert sample_periodic_item_quantity.get_value_for_item(expected_highest_period, item1) == 30
    assert sample_periodic_item_quantity.get_value_for_item(expected_highest_period, item2) == 35
    assert sample_periodic_item_quantity.highest_period == expected_highest_period


def test_get_average_value(sample_periodic_item_quantity):
    item1 = Item(id=1)
    expected_average = (10 + 15 + 5) / 3  # Average of item1 across all periods

    actual_average = sample_periodic_item_quantity.get_average_value(item1)

    assert actual_average == pytest.approx(expected_average)


def test_get_counters(sample_periodic_item_quantity):
    # Arrange
    period = 1
    expected_counter = Counter({Item(id=1): 10, Item(id=2): 20})

    # Act
    result = sample_periodic_item_quantity.get_counters(period)

    # Assert
    assert result == expected_counter


def test_cut_off_periods_lower_than(sample_periodic_item_quantity):
    # Arrange
    cutoff_period = 2

    # Act
    result = sample_periodic_item_quantity.cut_off_periods_lower_than(cutoff_period)

    # Assert
    assert result.lowest_period == 2
    assert result.highest_period == 3
    assert set(result.get_periods()) == {2, 3}
    assert result.get_value_for_item(2, Item(id=1)) == 15
    assert result.get_value_for_item(2, Item(id=2)) == 25
    assert result.get_value_for_item(3, Item(id=1)) == 5
    assert result.get_value_for_item(3, Item(id=2)) == 15


def test_with_starting_period(sample_periodic_item_quantity):
    # Arrange
    original = sample_periodic_item_quantity
    expected_start = 5

    # Act
    adjusted = original.with_starting_period(expected_start)

    # Assert
    assert adjusted.lowest_period == expected_start
    assert adjusted.highest_period == expected_start + 2
    assert adjusted.get_periods() == [5, 6, 7]

    for original_period, adjusted_period in zip(original.get_periods(), adjusted.get_periods(), strict=False):
        for item in original.get_unique_items():
            assert original.get_value_for_item(original_period, item) == adjusted.get_value_for_item(
                    adjusted_period,
                    item
            )


def test_different_items_in_periods_raises_value_error(sample_periodic_item_quantity):
    item1 = Item(id=1)
    item2 = Item(id=2)
    item3 = Item(id=3)

    invalid_data = {
            1: {item1: 10, item2: 20},
            2: {item1: 15, item2: 25},
            3: {item1: 5, item3: 15}  # item3 instead of item2
    }

    with pytest.raises(ValueError, match="Items are not the same in every period !"):
        PeriodicItemQuantity(invalid_data)


def test_has_continuous_periods(sample_periodic_item_quantity):
    assert sample_periodic_item_quantity.has_continuous_periods()

    # Create a non-continuous PeriodicItemQuantity
    item1 = Item(id=1)
    item2 = Item(id=2)
    non_continuous_data = {
            1: {item1: 10, item2: 20},
            2: {item1: 15, item2: 25},
            4: {item1: 5, item2: 15}  # Note the gap (period 3 is missing)
    }
    non_continuous_piq = PeriodicItemQuantity(non_continuous_data)
    assert not non_continuous_piq.has_continuous_periods()
