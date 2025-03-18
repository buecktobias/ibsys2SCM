from material.core.resource_counter import ResourceCounterBuilder
from material.graph.nodes.graph_nodes import Produced, Bought, StepProduced
from material.graph.nodes.process import Process
from material.graph.production_graph.material_product_graph import MaterialProductGraph
from material.graph.sub_graph import SubGraph


# noinspection PyPep8Naming
def create_full_production_graph():
    graph = MaterialProductGraph()

    graph = MaterialProductGraph()

    subX = graph.add_subgraph("X")
    sub1 = graph.add_subgraph("1")
    sub2 = graph.add_subgraph("2")
    sub3 = graph.add_subgraph("3")

    subgraph_XA = subX.add_subgraph("XA")
    subgraph_XB = subX.add_subgraph("XB")
    subgraph_XC = subX.add_subgraph("XC")

    subgraph_1A = sub1.add_subgraph("1A")
    subgraph_1B = sub1.add_subgraph("1B")
    subgraph_1C = sub1.add_subgraph("1C")
    subgraph_1D = sub1.add_subgraph("1D")
    subgraph_1E = sub1.add_subgraph("1E")
    subgraph_1w = sub1.add_subgraph("1w")
    subgraph_1x = sub1.add_subgraph("1x")
    subgraph_1y = sub1.add_subgraph("1y")
    subgraph_1z = sub1.add_subgraph("1z")

    subgraph_2A = sub2.add_subgraph("2A")
    subgraph_2B = sub2.add_subgraph("2B")
    subgraph_2C = sub2.add_subgraph("2C")
    subgraph_2D = sub2.add_subgraph("2D")
    subgraph_2E = sub2.add_subgraph("2E")
    subgraph_2w = sub2.add_subgraph("2w")
    subgraph_2x = sub2.add_subgraph("2x")
    subgraph_2y = sub2.add_subgraph("2y")
    subgraph_2z = sub2.add_subgraph("2z")

    subgraph_3A = sub3.add_subgraph("3A")
    subgraph_3B = sub3.add_subgraph("3B")
    subgraph_3C = sub3.add_subgraph("3C")
    subgraph_3D = sub3.add_subgraph("3D")
    subgraph_3E = sub3.add_subgraph("3E")
    subgraph_3w = sub3.add_subgraph("3w")
    subgraph_3x = sub3.add_subgraph("3x")
    subgraph_3y = sub3.add_subgraph("3y")
    subgraph_3z = sub3.add_subgraph("3z")

    subgraph_XA.add_process(
        Process(
            workstation_id=15,
            process_duration=3,
            setup_duration=15,
            inputs=
            ResourceCounterBuilder()
            .add_items([Bought(43), Bought(44), Bought(45), Bought(46)])
            .build(),
            output=Produced(17)
        )
    )

    p_16 = Produced(16)
    p16_1 = StepProduced(p_16, 1)

    subgraph_XB.add_process(
        Process(
            workstation_id=6,
            process_duration=2,
            setup_duration=15,
            inputs=ResourceCounterBuilder().add_items([Bought(28)]).build(),
            output=p16_1
        )
    )
    subgraph_XB.add_process(
        Process(
            workstation_id=14,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(24), p16_1])
            .add_items([Bought(40)])
            .add_items([Bought(41)])
            .add(Bought(42), 2)
            .build(),
            output=Produced(16)
        )
    )

    subgraph_XC.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add(Bought(44), 2)
            .add(Bought(48), 2)
            .build(),
            output=StepProduced(Produced(26), 1)
        )
    )
    subgraph_XC.add_process(
        Process(
            workstation_id=15,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(26), 1)])
            .add_items([Bought(47)])
            .build(),
            output=Produced(26)
        )
    )

    subgraph_1A.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(Produced(13), 1)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(13), 1)])
            .build(),
            output=StepProduced(Produced(13), 2)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(13), 2)])
            .build(),
            output=StepProduced(Produced(13), 3)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(13), 3)])
            .add_items([Bought(32)])
            .build(),
            output=StepProduced(Produced(13), 4)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(13), 4)])
            .build(),
            output=Produced(13)
        )
    )

    subgraph_1B.add_process(
        Process(
            workstation_id=6,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add(Bought(28), 3)
            .build(),
            output=StepProduced(Produced(18), 1)
        )
    )
    subgraph_1B.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(18), 1)])
            .build(),
            output=StepProduced(Produced(18), 2)
        )
    )
    subgraph_1B.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(18), 2)])
            .add(Bought(59), 2)
            .build(),
            output=StepProduced(Produced(18), 3)
        )
    )
    subgraph_1B.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(18), 3)])
            .build(),
            output=Produced(18)
        )
    )

    subgraph_1C.add_process(
        Process(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(52)])
            .add(Bought(53), 36)
            .build(),
            output=StepProduced(Produced(7), 1)
        )
    )
    subgraph_1C.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(7), 1)])
            .add(Bought(35), 2)
            .add(Bought(37), 2)
            .add_items([Bought(38)])
            .build(),
            output=Produced(7)
        )
    )

    subgraph_1D.add_process(
        Process(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(52)])
            .add(Bought(53), 36)
            .build(),
            output=StepProduced(Produced(4), 1)
        )
    )
    subgraph_1D.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(4), 1)])
            .add(Bought(35), 2)
            .add_items([Bought(36)])
            .build(),
            output=Produced(4)
        )
    )

    subgraph_1E.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(Produced(10), 1)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(10), 1)])
            .build(),
            output=StepProduced(Produced(10), 2)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(10), 2)])
            .build(),
            output=StepProduced(Produced(10), 3)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(10), 3)])
            .build(),
            output=StepProduced(Produced(10), 4)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(10), 4)])
            .build(),
            output=Produced(10)
        )
    )

    subgraph_1w.add_process(
        Process(
            workstation_id=1,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .add_items([Produced(13)])
            .add_items([Produced(18)])
            .add_items([Produced(7)])
            .build(),
            output=Produced(49)
        )
    )

    subgraph_1x.add_process(
        Process(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(49)])
            .add_items([Produced(4)])
            .add_items([Produced(10)])
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .build(),
            output=Produced(50)
        )
    )

    subgraph_1y.add_process(
        Process(
            workstation_id=3,
            process_duration=5,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(17)])
            .add_items([Produced(16)])
            .add_items([Produced(50)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=Produced(51)
        )
    )

    subgraph_1z.add_process(
        Process(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(26)])
            .add_items([Produced(51)])
            .add_items([Bought(21)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=Produced(1)
        )
    )

    subgraph_2A.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(Produced(14), 1)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(14), 1)])
            .build(),
            output=StepProduced(Produced(14), 2)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(14), 2)])
            .build(),
            output=StepProduced(Produced(14), 3)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(14), 3)])
            .add_items([Bought(32)])
            .build(),
            output=StepProduced(Produced(14), 4)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(14), 4)])
            .build(),
            output=Produced(14)
        )
    )

    # Old group D becomes 2B:
    subgraph_2B.add_process(
        Process(
            workstation_id=6,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add(Bought(28), 3)
            .build(),
            output=StepProduced(Produced(19), 1)
        )
    )
    subgraph_2B.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(19), 1)])
            .build(),
            output=StepProduced(Produced(19), 2)
        )
    )
    subgraph_2B.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(19), 2)])
            .add(Bought(59), 2)
            .build(),
            output=StepProduced(Produced(19), 3)
        )
    )
    subgraph_2B.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(19), 3)])
            .build(),
            output=Produced(19)
        )
    )

    # Old group E becomes 2C:
    subgraph_2C.add_process(
        Process(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(57)])
            .add(Bought(58), 36)
            .build(),
            output=StepProduced(Produced(8), 1)
        )
    )
    subgraph_2C.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(8), 1)])
            .add(Bought(35), 2)
            .add(Bought(37), 2)
            .add_items([Bought(38)])
            .build(),
            output=Produced(8)
        )
    )

    # Old group F becomes 2D:
    subgraph_2D.add_process(
        Process(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(57)])
            .add(Bought(58), 36)
            .build(),
            output=StepProduced(Produced(5), 1)
        )
    )
    subgraph_2D.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(5), 1)])
            .add(Bought(35), 2)
            .add_items([Bought(36)])
            .build(),
            output=Produced(5)
        )
    )

    # Old group G becomes 2E:
    subgraph_2E.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(Produced(11), 1)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(11), 1)])
            .build(),
            output=StepProduced(Produced(11), 2)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(11), 2)])
            .build(),
            output=StepProduced(Produced(11), 3)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(11), 3)])
            .build(),
            output=StepProduced(Produced(11), 4)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(11), 4)])
            .build(),
            output=Produced(11)
        )
    )

    # Old group w becomes 2w:
    subgraph_2w.add_process(
        Process(
            workstation_id=1,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .add_items([Produced(14)])
            .add_items([Produced(19)])
            .add_items([Produced(8)])
            .build(),
            output=Produced(54)
        )
    )

    # Old group x becomes 2x:
    subgraph_2x.add_process(
        Process(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(54)])
            .add_items([Produced(5)])
            .add_items([Produced(11)])
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .build(),
            output=Produced(55)
        )
    )

    # Old group y becomes 2y:
    subgraph_2y.add_process(
        Process(
            workstation_id=3,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(17)])
            .add_items([Produced(16)])
            .add_items([Produced(55)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=Produced(56)
        )
    )

    # Old group z becomes 2z:
    subgraph_2z.add_process(
        Process(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(26)])
            .add_items([Produced(56)])
            .add_items([Bought(22)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=Produced(2)
        )
    )

    # Mapping for group 3:
    # A -> XA, B -> XB, C -> 3A, D -> 3B, E -> 3C, F -> 3D, G -> 3E, H -> XC,
    # w -> 3w, x -> 3x, y -> 3y, z -> 3z

    # Group 3A (old group C -> 3A):
    subgraph_3A.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(Produced(15), 1)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(15), 1)])
            .build(),
            output=StepProduced(Produced(15), 2)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=8,
            process_duration=2,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(15), 2)])
            .build(),
            output=StepProduced(Produced(15), 3)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(15), 3)])
            .add_items([Bought(32)])
            .build(),
            output=StepProduced(Produced(15), 4)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(15), 4)])
            .build(),
            output=Produced(15)
        )
    )

    # Group 3B (old group D -> 3B):
    subgraph_3B.add_process(
        Process(
            workstation_id=6,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add(Bought(28), 3)
            .build(),
            output=StepProduced(Produced(20), 1)
        )
    )
    subgraph_3B.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(20), 1)])
            .build(),
            output=StepProduced(Produced(20), 2)
        )
    )
    subgraph_3B.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(20), 2)])
            .add(Bought(59), 2)
            .build(),
            output=StepProduced(Produced(20), 3)
        )
    )
    subgraph_3B.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(20), 3)])
            .build(),
            output=Produced(20)
        )
    )

    # Group 3C (old group E -> 3C):
    subgraph_3C.add_process(
        Process(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(57)])
            .add(Bought(58), 36)
            .build(),
            output=StepProduced(Produced(9), 1)
        )
    )
    subgraph_3C.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(9), 1)])
            .add(Bought(35), 2)
            .add(Bought(37), 2)
            .add_items([Bought(38)])
            .build(),
            output=Produced(9)
        )
    )

    # Group 3D (old group F -> 3D):
    subgraph_3D.add_process(
        Process(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(33)])
            .add(Bought(34), 36)
            .build(),
            output=StepProduced(Produced(6), 1)
        )
    )
    subgraph_3D.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(6), 1)])
            .add(Bought(35), 2)
            .add_items([Bought(36)])
            .build(),
            output=Produced(6)
        )
    )

    # Group 3E (old group G -> 3E):
    subgraph_3E.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(Produced(12), 1)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(12), 1)])
            .build(),
            output=StepProduced(Produced(12), 2)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(12), 2)])
            .build(),
            output=StepProduced(Produced(12), 3)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(12), 3)])
            .build(),
            output=StepProduced(Produced(12), 4)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(Produced(12), 4)])
            .build(),
            output=Produced(12)
        )
    )

    # Group 3w (old group w -> 3w):
    subgraph_3w.add_process(
        Process(
            workstation_id=1,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .add_items([Produced(15)])
            .add_items([Produced(20)])
            .add_items([Produced(9)])
            .build(),
            output=Produced(29)
        )
    )

    # Group 3x (old group x -> 3x):
    subgraph_3x.add_process(
        Process(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(29)])
            .add_items([Produced(6)])
            .add_items([Produced(12)])
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .build(),
            output=Produced(30)
        )
    )

    # Group 3y (old group y -> 3y):
    subgraph_3y.add_process(
        Process(
            workstation_id=3,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(17)])
            .add_items([Produced(16)])
            .add_items([Produced(30)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=Produced(31)
        )
    )

    # Group 3z (old group z -> 3z):
    subgraph_3z.add_process(
        Process(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([Produced(26)])
            .add_items([Produced(31)])
            .add_items([Bought(23)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=Produced(3)
        )
    )

    return graph
