module datapath(
  input clk,
  input step,
  input load,
  input [14:0] select,
  input [3:0] state,
  input [1:0] P,
  input [1:0] Q,
  input [1:0] R,
  input [1:0] S,
  input [1:0] T,
  input [1:0] U,
  output reg [31:0] observe,
  output [31:0] A,
  output [31:0] B,
  output [31:0] C,
  output [31:0] D,
  output [31:0] E,
  output [31:0] F,
  output [31:0] X
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

  reg [1:0] P_reg;
  reg [1:0] Q_reg;
  reg [1:0] R_reg;
  reg [1:0] S_reg;
  reg [1:0] T_reg;
  reg [1:0] U_reg;
  reg [31:0] X_1;
  reg [31:0] A_1;
  reg [31:0] X_2;
  reg [31:0] B_1;
  reg [31:0] C_1;
  reg [31:0] X_3;
  reg [31:0] D_1;
  reg [31:0] E_1;
  reg [31:0] X_4;
  reg [31:0] F_1;
  reg [31:0] X_5;
  reg [31:0] X_6;
  reg [31:0] X_7;

  always @(posedge clk) begin
      if (load && step) begin
          P_reg <= P;
          Q_reg <= Q;
          R_reg <= R;
          S_reg <= S;
          T_reg <= T;
          U_reg <= U;
      end
  end

  wire [31:0] add0_lhs;
  wire [31:0] add0_rhs;
  wire [31:0] add0_out;

  wire [31:0] add1_lhs;
  wire [31:0] add1_rhs;
  wire [31:0] add1_out;

  wire [31:0] mul0_lhs;
  wire [31:0] mul0_rhs;
  wire [31:0] mul0_out;

 add add0(
     .a(add0_lhs),
     .b(add0_rhs),
     .out(add0_out)
  );

 add add1(
     .a(add1_lhs),
     .b(add1_rhs),
     .out(add1_out)
  );

 mul mul0(
     .a(mul0_lhs),
     .b(mul0_rhs),
     .out(mul0_out)
  );

 assign add0_lhs = 
     (state == S0) ? T_reg :
     (state == S1) ? P_reg :
     (state == S2) ? Q_reg :
     (state == S3) ? R_reg :
             0;

 assign add0_rhs = 
     (state == S0) ? U_reg :
     (state == S1) ? R_reg :
     (state == S2) ? R_reg :
     (state == S3) ? S_reg :
             0;

 assign add1_lhs = 
     (state == S0) ? P_reg :
     (state == S1) ? P_reg :
     (state == S2) ? Q_reg :
             0;

 assign add1_rhs = 
     (state == S0) ? Q_reg :
     (state == S1) ? S_reg :
     (state == S2) ? S_reg :
             0;

 assign mul0_lhs = 
     (state == S1) ? X_1 :
     (state == S2) ? X_2 :
     (state == S3) ? X_3 :
     (state == S4) ? X_4 :
     (state == S5) ? X_5 :
     (state == S6) ? X_6 :
             0;

 assign mul0_rhs = 
     (state == S1) ? P_reg :
     (state == S2) ? Q_reg :
     (state == S3) ? R_reg :
     (state == S4) ? S_reg :
     (state == S5) ? T_reg :
     (state == S6) ? U_reg :
             0;


  always @(posedge clk) begin
     if (state == S0 && step) begin
         X_1 <= add0_out;
         A_1 <= add1_out;
     end
     if (state == S1 && step) begin
         X_2 <= mul0_out;
         B_1 <= add0_out;
         C_1 <= add1_out;
     end
     if (state == S2 && step) begin
         X_3 <= mul0_out;
         D_1 <= add0_out;
         E_1 <= add1_out;
     end
     if (state == S3 && step) begin
         X_4 <= mul0_out;
         F_1 <= add0_out;
     end
     if (state == S4 && step) begin
         X_5 <= mul0_out;
     end
     if (state == S5 && step) begin
         X_6 <= mul0_out;
     end
     if (state == S6 && step) begin
         X_7 <= mul0_out;
     end
  end

  always@(*) begin
      observe = 0;
      if (select[0]) begin
         observe = add0_out;
      end
      if (select[1]) begin
         observe = add1_out;
      end
      if (select[2]) begin
         observe = mul0_out;
      end
  end

 assign A = A_1;
 assign B = B_1;
 assign C = C_1;
 assign D = D_1;
 assign E = E_1;
 assign F = F_1;
 assign X = X_7;

endmodule