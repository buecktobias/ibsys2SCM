from production_graph import MaterialProductionFlowGraph

def create_graph_p3():
    flow = MaterialProductionFlowGraph()

    def _add_process(id, pd, sd):
        flow.add_process(id, pd, sd)

    def _add_edge(source_id, target_id, weight=1):
        flow.add_edge(source_id, target_id, weight)

    flow.add_produced("E3")

    # region A
    _add_process("15.A", 3, 15)

    # region B
    _add_process("6.B", 2, 15)
    _add_process("14.B", 3, 0)

    # region C
    _add_process("13.C", 2, 0)
    _add_process("12.C", 3, 0)
    _add_process("8.C", 2, 15)
    _add_process("7.C", 2, 20)
    _add_process("9.C", 3, 15)

    # region D
    _add_process("6.D", 3, 15)
    _add_process("7.D", 2, 20)
    _add_process("8.D", 3, 20)
    _add_process("9.D", 2, 15)

    # region E
    _add_process("10.E", 4, 20)
    _add_process("11.E", 3, 20)

    # region F
    _add_process("10.F", 4, 20)
    _add_process("11.F", 3, 20)

    # region G
    _add_process("13.G", 2, 0)
    _add_process("12.G", 3, 0)
    _add_process("8.G", 2, 15)
    _add_process("7.G", 2, 20)
    _add_process("9.G", 3, 15)

    # region H
    _add_process("7.H", 2, 30)
    _add_process("15.H", 3, 15)

    # Other processes
    _add_process("1.w", 6, 20)
    _add_process("2.x", 5, 20)
    _add_process("3.y", 6, 20)
    _add_process("4.z", 7, 30)

    # Now all the edges
    #A
    _add_edge("K43", "15.A")
    _add_edge("K44", "15.A")
    _add_edge("K45", "15.A")
    _add_edge("K46", "15.A")
    _add_edge("15.A", "E17")

    # B
    _add_edge("K28", "6.B")
    _add_edge("6.B", "14.B")
    _add_edge("K24", "14.B")
    _add_edge("K40", "14.B")
    _add_edge("K41", "14.B")
    _add_edge("K42", "14.B", 2)
    _add_edge("14.B", "E16")

    # C
    _add_edge("K39", "13.C")
    _add_edge("13.C", "12.C")
    _add_edge("12.C", "8.C")
    _add_edge("8.C", "7.C")
    _add_edge("K32", "9.C")
    _add_edge("7.C", "9.C")
    _add_edge("9.C", "E15")

    # D
    _add_edge("K28", "6.D", 5)
    _add_edge("6.D", "8.D")
    _add_edge("8.D", "7.D")
    _add_edge("K59", "7.D", 2)
    _add_edge("K32", "9.D")
    _add_edge("7.D", "9.D")
    _add_edge("9.D", "E20")

    # E
    _add_edge("K33", "10.E")
    _add_edge("K34", "10.E", 36)
    _add_edge("10.E", "11.E")
    _add_edge("K35", "11.E", 2)
    _add_edge("K37", "11.E")
    _add_edge("K38", "11.E")
    _add_edge("11.E", "E9")

    # F
    _add_edge("K33", "10.F")
    _add_edge("K34", "10.F", 36)
    _add_edge("10.F", "11.F")
    _add_edge("K35", "11.F", 2)
    _add_edge("K36", "11.F")
    _add_edge("11.F", "E6")

    # G
    _add_edge("K39", "13.G")
    _add_edge("13.G", "12.G")
    _add_edge("12.G", "8.G")
    _add_edge("8.G", "7.G")
    _add_edge("7.G", "9.G")
    _add_edge("K32", "9.G")
    _add_edge("9.G", "E12")

    # H
    _add_edge("K44", "7.H", 2)
    _add_edge("K48", "7.H", 2)
    _add_edge("7.H", "15.H")
    _add_edge("K47", "15.H")
    _add_edge("15.H", "E26")

    # w
    _add_edge("K24", "1.w", 2)
    _add_edge("K25", "1.w", 2)
    _add_edge("E15", "1.w")
    _add_edge("E20", "1.w")
    _add_edge("E9", "1.w")
    _add_edge("1.w", "E29")

    # x
    _add_edge("E29", "2.x")
    _add_edge("E6", "2.x")
    _add_edge("E12", "2.x")
    _add_edge("K24", "2.x", 2)
    _add_edge("K25", "2.x", 2)
    _add_edge("2.x", "E30")

    # y
    _add_edge("E17", "3.y")
    _add_edge("E16", "3.y")
    _add_edge("E30", "3.y")
    _add_edge("K24", "3.y")
    _add_edge("K27", "3.y")
    _add_edge("3.y", "E31")

    # z
    _add_edge("E31", "4.z")
    _add_edge("E26", "4.z")
    _add_edge("K23", "4.z")
    _add_edge("K24", "4.z")
    _add_edge("K27", "4.z")
    _add_edge("4.z", "E3")

    return flow
