

def asap(dag):
    schedule = {}
    schedule["cycles"] = [[]]

    for node in dag.values():
        if not node["deps"]:
            schedule["cycles"][0].append(node)
            continue

        cycle_num = -1  
        for i, cycle in enumerate(schedule["cycles"]):
            if any(eq["dest"] in node["deps"] for eq in cycle) and i > cycle_num:
                cycle_num = i
        cycle_num = cycle_num + 1
        
        if len(schedule["cycles"]) == cycle_num:
            schedule["cycles"].append([])
        schedule["cycles"][cycle_num].append(node)
    return schedule