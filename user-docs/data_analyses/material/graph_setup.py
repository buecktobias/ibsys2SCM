from production_graph import MaterialProductionFlowGraph


def create_graph():
    flow = MaterialProductionFlowGraph()

    def _add_process(id, pd, sd):
        flow.add_process(id, pd, sd)

    def _add_edge(source_id, target_id, weight):
        flow.add_edge(source_id, target_id, weight)

    _add_process("15.A", 3, 15)

    _add_process("6.B", 2, 15)
    _add_process("14.B", 3, 0)

    _add_process("13.C", 2, 0)
    _add_process("12.C", 3, 0)
    _add_process("8.C", 1, 15)
    _add_process("7.C", 2, 20)
    _add_process("9.C", 3, 15)

    _add_process("6.D", 3, 15)
    _add_process("7.D", 2, 20)
    _add_process("8.D", 1, 15)
    _add_process("9.D", 3, 15)

    _add_process("10.E", 4, 20)
    _add_process("11.E", 3, 20)

    _add_process("10.F", 4, 20)
    _add_process("11.F", 3, 10)

    _add_process("13.G", 2, 0)
    _add_process("12.G", 3, 0)
    _add_process("8.G", 1, 15)
    _add_process("7.G", 2, 20)
    _add_process("9.G", 3, 15)

    _add_process("7.H", 2, 30)
    _add_process("15.H", 3, 15)

    _add_process("1.w", 6, 20)
    _add_process("2.x", 5, 30)
    _add_process("4.z", 6, 30)
    _add_process("3.y", 5, 20)

    _add_edge("K43", "15.A", 1)
    _add_edge("K44", "15.A", 1)
    _add_edge("K45", "15.A", 1)
    _add_edge("K46", "15.A", 1)
    _add_edge("15.A", "E17", 1)

    _add_edge("K28", "6.B", 1)
    _add_edge("6.B", "14.B", 1)
    _add_edge("K24", "14.B", 1)
    _add_edge("K40", "14.B", 1)
    _add_edge("K41", "14.B", 1)
    _add_edge("K42", "14.B", 2)
    _add_edge("14.B", "E16", 1)

    _add_edge("K39", "13.C", 1)
    _add_edge("13.C", "12.C", 1)
    _add_edge("12.C", "8.C", 1)
    _add_edge("8.C", "7.C", 1)
    _add_edge("K32", "7.C", 1)
    _add_edge("7.C", "9.C", 1)
    _add_edge("9.C", "E13", 1)

    _add_edge("K28", "6.D", 3)
    _add_edge("6.D", "8.D", 1)
    _add_edge("K59", "8.D", 3)
    _add_edge("8.D", "7.D", 1)
    _add_edge("K32", "7.D", 2)
    _add_edge("7.D", "9.D", 1)
    _add_edge("9.D", "E18", 1)

    _add_edge("K52", "10.E", 1)
    _add_edge("K53", "10.E", 36)
    _add_edge("10.E", "11.E", 1)
    _add_edge("K35", "11.E", 1)
    _add_edge("K37", "11.E", 2)
    _add_edge("K38", "11.E", 1)
    _add_edge("11.E", "E7", 1)

    _add_edge("K52", "10.F", 1)
    _add_edge("K53", "10.F", 36)
    _add_edge("10.F", "11.F", 1)
    _add_edge("K35", "11.F", 2)
    _add_edge("K36", "11.F", 1)
    _add_edge("11.F", "E4", 1)

    _add_edge("K39", "13.G", 1)
    _add_edge("13.G", "12.G", 1)
    _add_edge("12.G", "8.G", 1)
    _add_edge("8.G", "7.G", 1)
    _add_edge("7.G", "9.G", 1)
    _add_edge("9.G", "E10", 1)

    _add_edge("7.H", "15.H", 1)
    _add_edge("K21", "15.H", 1)
    _add_edge("K24", "15.H", 1)
    _add_edge("K27", "15.H", 1)
    _add_edge("15.H", "E26", 1)

    _add_edge("K24", "1.w", 2)
    _add_edge("K24", "1.w", 2)
    _add_edge("K25", "1.w", 2)
    _add_edge("K26", "1.w", 2)
    _add_edge("E13", "1.w", 1)
    _add_edge("E18", "1.w", 1)
    _add_edge("E7", "1.w", 1)
    _add_edge("1.w", "E49", 1)

    _add_edge("E49", "2.x", 1)
    _add_edge("E4", "2.x", 1)
    _add_edge("E10", "2.x", 1)
    _add_edge("K24", "2.x", 2)
    _add_edge("K25", "2.x", 2)
    _add_edge("2.x", "E50", 1)

    _add_edge("E17", "3.y", 1)
    _add_edge("E16", "3.y", 1)
    _add_edge("E50", "3.y", 1)
    _add_edge("K24", "3.y", 1)
    _add_edge("K27", "3.y", 1)
    _add_edge("3.y", "E51", 1)

    _add_edge("4.z", "EP", 1)
    _add_edge("E26", "4.z", 1)
    _add_edge("E51", "4.z", 1)
    _add_edge("K21", "4.z", 1)
    _add_edge("K24", "4.z", 1)
    _add_edge("K27", "4.z", 1)

    return flow
