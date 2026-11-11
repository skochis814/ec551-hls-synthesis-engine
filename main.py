import sys

from python.parse_input import parse_file, gen_ssa, gen_dag
from python.export_ssa import export_ssa
from python.scheduler import scheduler
from python.datapath_generate import generate_datapath
from python.sequencer_generate import generate_sequencer
from python.top_module_generate import generate_top


input_path = "equations.txt"
mode = "optimized_constrained_asap"
constraints = {"add": 2, "mul": 1}

equations = parse_file(input_path)
ssa = gen_ssa(equations)

if "--export-ssa" in sys.argv:
    export_ssa(ssa)

dag = gen_dag(ssa)
schedule = scheduler(mode, dag, constraints)

symbols = {"add": "+", "sub": "-", "mul": "*"}

print(f"\n{mode}")
for cycle_num, cycle in enumerate(schedule["cycles"]):
    print(f"Cycle {cycle_num}")
    for eq in cycle:
        op = symbols[eq["op"]]
        print(f"  {eq['dest']} = {eq['lhs']} {op} {eq['rhs']}")

print("\n")
print("Functional Unit Switches:")
generate_datapath(schedule)
generate_sequencer(schedule)
generate_top(schedule)