from python.parse_input import parse_file, gen_ssa
from python.export_ssa import export_ssa
import sys


def print_equations(equations):
    symbols = {"add": "+", "sub": "-", "mul": "*"}
    for eq in equations:
        op = symbols[eq["op"]]
        print(f"{eq['dest']} = {eq['lhs']} {op} {eq['rhs']}")


equations = parse_file("equations.txt")
ssa = gen_ssa(equations)
if "--export-ssa" in sys.argv:
    export_ssa(ssa)

print("Parsed equations")
print_equations(equations)

print("\nSSA equations")
print_equations(ssa)
