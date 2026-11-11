module sequencer(
  input clk,
  input step,
  input reset,
  output reg load,
  output reg [3:0] state
);
  localparam IDLE = 4'b0000;
  localparam LOAD = 4'b0001;
  localparam S0 = 4'b0010;
  localparam S1 = 4'b0011;
  localparam S2 = 4'b0100;
  localparam S3 = 4'b0101;
  localparam S4 = 4'b0110;
  localparam S5 = 4'b0111;
  localparam S6 = 4'b1000;

  reg [3:0] next_state;

  always@(posedge clk) begin
      if (reset) begin
          state <= IDLE;
      end
      else if (step) begin
          state <= next_state;
      end
  end

  always@(*) begin
      next_state = state;
      load = 0;
      case (state)
          IDLE: next_state = LOAD;
          LOAD: begin
              next_state = S0;
              load = 1'b1;
          end
          S0: next_state = S1;
          S1: next_state = S2;
          S2: next_state = S3;
          S3: next_state = S4;
          S4: next_state = S5;
          S5: next_state = S6;
          S6: next_state = IDLE;
      endcase
  end
endmodule