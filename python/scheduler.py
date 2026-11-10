def asap(dag):
    schedule = {}
    schedule["cycles"] = [[]]

    for node in dag.values():
        cycle_num = -1  
        for i, cycle in enumerate(schedule["cycles"]):
            if any(eq["dest"] in node["deps"] for eq in cycle) and i > cycle_num:
                cycle_num = i
        cycle_num = cycle_num + 1
        
        if len(schedule["cycles"]) == cycle_num:
            schedule["cycles"].append([])
        schedule["cycles"][cycle_num].append(node)

    return schedule

def constrained_asap(dag, constraints):
    schedule = {}
    schedule["cycles"] = [[]]

    for node in dag.values():
        cycle_num = -1  
        for i, cycle in enumerate(schedule["cycles"]):
            if any(eq["dest"] in node["deps"] for eq in cycle) and i > cycle_num:
                cycle_num = i
        cycle_num = cycle_num + 1

        while cycle_num < len(schedule["cycles"]) and constraints.get(node["op"]) is not None:
            if sum(1 for eq in schedule["cycles"][cycle_num] if eq["op"] == node["op"]) < constraints[node["op"]]:
                break
            cycle_num = cycle_num + 1

        if len(schedule["cycles"]) == cycle_num:
            schedule["cycles"].append([])

        schedule["cycles"][cycle_num].append(node)

    return schedule

def alap(dag):
    schedule = {}
    schedule["cycles"] = [[]]

    for node in reversed(dag.values()):
        cycle_num = -1
        for i, cycle in enumerate(schedule["cycles"]):
            if any(node["dest"] in eq["deps"] for eq in cycle) and i > cycle_num:
                cycle_num = i
        cycle_num = cycle_num + 1

        if len(schedule["cycles"]) == cycle_num:
            schedule["cycles"].append([])

        schedule["cycles"][cycle_num].append(node)

    schedule["cycles"].reverse()
    return schedule

def constrained_alap(dag, constraints):
    schedule = {}
    schedule["cycles"] = [[]]

    for node in reversed(dag.values()):
        cycle_num = -1
        for i, cycle in enumerate(schedule["cycles"]):
            if any(node["dest"] in eq["deps"] for eq in cycle) and i > cycle_num:
                cycle_num = i
        cycle_num = cycle_num + 1

        while cycle_num < len(schedule["cycles"]) and constraints.get(node["op"]) is not None:
            if sum(1 for eq in schedule["cycles"][cycle_num] if eq["op"] == node["op"]) < constraints[node["op"]]:
                break
            cycle_num = cycle_num + 1

        if len(schedule["cycles"]) == cycle_num:
            schedule["cycles"].append([])

        schedule["cycles"][cycle_num].append(node)

    schedule["cycles"].reverse()
    return schedule

def scheduler(mode, dag, constraints=None):
    if constraints is None:
        constraints = {}

    if mode == "asap":
        schedule = asap(dag)
    elif mode == "constrained_asap":
        schedule = constrained_asap(dag, constraints)
    elif mode == "alap":
        schedule = alap(dag)
    elif mode == "constrained_alap":
        schedule = constrained_alap(dag, constraints)
    else:
        return None

    schedule["inputs"] = {}
    schedule["outputs"] = {}

    for node in dag.values():
        lhs = node["lhs"]
        rhs = node["rhs"]
        dest = node["dest"]

        for operand in (lhs, rhs):
            name, version = operand.rsplit("_", 1)
            if version == "0":
                schedule["inputs"][name] = operand

        name, version = dest.rsplit("_", 1)
        schedule["outputs"][name] = dest

    for cycle in schedule["cycles"]:
        unit_count = {"add": 0, "sub": 0, "mul": 0}

        for i, node in enumerate(cycle):
            op = node["op"]
            equation = node.copy()
            del equation["deps"]

            equation["unit"] = unit_count[op]
            unit_count[op] = unit_count[op] + 1

            cycle[i] = equation

    return schedule