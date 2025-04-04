import typing

from material.db.models import Process, Item


def get_process_outgoing_to(processes: typing.Collection[Process], item: Item):
    """
    Returns a list of _processes that are outgoing to the given item.
    """
    return [p for p in processes if p.output == item]


def get_process_incoming_from(processes: typing.Collection[Process], item: Item):
    """
    Returns a list of _processes that are incoming from the given item.
    """
    return [p for p in processes if item in p.inputs]
