# EC551 HLS Synthesis Engine

The Python front end reads arithmetic equations, converts them to static single assignment (SSA) form, and builds a dependency graph. The scheduler uses that graph to assign operations to clock cycles and arithmetic units. The resulting schedule is passed to the Verilog generators.

## Running the scheduler

From the repository root, run:

```sh
python main.py
```

The program reads `equations.txt` and prints the schedule for the mode selected in `main.py`. The default is `optimized_constrained_asap` with one adder and one multiplier. Edit `mode` and `constraints` in `main.py` to change the scheduler or unit limits. Constraint keys are `add`, `sub`, and `mul`. Use positive counts for limited unit types and omit a type to leave it unlimited.

To also write the SSA equations to `ssa.txt`, run:

```sh
python main.py --export-ssa
```

## Input and dependencies

Write one equation per line using two variable operands and one operator (`+`, `-`, or `*`). For example:

```text
X = A + B
X = X * C
```

The SSA pass converts this to:

```text
X_1 = A_0 + B_0
X_2 = X_1 * C_0
```

Version `_0` identifies an external input. Each assignment creates a new version of its destination. The dependency graph uses each operation’s destination as its ID, so the multiply above depends on the operation that produces `X_1`.

## Scheduling modes

| Mode | Placement rule |
| --- | --- |
| `asap` | Place each operation in the earliest cycle allowed by its dependencies. |
| `constrained_asap` | Place each operation in the earliest cycle allowed by its dependencies and the unit limits. |
| `alap` | Work backward from the last cycle to place each operation as late as its consumers allow. |
| `constrained_alap` | Schedule backward while enforcing the unit limits. |
| `optimized_constrained_asap` | Build one cycle at a time. When ready operations compete for a unit, prioritize the operation with the earliest unconstrained ALAP position, which has a longer chain of dependent work ahead of it. |

On the bundled input, constrained ASAP takes **13 cycles** and optimized constrained ASAP takes **7 cycles** with the same unit limits. The optimized mode starts the multiplication chain earlier, then runs the independent additions alongside the multiplications.

## Schedule format

`scheduler(mode, dag, constraints)` returns a dictionary with three fields.

- `inputs` maps external variable names to their `_0` SSA names.
- `outputs` maps each assigned variable name to its final SSA version.
- `cycles` contains one list per clock cycle. Each operation includes `dest`, `lhs`, `rhs`, `op`, and `unit`. Unit IDs start at `0` for each operation type and can be reused across cycles.

## Verilog Generation

The Verilog generators convert the scheduler's output into synthesizable hardware. 

## FPGA Demonstration

The generated design can be demonstrated using a separate `wrapper.v` module. The wrapper connects the generated hardware to the board's peripherals.

| FPGA Interface | Function |
| --- | --- |
| SW0-SW7 | Provides up to four primary input 2-bit values to be selected |
| SW8-SW15 | Selects which arithmetic unit's output is displayed (switch to functional unit mappings are printed) |
| Center Button | Resets the sequencer |
| Up Button | The "clock signal" |

## Testbench Simulation

A simple testbench can be written in the format shown in `testbench.v` to verify the system functionality before board deployment. The testbench tests a random input combination. To ensure proper functionality, add the internal registers storing the results from each computation from the instantiation of `datapath.v` to the wave window. Compare when these values are stored to the cycle number from the schedule to verify that the schedule was implemented in Verilog correctly, as well as the final output values.

## Front-end files

| File | Purpose |
| --- | --- |
| `main.py` | Reads the input, runs the selected scheduler, and prints the schedule. |
| `python/parse_input.py` | Parses equations, converts them to SSA, and builds the dependency graph. |
| `python/export_ssa.py` | Writes the SSA equations to `ssa.txt` on request. |
| `python/scheduler.py` | Implements the five scheduling modes and prepares the schedule for Verilog generation. |
| `python/datapath_generate.py` | Automatically generates a Mux and Register based Verilog module  reflecting the chosen schedule, instantiating functional units as well |
| `python/sequence_generate.py` | Automatically generates an FSM control Verilog module to manage Mux selects and register write-enables |
| `python/top_module_generate.py` | Instantiates both the generated datapath and control modules into a top level module |

## Complementary Verilog Files
| File | Purpose |
| --- | --- |
| `verilog/add.v` | Basic adder module |
| `verilog/sub.v` | Basic subtractor module |
| `verilog/add.v` | Basic multiplier module |
| `verilog/binary_to_bcd.v` | Converts the 32-bit outputs from the internal registers to BCD for display |
| `verilog/seven_segment.v` | Drives the seven segment display on the FPGA |
| `verilog/debouncer.v` | Used to debounce buttons for clock cycle advancing |
| `verilog/wrapper.v` | Connects the generated modules to the board's peripherals for demo |
| `verilog/testbench.v` | Simulation used to verify schedule was correctly implemented in Verilog |
