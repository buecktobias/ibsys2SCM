import networkx as nx


def create_graph():
    G = nx.DiGraph()

    # Nodes – non-process (bought and produced) sorted by numeric value
    G.add_node("E4", type="produced")
    G.add_node("E7", type="produced")
    G.add_node("E10", type="produced")
    G.add_node("E13", type="produced")
    G.add_node("E18", type="produced")
    G.add_node("E26", type="produced")
    G.add_node("E49", type="produced")
    G.add_node("E50", type="produced")
    G.add_node("E51", type="produced")
    G.add_node("K21", type="bought")
    G.add_node("K25", type="bought")
    G.add_node("K26", type="bought")
    G.add_node("K27", type="bought")
    G.add_node("K28", type="bought")
    G.add_node("K32", type="bought")
    G.add_node("K35", type="bought")
    G.add_node("K36", type="bought")
    G.add_node("K37", type="bought")
    G.add_node("K38", type="bought")
    G.add_node("K39", type="bought")
    G.add_node("K47", type="bought")
    G.add_node("K52", type="bought")
    G.add_node("K53", type="bought")
    G.add_node("K59", type="bought")


    G.add_node("6.D", type="process", process_duration=3, setup_duration=15)
    G.add_node("7.D", type="process", process_duration=2, setup_duration=20)
    G.add_node("8.D", type="process", process_duration=1, setup_duration=15)
    G.add_node("9.D", type="process", process_duration=3, setup_duration=15)
    G.add_node("12.G", type="process", process_duration=3, setup_duration=0)
    G.add_node("13.G", type="process", process_duration=2, setup_duration=0)
    G.add_node("7.C", type="process", process_duration=2, setup_duration=20)
    G.add_node("8.C", type="process", process_duration=1, setup_duration=15)
    G.add_node("9.C", type="process", process_duration=3, setup_duration=15)
    G.add_node("11.C", type="process", process_duration=3, setup_duration=10)
    G.add_node("12.C", type="process", process_duration=3, setup_duration=0)
    G.add_node("13.C", type="process", process_duration=2, setup_duration=0)
    G.add_node("1.w", type="process", process_duration=6, setup_duration=20)
    G.add_node("2.x", type="process", process_duration=5, setup_duration=30)
    G.add_node("7.H", type="process", process_duration=2, setup_duration=30)
    G.add_node("15.H", type="process", process_duration=3, setup_duration=15)
    G.add_node("4.z", type="process", process_duration=6, setup_duration=30)
    G.add_node("3.y", type="process", process_duration=5, setup_duration=20)

    # Edges sorted by the process letter key and then by flow order (edges in a chain appear before subsequent ones)
    # --- C
    G.add_edge("K39", "13.C", weight=1)
    G.add_edge("13.C", "12.C", weight=1)
    G.add_edge("12.C", "8.C", weight=1)
    G.add_edge("8.C", "7.C", weight=1)
    G.add_edge("K32", "7.C", weight=1)
    G.add_edge("7.C", "9.C", weight=1)
    G.add_edge("9.C", "E13", weight=1)

    # D
    G.add_edge("K28", "6.D", weight=3)
    G.add_edge("6.D", "8.D", weight=1)
    G.add_edge("K59", "8.D", weight=3)
    G.add_edge("8.D", "7.D", weight=1)
    G.add_edge("K32", "7.D", weight=2)
    G.add_edge("7.D", "9.D", weight=1)
    G.add_edge("9.D", "E18", weight=1)

    # E
    G.add_edge("K52", "10.E", weight=1)
    G.add_edge("K53", "10.E", weight=36)
    G.add_edge("10.E", "11.E", weight=1)
    G.add_edge("K35", "11.E", weight=1)
    G.add_edge("K37", "11.E", weight=2)
    G.add_edge("K38", "11.E", weight=1)
    G.add_edge("11.E", "E7", weight=1)





    # F ---
    G.add_edge("K52", "10.F", weight=1)
    G.add_edge("K53", "10.F", weight=36)
    G.add_edge("10.F", "11.F", weight=1)
    G.add_edge("K35", "11.F", weight=2)
    G.add_edge("K36", "11.F", weight=1)
    G.add_edge("11.F", "E4", weight=1)


    # G
    G.add_edge("K39", "13.G", weight=1)
    G.add_edge("13.G", "12.G", weight=1)
    G.add_edge("12.G", "8.G", weight=1)
    G.add_edge("8.G", "7.G", weight=1)
    G.add_edge("7.G", "9.G", weight=1)
    G.add_edge("9.G", "E10", weight=1)

    # H
    G.add_edge("7.H", "15.H", weight=1)
    G.add_edge("K21", "15.H", weight=1)
    G.add_edge("K24", "15.H", weight=1)
    G.add_edge("K27", "15.H", weight=1)
    G.add_edge("15.H", "E26", weight=1)

    # w
    G.add_edge("K24", "1.w", weight=2)
    G.add_edge("K24", "1.w", weight=2)
    G.add_edge("K25", "1.w", weight=2)
    G.add_edge("K26", "1.w", weight=2)
    G.add_edge("E13", "1.w", weight=1)
    G.add_edge("E18", "1.w", weight=1)
    G.add_edge("E7", "1.w", weight=1)
    G.add_edge("1.w", "E49", weight=1)

    # x
    G.add_edge("E49", "2.x", weight=1)
    G.add_edge("E4", "2.x", weight=1)
    G.add_edge("E10", "2.x", weight=1)
    G.add_edge("K24", "2.x", weight=2)
    G.add_edge("K25", "2.x", weight=2)
    G.add_edge("2.x", "E50", weight=1)

    # z ---
    G.add_edge("E17", "3.y", weight=1)
    G.add_edge("E16", "3.y", weight=1)
    G.add_edge("E50", "3.y", weight=1)
    G.add_edge("K24", "3.y", weight=1)
    G.add_edge("K27", "3.y", weight=1)
    G.add_edge("3.y", "E51", weight=1)

    return G