from material.core.resource_counter import ResourceCounter
from material.graph.nodes.graph_nodes import Item, StepProduced
from material.graph.nodes.mermaid_node import LabeledGraphNode
from material.graph.nodes.production_node_type import ProductionNodeType


class Process(LabeledGraphNode):
    """
    Represents a process node in the nx_graph.

    Attributes:
        _workstation_id (int): The identifier for the workstation.
        _process_duration (int): The duration of the process.
        _setup_duration (int): The setup duration before the process.
        _inputs (dict[Item, int], optional): A dictionary mapping input Items to their required quantities.
        _output (Item, optional): The output Item of the process.
    """
    _output: Item
    _inputs: ResourceCounter
    _setup_duration: int
    _process_duration: int
    _workstation_id: int

    def __init__(self, workstation_id: int, process_duration: int, setup_duration: int,
                 inputs: ResourceCounter, output: Item):
        if isinstance(output, StepProduced):
            output.produced_by_workstation = workstation_id
        self._workstation_id = workstation_id
        self._process_duration = process_duration
        self._setup_duration = setup_duration
        self._inputs = inputs
        self._output = output

    @property
    def workstation_id(self):
        return self._workstation_id

    @property
    def unique_numerical_id(self):
        return self.workstation_id * 10 ** 4 + self.output.node_numerical_id

    @property
    def inputs(self):
        return self._inputs

    @property
    def output(self):
        return self._output

    @property
    def process_duration(self):
        return self._process_duration

    @property
    def setup_duration(self):
        return self._setup_duration

    @property
    def node_type(self):
        """
        Returns the production node diagram_type for a process, which is always PROCESS.
        """
        return ProductionNodeType.PROCESS

    @property
    def label(self):
        return f"{ProductionNodeType.PROCESS.value}{self.workstation_id}_{self.output.node_numerical_id}"

    def __hash__(self):
        return hash((self._workstation_id, self._output, self._inputs, self.setup_duration, self.process_duration))

    def __eq__(self, other):
        if not isinstance(other, Process):
            return False
        return self._workstation_id == other.workstation_id and self._output == other.output and \
            self._inputs == other.inputs and self.setup_duration == other.setup_duration and \
            self.process_duration == other.process_duration
