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