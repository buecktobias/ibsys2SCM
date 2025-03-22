from material.core.resource_counter import ResourceCounterBuilder
from material.initialize_db.graph.nodes.domainprocess import DomainProcess
from material.initialize_db.graph.nodes.graph_nodes import DomainItem, DomainBought, DomainFullProduced, \
    DomainStepProduced
from material.initialize_db.graph.production_graph.base_graph import MaterialProductGraphBuilder


# noinspection PyPep8Naming
def create_full_production_graph():
    graph = MaterialProductGraphBuilder("Full Production GraphORM", 1_000_000)

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
        DomainProcess(
            workstation_id=15,
            process_duration=3,
            setup_duration=15,
            inputs=
            ResourceCounterBuilder[DomainItem]()
            .add_items([DomainBought(43), DomainBought(44), DomainBought(45), DomainBought(46)])
            .build(),
            output=DomainFullProduced(17)
        )
    )
    p16 = DomainFullProduced(16)
    p16_1 = DomainStepProduced(p16, 1)

    subgraph_XB.add_process(
        DomainProcess(
            workstation_id=6,
            process_duration=2,
            setup_duration=15,
            inputs=ResourceCounterBuilder().add_items([DomainBought(28)]).build(),
            output=p16_1
        )
    )
    subgraph_XB.add_process(
        DomainProcess(
            workstation_id=14,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(24), p16_1])
            .add_items([DomainBought(40)])
            .add_items([DomainBought(41)])
            .add(DomainBought(42), 2)
            .build(),
            output=p16
        )
    )

    subgraph_XC.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add(DomainBought(44), 2)
            .add(DomainBought(48), 2)
            .build(),
            output=DomainStepProduced(DomainFullProduced(26), 1)
        )
    )
    subgraph_XC.add_process(
        DomainProcess(
            workstation_id=15,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(26), 1)])
            .add_items([DomainBought(47)])
            .build(),
            output=DomainFullProduced(26)
        )
    )

    subgraph_1A.add_process(
        DomainProcess(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(39)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(13), 1)
        )
    )
    subgraph_1A.add_process(
        DomainProcess(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(13), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(13), 2)
        )
    )
    subgraph_1A.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(13), 2)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(13), 3)
        )
    )
    subgraph_1A.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(13), 3)])
            .add_items([DomainBought(32)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(13), 4)
        )
    )
    subgraph_1A.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(13), 4)])
            .build(),
            output=DomainFullProduced(13)
        )
    )

    subgraph_1B.add_process(
        DomainProcess(
            workstation_id=6,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add(DomainBought(28), 3)
            .build(),
            output=DomainStepProduced(DomainFullProduced(18), 1)
        )
    )
    subgraph_1B.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(18), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(18), 2)
        )
    )
    subgraph_1B.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(18), 2)])
            .add(DomainBought(59), 2)
            .build(),
            output=DomainStepProduced(DomainFullProduced(18), 3)
        )
    )
    subgraph_1B.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(18), 3)])
            .build(),
            output=DomainFullProduced(18)
        )
    )

    subgraph_1C.add_process(
        DomainProcess(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(52)])
            .add(DomainBought(53), 36)
            .build(),
            output=DomainStepProduced(DomainFullProduced(7), 1)
        )
    )
    subgraph_1C.add_process(
        DomainProcess(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(7), 1)])
            .add(DomainBought(35), 2)
            .add(DomainBought(37), 2)
            .add_items([DomainBought(38)])
            .build(),
            output=DomainFullProduced(7)
        )
    )

    subgraph_1D.add_process(
        DomainProcess(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(52)])
            .add(DomainBought(53), 36)
            .build(),
            output=DomainStepProduced(DomainFullProduced(4), 1)
        )
    )
    subgraph_1D.add_process(
        DomainProcess(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(4), 1)])
            .add(DomainBought(35), 2)
            .add_items([DomainBought(36)])
            .build(),
            output=DomainFullProduced(4)
        )
    )

    subgraph_1E.add_process(
        DomainProcess(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(39)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(10), 1)
        )
    )
    subgraph_1E.add_process(
        DomainProcess(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(10), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(10), 2)
        )
    )
    subgraph_1E.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(10), 2)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(10), 3)
        )
    )
    subgraph_1E.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(10), 3)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(10), 4)
        )
    )
    subgraph_1E.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(10), 4)])
            .build(),
            output=DomainFullProduced(10)
        )
    )

    subgraph_1w.add_process(
        DomainProcess(
            workstation_id=1,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add(DomainBought(24), 2)
            .add(DomainBought(25), 2)
            .add_items([DomainFullProduced(13)])
            .add_items([DomainFullProduced(18)])
            .add_items([DomainFullProduced(7)])
            .build(),
            output=DomainFullProduced(49)
        )
    )

    subgraph_1x.add_process(
        DomainProcess(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(49)])
            .add_items([DomainFullProduced(4)])
            .add_items([DomainFullProduced(10)])
            .add(DomainBought(24), 2)
            .add(DomainBought(25), 2)
            .build(),
            output=DomainFullProduced(50)
        )
    )

    subgraph_1y.add_process(
        DomainProcess(
            workstation_id=3,
            process_duration=5,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(17)])
            .add_items([DomainFullProduced(16)])
            .add_items([DomainFullProduced(50)])
            .add_items([DomainBought(24)])
            .add_items([DomainBought(27)])
            .build(),
            output=DomainFullProduced(51)
        )
    )

    subgraph_1z.add_process(
        DomainProcess(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(26)])
            .add_items([DomainFullProduced(51)])
            .add_items([DomainBought(21)])
            .add_items([DomainBought(24)])
            .add_items([DomainBought(27)])
            .build(),
            output=DomainFullProduced(1)
        )
    )

    subgraph_2A.add_process(
        DomainProcess(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(39)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(14), 1)
        )
    )
    subgraph_2A.add_process(
        DomainProcess(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(14), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(14), 2)
        )
    )
    subgraph_2A.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(14), 2)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(14), 3)
        )
    )
    subgraph_2A.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(14), 3)])
            .add_items([DomainBought(32)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(14), 4)
        )
    )
    subgraph_2A.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(14), 4)])
            .build(),
            output=DomainFullProduced(14)
        )
    )

    # Old group D becomes 2B:
    subgraph_2B.add_process(
        DomainProcess(
            workstation_id=6,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add(DomainBought(28), 3)
            .build(),
            output=DomainStepProduced(DomainFullProduced(19), 1)
        )
    )
    subgraph_2B.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(19), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(19), 2)
        )
    )
    subgraph_2B.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(19), 2)])
            .add(DomainBought(59), 2)
            .build(),
            output=DomainStepProduced(DomainFullProduced(19), 3)
        )
    )
    subgraph_2B.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(19), 3)])
            .build(),
            output=DomainFullProduced(19)
        )
    )

    # Old group E becomes 2C:
    subgraph_2C.add_process(
        DomainProcess(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(57)])
            .add(DomainBought(58), 36)
            .build(),
            output=DomainStepProduced(DomainFullProduced(8), 1)
        )
    )
    subgraph_2C.add_process(
        DomainProcess(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(8), 1)])
            .add(DomainBought(35), 2)
            .add(DomainBought(37), 2)
            .add_items([DomainBought(38)])
            .build(),
            output=DomainFullProduced(8)
        )
    )

    # Old group F becomes 2D:
    subgraph_2D.add_process(
        DomainProcess(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(57)])
            .add(DomainBought(58), 36)
            .build(),
            output=DomainStepProduced(DomainFullProduced(5), 1)
        )
    )
    subgraph_2D.add_process(
        DomainProcess(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(5), 1)])
            .add(DomainBought(35), 2)
            .add_items([DomainBought(36)])
            .build(),
            output=DomainFullProduced(5)
        )
    )

    # Old group G becomes 2E:
    subgraph_2E.add_process(
        DomainProcess(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(39)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(11), 1)
        )
    )
    subgraph_2E.add_process(
        DomainProcess(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(11), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(11), 2)
        )
    )
    subgraph_2E.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(11), 2)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(11), 3)
        )
    )
    subgraph_2E.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(11), 3)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(11), 4)
        )
    )
    subgraph_2E.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(11), 4)])
            .build(),
            output=DomainFullProduced(11)
        )
    )

    # Old group w becomes 2w:
    subgraph_2w.add_process(
        DomainProcess(
            workstation_id=1,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add(DomainBought(24), 2)
            .add(DomainBought(25), 2)
            .add_items([DomainFullProduced(14)])
            .add_items([DomainFullProduced(19)])
            .add_items([DomainFullProduced(8)])
            .build(),
            output=DomainFullProduced(54)
        )
    )

    # Old group x becomes 2x:
    subgraph_2x.add_process(
        DomainProcess(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(54)])
            .add_items([DomainFullProduced(5)])
            .add_items([DomainFullProduced(11)])
            .add(DomainBought(24), 2)
            .add(DomainBought(25), 2)
            .build(),
            output=DomainFullProduced(55)
        )
    )

    # Old group y becomes 2y:
    subgraph_2y.add_process(
        DomainProcess(
            workstation_id=3,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(17)])
            .add_items([DomainFullProduced(16)])
            .add_items([DomainFullProduced(55)])
            .add_items([DomainBought(24)])
            .add_items([DomainBought(27)])
            .build(),
            output=DomainFullProduced(56)
        )
    )

    # Old group z becomes 2z:
    subgraph_2z.add_process(
        DomainProcess(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(26)])
            .add_items([DomainFullProduced(56)])
            .add_items([DomainBought(22)])
            .add_items([DomainBought(24)])
            .add_items([DomainBought(27)])
            .build(),
            output=DomainFullProduced(2)
        )
    )

    subgraph_3A.add_process(
        DomainProcess(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(39)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(15), 1)
        )
    )
    subgraph_3A.add_process(
        DomainProcess(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(15), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(15), 2)
        )
    )
    subgraph_3A.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=2,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(15), 2)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(15), 3)
        )
    )
    subgraph_3A.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(15), 3)])
            .add_items([DomainBought(32)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(15), 4)
        )
    )
    subgraph_3A.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(15), 4)])
            .build(),
            output=DomainFullProduced(15)
        )
    )

    # Group 3B (old group D -> 3B):
    subgraph_3B.add_process(
        DomainProcess(
            workstation_id=6,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add(DomainBought(28), 3)
            .build(),
            output=DomainStepProduced(DomainFullProduced(20), 1)
        )
    )
    subgraph_3B.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(20), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(20), 2)
        )
    )
    subgraph_3B.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(20), 2)])
            .add(DomainBought(59), 2)
            .build(),
            output=DomainStepProduced(DomainFullProduced(20), 3)
        )
    )
    subgraph_3B.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(20), 3)])
            .build(),
            output=DomainFullProduced(20)
        )
    )

    # Group 3C (old group E -> 3C):
    subgraph_3C.add_process(
        DomainProcess(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(57)])
            .add(DomainBought(58), 36)
            .build(),
            output=DomainStepProduced(DomainFullProduced(9), 1)
        )
    )
    subgraph_3C.add_process(
        DomainProcess(
            workstation_id=11,
            process_duration=3,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(9), 1)])
            .add(DomainBought(35), 2)
            .add(DomainBought(37), 2)
            .add_items([DomainBought(38)])
            .build(),
            output=DomainFullProduced(9)
        )
    )

    # Group 3D (old group F -> 3D):
    subgraph_3D.add_process(
        DomainProcess(
            workstation_id=10,
            process_duration=4,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(33)])
            .add(DomainBought(34), 36)
            .build(),
            output=DomainStepProduced(DomainFullProduced(6), 1)
        )
    )
    subgraph_3D.add_process(
        DomainProcess(
            workstation_id=11,
            process_duration=3,
            setup_duration=10,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(6), 1)])
            .add(DomainBought(35), 2)
            .add_items([DomainBought(36)])
            .build(),
            output=DomainFullProduced(6)
        )
    )

    subgraph_3E.add_process(
        DomainProcess(
            workstation_id=13,
            process_duration=2,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainBought(39)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(12), 1)
        )
    )
    subgraph_3E.add_process(
        DomainProcess(
            workstation_id=12,
            process_duration=3,
            setup_duration=0,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(12), 1)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(12), 2)
        )
    )
    subgraph_3E.add_process(
        DomainProcess(
            workstation_id=8,
            process_duration=1,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(12), 2)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(12), 3)
        )
    )
    subgraph_3E.add_process(
        DomainProcess(
            workstation_id=7,
            process_duration=2,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(12), 3)])
            .build(),
            output=DomainStepProduced(DomainFullProduced(12), 4)
        )
    )
    subgraph_3E.add_process(
        DomainProcess(
            workstation_id=9,
            process_duration=3,
            setup_duration=15,
            inputs=ResourceCounterBuilder()
            .add_items([DomainStepProduced(DomainFullProduced(12), 4)])
            .build(),
            output=DomainFullProduced(12)
        )
    )

    subgraph_3w.add_process(
        DomainProcess(
            workstation_id=1,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add(DomainBought(24), 2)
            .add(DomainBought(25), 2)
            .add_items([DomainFullProduced(15)])
            .add_items([DomainFullProduced(20)])
            .add_items([DomainFullProduced(9)])
            .build(),
            output=DomainFullProduced(29)
        )
    )

    subgraph_3x.add_process(
        DomainProcess(
            workstation_id=2,
            process_duration=5,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(29)])
            .add_items([DomainFullProduced(6)])
            .add_items([DomainFullProduced(12)])
            .add(DomainBought(24), 2)
            .add(DomainBought(25), 2)
            .build(),
            output=DomainFullProduced(30)
        )
    )

    subgraph_3y.add_process(
        DomainProcess(
            workstation_id=3,
            process_duration=6,
            setup_duration=20,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(17)])
            .add_items([DomainFullProduced(16)])
            .add_items([DomainFullProduced(30)])
            .add_items([DomainBought(24)])
            .add_items([DomainBought(27)])
            .build(),
            output=DomainFullProduced(31)
        )
    )

    subgraph_3z.add_process(
        DomainProcess(
            workstation_id=4,
            process_duration=6,
            setup_duration=30,
            inputs=ResourceCounterBuilder()
            .add_items([DomainFullProduced(26)])
            .add_items([DomainFullProduced(31)])
            .add_items([DomainBought(23)])
            .add_items([DomainBought(24)])
            .add_items([DomainBought(27)])
            .build(),
            output=DomainFullProduced(3)
        )
    )

    return graph.build()
