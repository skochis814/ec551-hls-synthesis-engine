module top(
  input clk,
  input step,
  input reset,
  input [14:0] select,
  input [1:0] P,
  input [1:0] Q,
  input [1:0] R,
  input [1:0] S,
  input [1:0] T,
  input [1:0] U,
  output [31:0] observe,
  output [31:0] A,
  output [31:0] B,
  output [31:0] C,
  output [31:0] D,
  output [31:0] E,
  output [31:0] F,
  output [31:0] X
);

  wire load;
  wire [3:0] state;

  sequencer dut1(
      .clk(clk),
      .step(step),
      .reset(reset),
      .load(load),
      .state(state)
  );

  datapath dut2(
      .clk(clk),
      .step(step),
      .load(load),
      .select(select),
      .state(state),
      .P(P),
      .Q(Q),
      .R(R),
      .S(S),
      .T(T),
      .U(U),
      .observe(observe),
      .A(A),
      .B(B),
      .C(C),
      .D(D),
      .E(E),
      .F(F),
      .X(X)
  );

endmodule