`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/10/2026 08:29:11 PM
// Design Name: 
// Module Name: wrapper
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module wrapper(
    input clk_100MHz,
    input reset,
    input clk_step,
    input [15:0] sw,
    output [6:0] seg,
    output [7:0] an,
    output dp
);

    wire step_pulse;
    wire [31:0] observe;
    wire [39:0] bcd;

    
    wire [31:0] X, Y;
    //wire [31:0] Z, W;   // other outputs to be added

    debouncer step_button(
        .clk(clk_100MHz),
        .button(clk_step),
        .pulse(step_pulse)
    );

    top dut(
        .clk(clk_100MHz),
        .step(step_pulse),
        .reset(reset),
        .select({7'b0, sw[15:8]}),
        .A(sw[1:0]),
        .B(sw[3:2]),
        // .C(sw[5:4]),
        // .D(sw[7:6]),
        .observe(observe),
        .X(X),
        .Y(Y)
        // .Z(Z),
        // .W(W)
    );

    binary_to_bcd converter(
        .binary(observe),
        .bcd(bcd)
    );

    seven_segment display(
        .clk(clk_100MHz),
        .reset(reset),
        .bcd(bcd),
        .seg(seg),
        .an(an),
        .dp(dp)
    );

endmodule

