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

def optimized_constrained_asap(dag, constraints):
    alap_schedule = alap(dag)
    schedule = {}
    schedule["cycles"] = [[]]

    alap_pos = {}
    for cycle_num, cycle in enumerate(alap_schedule["cycles"]):
        for eq in cycle:
            alap_pos[eq["dest"]] = cycle_num
    
    placed = 0
    cycle_num = 0

    while placed < len(dag):
        if len(schedule["cycles"]) == cycle_num:
            schedule["cycles"].append([])
        
        deps_done = []
        for cycle in schedule["cycles"]:
            for eq in cycle:
                deps_done.append(eq["dest"])

        cycle_nodes = []
        for node in dag.values():
            done = True
            for dep in node["deps"]:
                if dep not in deps_done:
                    done = False
            if done and node["dest"] not in deps_done:
                cycle_nodes.append(node["dest"])

        cycle_nodes.sort(key=alap_pos.get)

        used = {"add": 0, "sub": 0, "mul": 0}
        for dest in cycle_nodes:
            node = dag[dest]
            if constraints.get(node["op"]) is None or used[node["op"]] < constraints[node["op"]]:
                schedule["cycles"][cycle_num].append(node)

                placed = placed + 1
                used[node["op"]] = used[node["op"]] + 1
        
        cycle_num = cycle_num + 1
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
    elif mode == "optimized_constrained_asap":
        schedule = optimized_constrained_asap(dag, constraints)
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