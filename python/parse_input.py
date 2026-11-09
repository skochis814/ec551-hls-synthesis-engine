def parse_file(input_path):
    equations = []
    operators = {"+": "add", "-": "sub", "*": "mul"}
    with open(input_path) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            line = "".join(line.split())

            dest, args = line.split("=")
            for char in args:
                if char in "+-*":
                    op = char
                    break
            lhs, rhs = args.split(op)

            equation = {
                "dest": dest,
                "lhs": lhs,
                "op": operators[op],
                "rhs": rhs
            }

            equations.append(equation)
    return equations

#this form of SSA has intermediate outputs immediately start at _1 even if 
#they have not been used as an input prior, to simplify implementation
def gen_ssa(equations):
    ssa_eqs = []
    sym_count = {}
    for eq in equations:
        dest = eq["dest"]
        lhs = eq["lhs"]
        rhs = eq["rhs"]

        if dest not in sym_count:
            sym_count[dest] = 0
        if lhs not in sym_count:
            sym_count[lhs] = 0
        if rhs not in sym_count:
            sym_count[rhs] = 0

        ssa_lhs = lhs + "_" + str(sym_count[lhs])
        ssa_rhs = rhs + "_" + str(sym_count[rhs])

        sym_count[dest] = sym_count[dest] + 1
        ssa_dest = dest + "_" + str(sym_count[dest])

        ssa = {
            "dest": ssa_dest,
            "lhs": ssa_lhs,
            "op": eq["op"],
            "rhs": ssa_rhs
        }

        ssa_eqs.append(ssa)
    return ssa_eqs

def gen_dag(ssa):
    dag = {}
    for eq in ssa:
        dest = eq["dest"]
        lhs = eq["lhs"]
        rhs = eq["rhs"]

        deps = []

        if not lhs.endswith("_0"):
            deps.append(lhs)
        if not rhs.endswith("_0") and rhs != lhs:
            deps.append(rhs)

        node = eq.copy()
        node["deps"] = deps

        dag[dest] = node
    return dag
            