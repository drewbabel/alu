// ALU timing harness
module tt_alu (
    input  logic clk,
    input  logic si,
    output logic so
);
  localparam int XLEN = 32;
  localparam int OPW = $bits(alu_pkg::alu_op_e);
  localparam int NIN = 2 * XLEN + OPW;

  logic [NIN-1:0] in_r;
  logic [XLEN+2:0] out_w, out_r;

  always_ff @(posedge clk) in_r <= {in_r[NIN-2:0], si};

  alu dut (
      .a     (in_r[31:0]),
      .b     (in_r[63:32]),
      .alu_op(alu_pkg::alu_op_e'(in_r[63+OPW:64])),
      .result(out_w[31:0]),
      .zero  (out_w[32]),
      .lt    (out_w[33]),
      .ltu   (out_w[34])
  );

  always_ff @(posedge clk) out_r <= out_w;
  always_ff @(posedge clk) so <= ^out_r;
endmodule
