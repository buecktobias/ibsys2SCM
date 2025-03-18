from material.core.resource_counter import ResourceCounter
from material.graph.nodes.graph_nodes import Item, Node
from material.graph.nodes.production_node_type import ProductionNodeType


class Process(Node):
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
        self._process_id = f"{workstation_id}_{output.node_numerical_id}"
        self._workstation_id = workstation_id
        self._process_duration = process_duration
        self._setup_duration = setup_duration
        self._inputs = inputs
        self._output = output

    def __validate_process_id(self):
        assert str(self._workstation_id) in self._process_id, "Workstation ID not in process ID."
        assert "_" in self._process_id, "Process ID does not contain an underscore."

    @property
    def workstation_id(self):
        return self._workstation_id

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
        Returns the production node type for a process, which is always PROCESS.
        """
        return ProductionNodeType.PROCESS

    @property
    def node_id(self):
        return f"{ProductionNodeType.PROCESS.value}{self._process_id}"

    def __repr__(self):
        return f"{self.node_id}"

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.node_id == other.node_id
