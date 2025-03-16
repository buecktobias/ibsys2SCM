from material.graph.production_graph import MaterialProductFlowGraph, SubGraph


# noinspection PyPep8Naming
def create_graph_p1():
    graph = MaterialProductFlowGraph()

    def create_sub_graph(label):
        return SubGraph(label, graph)

    # Create subgraph builders for each group.
    subgraph_A = create_sub_graph("A")
    subgraph_B = create_sub_graph("B")
    subgraph_C = create_sub_graph("C")
    subgraph_D = create_sub_graph("D")
    subgraph_E = create_sub_graph("E")
    subgraph_F = create_sub_graph("F")
    subgraph_G = create_sub_graph("G")
    subgraph_H = create_sub_graph("H")
    subgraph_w = create_sub_graph("w")
    subgraph_x = create_sub_graph("x")
    subgraph_y = create_sub_graph("y")
    subgraph_z = create_sub_graph("z")

    # For each process, provide inputs (map of item uid to weight) and output uid.
    subgraph_A.add_process(
        workstation_id=15,
        process_duration=3,
        setup_duration=15,
        inputs={"K43": 1, "K44": 1, "K45": 1, "K46": 1},
        output_uid="E17"
    )

    subgraph_B.add_process(
        workstation_id=6,
        process_duration=2,
        setup_duration=15,
        inputs={"K28": 1},
        output_uid="E14"
    )
    subgraph_B.add_process(
        workstation_id=14,
        process_duration=3,
        setup_duration=0,
        inputs={"E14": 1, "K24": 1, "K40": 1, "K41": 1, "K42": 2},
        output_uid="E16"
    )

    subgraph_C.add_process(
        workstation_id=13,
        process_duration=2,
        setup_duration=0,
        inputs={"K39": 1},
        output_uid="E12"
    )
    subgraph_C.add_process(
        workstation_id=12,
        process_duration=3,
        setup_duration=0,
        inputs={"E12": 1},
        output_uid="E8"
    )
    subgraph_C.add_process(
        workstation_id=8,
        process_duration=1,
        setup_duration=15,
        inputs={"E8": 1},
        output_uid="E7"
    )
    subgraph_C.add_process(
        workstation_id=7,
        process_duration=2,
        setup_duration=20,
        inputs={"E7": 1, "K32": 1},
        output_uid="E9"
    )
    subgraph_C.add_process(
        workstation_id=9,
        process_duration=3,
        setup_duration=15,
        inputs={"E9": 1},
        output_uid="E13"
    )

    subgraph_D.add_process(
        workstation_id=6,
        process_duration=3,
        setup_duration=15,
        inputs={"K28": 3},
        output_uid="E8D"
    )
    subgraph_D.add_process(
        workstation_id=8,
        process_duration=1,
        setup_duration=15,
        inputs={"E8D": 1, "K59": 2},
        output_uid="E7D"
    )
    subgraph_D.add_process(
        workstation_id=7,
        process_duration=2,
        setup_duration=20,
        inputs={"E7D": 1, "K32": 2},
        output_uid="E9D"
    )
    subgraph_D.add_process(
        workstation_id=9,
        process_duration=3,
        setup_duration=15,
        inputs={"E9D": 1},
        output_uid="E18"
    )

    subgraph_E.add_process(
        workstation_id=10,
        process_duration=4,
        setup_duration=20,
        inputs={"K52": 1, "K53": 36},
        output_uid="E11"
    )
    subgraph_E.add_process(
        workstation_id=11,
        process_duration=3,
        setup_duration=20,
        inputs={"E11": 1, "K35": 2, "K37": 2, "K38": 1},
        output_uid="E7"
    )

    subgraph_F.add_process(
        workstation_id=10,
        process_duration=4,
        setup_duration=20,
        inputs={"K52": 1, "K53": 36},
        output_uid="E11F"
    )
    subgraph_F.add_process(
        workstation_id=11,
        process_duration=3,
        setup_duration=10,
        inputs={"E11F": 1, "K35": 2, "K36": 1},
        output_uid="E4"
    )

    subgraph_G.add_process(
        workstation_id=13,
        process_duration=2,
        setup_duration=0,
        inputs={"K39": 1},
        output_uid="E12G"
    )
    subgraph_G.add_process(
        workstation_id=12,
        process_duration=3,
        setup_duration=0,
        inputs={"E12G": 1},
        output_uid="E8G"
    )
    subgraph_G.add_process(
        workstation_id=8,
        process_duration=1,
        setup_duration=15,
        inputs={"E8G": 1},
        output_uid="E7G"
    )
    subgraph_G.add_process(
        workstation_id=7,
        process_duration=2,
        setup_duration=20,
        inputs={"E7G": 1},
        output_uid="E9G"
    )
    subgraph_G.add_process(
        workstation_id=9,
        process_duration=3,
        setup_duration=15,
        inputs={"E9G": 1},
        output_uid="E10"
    )

    subgraph_H.add_process(
        workstation_id=7,
        process_duration=2,
        setup_duration=30,
        inputs={"K44": 2, "K48": 2},
        output_uid="E15H"
    )
    subgraph_H.add_process(
        workstation_id=15,
        process_duration=3,
        setup_duration=15,
        inputs={"E15H": 1, "K47": 1},
        output_uid="E26"
    )

    subgraph_w.add_process(
        workstation_id=1,
        process_duration=6,
        setup_duration=20,
        inputs={"K24": 2, "K25": 2, "K26": 2, "E13": 1, "E18": 1, "E7": 1},
        output_uid="E49"
    )

    subgraph_x.add_process(
        workstation_id=2,
        process_duration=5,
        setup_duration=30,
        inputs={"E49": 1, "E4": 1, "E10": 1, "K24": 2, "K25": 2},
        output_uid="E50"
    )

    subgraph_y.add_process(
        workstation_id=3,
        process_duration=5,
        setup_duration=20,
        inputs={"E17": 1, "E16": 1, "E50": 1, "K24": 1, "K27": 1},
        output_uid="E51"
    )

    subgraph_z.add_process(
        workstation_id=4,
        process_duration=6,
        setup_duration=30,
        inputs={"E26": 1, "E51": 1, "K21": 1, "K24": 1, "K27": 1},
        output_uid="E1"
    )

    graph.child_node_aggregates.extend(
        [
            subgraph_A, subgraph_B, subgraph_C, subgraph_D, subgraph_E,
            subgraph_F, subgraph_G, subgraph_H, subgraph_w, subgraph_x,
            subgraph_y, subgraph_z
        ]
    )

    return graph
