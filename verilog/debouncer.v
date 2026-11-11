`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/10/2026 05:39:04 PM
// Design Name: 
// Module Name: debouncer
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



module debouncer #(
    parameter DEBOUNCE_COUNT = 1_000_000
)(
    input wire clk,
    input wire button,
    output reg debounced = 0,
    output wire pulse
);

    reg sync1 = 0;
    reg sync2 = 0;
    reg [19:0] counter = 0;
    reg debounced_d = 0;

    
    always @(posedge clk) begin
        sync1 <= button;
        sync2 <= sync1;
    end

    
    always @(posedge clk) begin
        if (sync2 == debounced) begin
            counter <= 0;
        end
        else if (counter == DEBOUNCE_COUNT - 1) begin
            counter <= 0;
            debounced <= sync2;
        end
        else begin
            counter <= counter + 1'b1;
        end
    end

    
    always @(posedge clk) begin
        debounced_d <= debounced;
    end

    assign pulse = debounced & ~debounced_d;

endmodule

