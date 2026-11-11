`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/10/2026 05:18:30 PM
// Design Name: 
// Module Name: binary_to_bcd
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



module binary_to_bcd(
    input wire [31:0] binary,
    output reg [31:0] bcd
);

    reg [39:0] digits;
    integer i;
    integer j;

    always @(*) begin
        digits = 40'd0;

        for (i = 31; i >= 0; i = i - 1) begin
            for (j = 0; j < 10; j = j + 1) begin
                if (digits[j*4 +: 4] >= 5)
                    digits[j*4 +: 4] =
                        digits[j*4 +: 4] + 4'd3;
            end

            digits = {digits[38:0], binary[i]};
        end

        bcd = digits[31:0];
    end


endmodule

