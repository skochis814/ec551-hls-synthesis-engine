


#ill have the schedules stored in a dict formatted as shown below 
# the [] containing {} are one cycle each, and unit refers to like adder0 or multiplier0, to track if we gotta reuse or create additional
schedule = {
    "inputs": {"A": "A_0", "B": "B_0"},
    "outputs": {"X": "X_2", "Y": "Y_1"},
    "cycles": [
        [  # Cycle 0: X = A + B and Y = A * B
            {"op": "add", "unit": 0, "lhs": "A_0", "rhs": "B_0", "dest": "X_1"},
            {"op": "mul", "unit": 0, "lhs": "A_0", "rhs": "B_0", "dest": "Y_1"},
        ],
        [  # Cycle 1: X = X + Y
            {"op": "add", "unit": 0, "lhs": "X_1", "rhs": "Y_1", "dest": "X_2"},
        ],
    ],
}


def generate_datapath(schedule):
    lines = []

    hardware = {"add": 0, "sub": 0, "mul": 0}
    registers = []
    for cycle in schedule["cycles"]:
        for equation in cycle:
            hardware[equation["op"]] = max(hardware[equation["op"]], equation["unit"] + 1)
            registers.append(equation["dest"])

    inputs = []
    for input in schedule["inputs"]:
        inputs.append(input)

    outputs = []
    for output in schedule["outputs"]:
        outputs.append(output)

    num_states = len(schedule["cycles"]) + 2
    state_width = (num_states - 1).bit_length()
    
    lines.append("module datapath(")
    lines.append("  input clk,")
    lines.append("  input reset,")
    lines.append("  input load,")
    lines.append(f"  input [{state_width - 1}:0] state,")
    for input in inputs:
        lines.append(f"  input [1:0] {input},")
    lines.append(",\n".join(f"  output [31:0] {output}" for output in outputs))
    lines.append(");")
    lines.append("")

    lines.append(f"  localparam IDLE = {state_width}'b{0:0{state_width}b};")
    lines.append(f"  localparam LOAD = {state_width}'b{1:0{state_width}b};")
    
    cycle_num = len(schedule["cycles"])
    
    state_number = 2
    for state_count in range(cycle_num):
        state_bin = f"{state_width}'b{state_number + state_count:0{state_width}b}"
        lines.append(f"  localparam S{state_count} = {state_bin};")

    for input in inputs:
        lines.append(f"  reg [1:0] {input}_reg;")

    for register in registers:
        lines.append(f"  reg [31:0] {register};")
    lines.append("")

    lines.append("  always @(posedge clk) begin")
    lines.append("      if (load) begin")
    for input in inputs:
        lines.append(f"          {input}_reg <= {input};")
    lines.append("      end")
    lines.append("  end")
    lines.append("")

    for op, count in hardware.items():
        for unit in range(count):
            lines.append(f"  wire [31:0] {op}{unit}_lhs;")
            lines.append(f"  wire [31:0] {op}{unit}_rhs;")
            lines.append(f"  wire [31:0] {op}{unit}_out;")
            lines.append("")

    for op, count in hardware.items():
        for unit in range(count):
            lines.append(f" {op} {op}{unit}(")
            lines.append(f"     .a({op}{unit}_lhs),")
            lines.append(f"     .b({op}{unit}_rhs),")
            lines.append(f"     .out({op}{unit}_out)")
            lines.append("  );")
            lines.append("")


    unit_inputs = {}
    for cycle in schedule["cycles"]:
        for equation in cycle:
            key = f"{equation["op"]}{equation["unit"]}"
            if key not in unit_inputs:
                unit_inputs[key] = {"lhs": [], "rhs": []}

            if equation["lhs"] not in unit_inputs[key]["lhs"]:
                unit_inputs[key]["lhs"].append(equation["lhs"])
            if equation["rhs"] not in unit_inputs[key]["rhs"]:
                unit_inputs[key]["rhs"].append(equation["rhs"])

    # Create muxes by looping through each functional unit
    for unit in unit_inputs:

        # parameter is lhs or rhs
        for parameter in unit_inputs[unit]:

            # check if there is only one input assignment
            if len(unit_inputs[unit][parameter]) == 1:
                source = unit_inputs[unit][parameter][0]

                # check if the input is a primary input
                if source in schedule["inputs"].values():
                    source = source.split("_")[0] + "_reg"

                lines.append(f"  assign {unit}_{parameter} = {source};")

            # we need a mux
            else:
                lines.append(f" assign {unit}_{parameter} = ")
                for cycle_num, cycle in enumerate(schedule["cycles"]):
                    for equation in cycle:
                        key = f"{equation["op"]}{equation["unit"]}"

                        # check if the current equation we are looking at contains the unit
                        if key == unit:
                            source = equation[parameter]
                            if source in schedule["inputs"].values():
                                source = source.split("_")[0] + "_reg"

                            lines.append(f"     (state == S{cycle_num}) ? {source} :")

                lines.append(f"             0;")
                lines.append("")

    lines.append("")
    lines.append("  always @(posedge clk) begin")
    for cycle_num, cycle in enumerate(schedule["cycles"]):
        lines.append(f"     if (state == S{cycle_num}) begin")
        for equation in cycle:
            lines.append(f"         {equation["dest"]} <= {equation["op"]}{equation["unit"]}_out;")
        lines.append(f"     end")
    lines.append("  end")
    lines.append("")

    for output in schedule["outputs"]:
        lines.append(f" assign {output} = {schedule["outputs"][output]};")

    lines.append("")
    lines.append("endmodule")

    with open("datapath.v", "w") as file:
        file.write("\n".join(lines))

generate_datapath(schedule)