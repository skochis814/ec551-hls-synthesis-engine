from python.parse_input import parse_file, gen_ssa


def print_equations(equations):
    symbols = {"add": "+", "sub": "-", "mul": "*"}
    for i, eq in enumerate(equations, start=1):
        op = symbols[eq["op"]]
        print(f"{i:2}. {eq['dest']} = {eq['lhs']} {op} {eq['rhs']}")


equations = parse_file("equations.txt")

print("Parsed equations")
print_equations(equations)

print("\nSSA equations")
print_equations(gen_ssa(equations))