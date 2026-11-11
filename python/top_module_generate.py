

def generate_top(schedule):
    num_states = len(schedule["cycles"]) + 2
    state_width = (num_states - 1).bit_length()

    lines = []
    lines.append("module top(")
    lines.append("  input clk,")
    lines.append("  input step,")
    lines.append("  input reset,")
    lines.append("  input [14:0] select,")

    for input in schedule["inputs"]:
        lines.append(f"  input [1:0] {input},")

    lines.append("  output [31:0] observe,")

    outputs = []
    for output in schedule["outputs"]:
        outputs.append(output)
    lines.append(",\n".join(f"  output [31:0] {output}" for output in outputs))
    lines.append(");")
    lines.append("")

    lines.append("  wire load;")
    lines.append(f"  wire [{state_width - 1}:0] state;")
    lines.append("")

    lines.append("  sequencer dut1(")
    lines.append("      .clk(clk),")
    lines.append("      .step(step),")
    lines.append("      .reset(reset),")
    lines.append("      .load(load),")
    lines.append("      .state(state)")
    lines.append("  );")
    lines.append("")



    lines.append("  datapath dut2(")
    lines.append("      .clk(clk),")
    lines.append("      .step(step),")
    lines.append("      .load(load),")
    lines.append("      .select(select),")
    lines.append("      .state(state),")

    for input in schedule["inputs"]:
        lines.append(f"      .{input}({input}),")

    lines.append("      .observe(observe),")
    lines.append(",\n".join(f"      .{output}({output})" for output in outputs))
    lines.append("  );")
    lines.append("")
    lines.append("endmodule")

    with open("top.v", "w") as file:
        file.write("\n".join(lines))