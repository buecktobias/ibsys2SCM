from material.core.resource_counter import ResourceCounterBuilder
from material.graph.nodes.graph_nodes import Bought, StepProduced, FullProduced
from material.graph.nodes.process import Process
from material.graph.production_graph.base_graph import MaterialProductGraphBuilder


# noinspection PyPep8Naming
def create_full_production_graph():
    graph = MaterialProductGraphBuilder("Full Production Graph")

    subX = graph.create_subgraph("X")
    sub1 = graph.create_subgraph("1")
    sub2 = graph.create_subgraph("2")
    sub3 = graph.create_subgraph("3")

    subgraph_XA = subX.create_subgraph("XA")
    subgraph_XB = subX.create_subgraph("XB")
    subgraph_XC = subX.create_subgraph("XC")

    subgraph_1A = sub1.create_subgraph("1A")
    subgraph_1B = sub1.create_subgraph("1B")
    subgraph_1C = sub1.create_subgraph("1C")
    subgraph_1D = sub1.create_subgraph("1D")
    subgraph_1E = sub1.create_subgraph("1E")
    subgraph_1w = sub1.create_subgraph("1w")
    subgraph_1x = sub1.create_subgraph("1x")
    subgraph_1y = sub1.create_subgraph("1y")
    subgraph_1z = sub1.create_subgraph("1z")

    subgraph_2A = sub2.create_subgraph("2A")
    subgraph_2B = sub2.create_subgraph("2B")
    subgraph_2C = sub2.create_subgraph("2C")
    subgraph_2D = sub2.create_subgraph("2D")
    subgraph_2E = sub2.create_subgraph("2E")
    subgraph_2w = sub2.create_subgraph("2w")
    subgraph_2x = sub2.create_subgraph("2x")
    subgraph_2y = sub2.create_subgraph("2y")
    subgraph_2z = sub2.create_subgraph("2z")

    subgraph_3A = sub3.create_subgraph("3A")
    subgraph_3B = sub3.create_subgraph("3B")
    subgraph_3C = sub3.create_subgraph("3C")
    subgraph_3D = sub3.create_subgraph("3D")
    subgraph_3E = sub3.create_subgraph("3E")
    subgraph_3w = sub3.create_subgraph("3w")
    subgraph_3x = sub3.create_subgraph("3x")
    subgraph_3y = sub3.create_subgraph("3y")
    subgraph_3z = sub3.create_subgraph("3z")

    subgraph_XA.add_process(
        Process(
            workstation_id=15,
            process_duration=3,
            setup_duration=15,
            inputs=
            ResourceCounterBuilder()
            .add_items([Bought(43), Bought(44), Bought(45), Bought(46)])
            .build(),
            output=FullProduced(17)
        )
    )
    p16 = FullProduced(16)
    p16_1 = StepProduced(p16, 1)

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
            output=p16
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
            output=StepProduced(FullProduced(26), 1)
        )
    )
    subgraph_XC.add_process(
        Process(
            workstation_id=15,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(26), 1)])
            .add_items([Bought(47)])
            .build(),
            output=FullProduced(26)
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
            output=StepProduced(FullProduced(13), 1)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(13), 1)])
            .build(),
            output=StepProduced(FullProduced(13), 2)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(13), 2)])
            .build(),
            output=StepProduced(FullProduced(13), 3)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(13), 3)])
            .add_items([Bought(32)])
            .build(),
            output=StepProduced(FullProduced(13), 4)
        )
    )
    subgraph_1A.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(13), 4)])
            .build(),
            output=FullProduced(13)
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
            output=StepProduced(FullProduced(18), 1)
        )
    )
    subgraph_1B.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(18), 1)])
            .build(),
            output=StepProduced(FullProduced(18), 2)
        )
    )
    subgraph_1B.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(18), 2)])
            .add(Bought(59), 2)
            .build(),
            output=StepProduced(FullProduced(18), 3)
        )
    )
    subgraph_1B.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(18), 3)])
            .build(),
            output=FullProduced(18)
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
            output=StepProduced(FullProduced(7), 1)
        )
    )
    subgraph_1C.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(7), 1)])
            .add(Bought(35), 2)
            .add(Bought(37), 2)
            .add_items([Bought(38)])
            .build(),
            output=FullProduced(7)
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
            output=StepProduced(FullProduced(4), 1)
        )
    )
    subgraph_1D.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(4), 1)])
            .add(Bought(35), 2)
            .add_items([Bought(36)])
            .build(),
            output=FullProduced(4)
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
            output=StepProduced(FullProduced(10), 1)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(10), 1)])
            .build(),
            output=StepProduced(FullProduced(10), 2)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(10), 2)])
            .build(),
            output=StepProduced(FullProduced(10), 3)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(10), 3)])
            .build(),
            output=StepProduced(FullProduced(10), 4)
        )
    )
    subgraph_1E.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(10), 4)])
            .build(),
            output=FullProduced(10)
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
            .add_items([FullProduced(13)])
            .add_items([FullProduced(18)])
            .add_items([FullProduced(7)])
            .build(),
            output=FullProduced(49)
        )
    )

    subgraph_1x.add_process(
        Process(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(49)])
            .add_items([FullProduced(4)])
            .add_items([FullProduced(10)])
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .build(),
            output=FullProduced(50)
        )
    )

    subgraph_1y.add_process(
        Process(
            workstation_id=3,
            process_duration=5,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(17)])
            .add_items([FullProduced(16)])
            .add_items([FullProduced(50)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=FullProduced(51)
        )
    )

    subgraph_1z.add_process(
        Process(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(26)])
            .add_items([FullProduced(51)])
            .add_items([Bought(21)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=FullProduced(1)
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
            output=StepProduced(FullProduced(14), 1)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(14), 1)])
            .build(),
            output=StepProduced(FullProduced(14), 2)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(14), 2)])
            .build(),
            output=StepProduced(FullProduced(14), 3)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(14), 3)])
            .add_items([Bought(32)])
            .build(),
            output=StepProduced(FullProduced(14), 4)
        )
    )
    subgraph_2A.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(14), 4)])
            .build(),
            output=FullProduced(14)
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
            output=StepProduced(FullProduced(19), 1)
        )
    )
    subgraph_2B.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(19), 1)])
            .build(),
            output=StepProduced(FullProduced(19), 2)
        )
    )
    subgraph_2B.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(19), 2)])
            .add(Bought(59), 2)
            .build(),
            output=StepProduced(FullProduced(19), 3)
        )
    )
    subgraph_2B.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(19), 3)])
            .build(),
            output=FullProduced(19)
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
            output=StepProduced(FullProduced(8), 1)
        )
    )
    subgraph_2C.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(8), 1)])
            .add(Bought(35), 2)
            .add(Bought(37), 2)
            .add_items([Bought(38)])
            .build(),
            output=FullProduced(8)
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
            output=StepProduced(FullProduced(5), 1)
        )
    )
    subgraph_2D.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(5), 1)])
            .add(Bought(35), 2)
            .add_items([Bought(36)])
            .build(),
            output=FullProduced(5)
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
            output=StepProduced(FullProduced(11), 1)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(11), 1)])
            .build(),
            output=StepProduced(FullProduced(11), 2)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(11), 2)])
            .build(),
            output=StepProduced(FullProduced(11), 3)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(11), 3)])
            .build(),
            output=StepProduced(FullProduced(11), 4)
        )
    )
    subgraph_2E.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(11), 4)])
            .build(),
            output=FullProduced(11)
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
            .add_items([FullProduced(14)])
            .add_items([FullProduced(19)])
            .add_items([FullProduced(8)])
            .build(),
            output=FullProduced(54)
        )
    )

    # Old group x becomes 2x:
    subgraph_2x.add_process(
        Process(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(54)])
            .add_items([FullProduced(5)])
            .add_items([FullProduced(11)])
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .build(),
            output=FullProduced(55)
        )
    )

    # Old group y becomes 2y:
    subgraph_2y.add_process(
        Process(
            workstation_id=3,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(17)])
            .add_items([FullProduced(16)])
            .add_items([FullProduced(55)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=FullProduced(56)
        )
    )

    # Old group z becomes 2z:
    subgraph_2z.add_process(
        Process(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(26)])
            .add_items([FullProduced(56)])
            .add_items([Bought(22)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=FullProduced(2)
        )
    )

    subgraph_3A.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(FullProduced(15), 1)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(15), 1)])
            .build(),
            output=StepProduced(FullProduced(15), 2)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=8,
            process_duration=2,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(15), 2)])
            .build(),
            output=StepProduced(FullProduced(15), 3)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(15), 3)])
            .add_items([Bought(32)])
            .build(),
            output=StepProduced(FullProduced(15), 4)
        )
    )
    subgraph_3A.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(15), 4)])
            .build(),
            output=FullProduced(15)
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
            output=StepProduced(FullProduced(20), 1)
        )
    )
    subgraph_3B.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(20), 1)])
            .build(),
            output=StepProduced(FullProduced(20), 2)
        )
    )
    subgraph_3B.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(20), 2)])
            .add(Bought(59), 2)
            .build(),
            output=StepProduced(FullProduced(20), 3)
        )
    )
    subgraph_3B.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(20), 3)])
            .build(),
            output=FullProduced(20)
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
            output=StepProduced(FullProduced(9), 1)
        )
    )
    subgraph_3C.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(9), 1)])
            .add(Bought(35), 2)
            .add(Bought(37), 2)
            .add_items([Bought(38)])
            .build(),
            output=FullProduced(9)
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
            output=StepProduced(FullProduced(6), 1)
        )
    )
    subgraph_3D.add_process(
        Process(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(6), 1)])
            .add(Bought(35), 2)
            .add_items([Bought(36)])
            .build(),
            output=FullProduced(6)
        )
    )

    subgraph_3E.add_process(
        Process(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([Bought(39)])
            .build(),
            output=StepProduced(FullProduced(12), 1)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(12), 1)])
            .build(),
            output=StepProduced(FullProduced(12), 2)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(12), 2)])
            .build(),
            output=StepProduced(FullProduced(12), 3)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(12), 3)])
            .build(),
            output=StepProduced(FullProduced(12), 4)
        )
    )
    subgraph_3E.add_process(
        Process(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([StepProduced(FullProduced(12), 4)])
            .build(),
            output=FullProduced(12)
        )
    )

    subgraph_3w.add_process(
        Process(
            workstation_id=1,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .add_items([FullProduced(15)])
            .add_items([FullProduced(20)])
            .add_items([FullProduced(9)])
            .build(),
            output=FullProduced(29)
        )
    )

    subgraph_3x.add_process(
        Process(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(29)])
            .add_items([FullProduced(6)])
            .add_items([FullProduced(12)])
            .add(Bought(24), 2)
            .add(Bought(25), 2)
            .build(),
            output=FullProduced(30)
        )
    )

    subgraph_3y.add_process(
        Process(
            workstation_id=3,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(17)])
            .add_items([FullProduced(16)])
            .add_items([FullProduced(30)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=FullProduced(31)
        )
    )

    subgraph_3z.add_process(
        Process(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([FullProduced(26)])
            .add_items([FullProduced(31)])
            .add_items([Bought(23)])
            .add_items([Bought(24)])
            .add_items([Bought(27)])
            .build(),
            output=FullProduced(3)
        )
    )

    return graph.build()
