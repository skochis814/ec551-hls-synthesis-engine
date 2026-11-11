`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/10/2026 11:03:56 PM
// Design Name: 
// Module Name: testbench
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


module testbench(

    );
    
    reg clk = 0;
    reg reset = 0;
    reg [14:0] select;
    reg [1:0] P;
    reg [1:0] Q;
    reg [1:0] R;
    reg [1:0] S;
    reg [1:0] T;
    reg [1:0] U;
    wire [31:0] A;
    wire [31:0] B;
    wire [31:0] C;
    wire [31:0] D;
    wire [31:0] E;
    wire [31:0] F;
    wire [31:0] X;
    wire [31:0] observe;
    
    top dut (
        .clk(clk),
        .reset(reset),
        .select(select),
        .P(P),
        .Q(Q),
        .R(R),
        .S(S),
        .T(T),
        .U(U),
        .observe(observe),
        .X(X)
    );
    
    always #5 clk = ~clk;
    
    initial begin
        P = 1;
        Q = 2;
        R = 1;
        S = 2;
        T = 2;
        U = 3;
        
        reset = 1;
        #11;
        reset = 0;
        
        #10000;
        
        $finish;
     end
endmodule
