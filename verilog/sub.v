`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/09/2026 03:26:48 PM
// Design Name: 
// Module Name: sub
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


module sub(
    input [31:0] a,
    input [31:0] b,
    output [31:0] out
    );
    
    assign out = a - b;
    
endmodule
