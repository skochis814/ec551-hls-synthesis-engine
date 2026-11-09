def export_ssa(ssa):
    symbols = {"add": "+", "sub": "-", "mul": "*"}

    with open("ssa.txt", "w", encoding="utf-8") as file:
        for eq in ssa:
            op = symbols[eq["op"]]
            file.write(f"{eq['dest']} = {eq['lhs']} {op} {eq['rhs']}\n")