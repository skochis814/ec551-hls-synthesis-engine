
""" schedule = {
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
} """

def generate_sequencer(schedule):
    num_states = len(schedule["cycles"]) + 2
    state_width = (num_states - 1).bit_length()

    lines = []
    lines.append("module sequencer(")
    lines.append("  input clk,")
    lines.append("  input reset,")
    lines.append("  output reg load,")
    lines.append(f"  output reg [{state_width - 1}:0] state")
    lines.append(");")


    lines.append(f"  localparam IDLE = {state_width}'b{0:0{state_width}b};")
    lines.append(f"  localparam LOAD = {state_width}'b{1:0{state_width}b};")

    cycle_num = len(schedule["cycles"])

    state_number = 2
    for state_count in range(cycle_num):
        state_bin = f"{state_width}'b{state_number + state_count:0{state_width}b}"
        lines.append(f"  localparam S{state_count} = {state_bin};")

    lines.append("")
    lines.append(f"  reg [{state_width - 1}:0] next_state;")
    lines.append("")

    lines.append("  always@(posedge clk) begin")
    lines.append("      if (reset) begin")
    lines.append("          state <= IDLE;")
    lines.append("      end")
    lines.append("      else begin")
    lines.append("          state <= next_state;")
    lines.append("      end")
    lines.append("  end")
    lines.append("")

    lines.append("  always@(*) begin")
    lines.append("      next_state = state;")
    lines.append("      load = 0;")
    lines.append("      case (state)")
    lines.append("          IDLE: next_state = LOAD;")
    lines.append("          LOAD: begin")
    lines.append("              next_state = S0;")
    lines.append("              load = 1'b1;")
    lines.append("          end")

    if cycle_num > 1:
        for state_count in range(cycle_num - 1):
            lines.append(f"          S{state_count}: next_state = S{state_count + 1};")

    lines.append(f"          S{cycle_num - 1}: next_state = IDLE;")

    lines.append("      endcase")
    lines.append("  end")
    lines.append("endmodule")

    with open("sequencer.v", "w") as file:
        file.write("\n".join(lines))

#generate_sequencer(schedule)