// Regfile timing harness
module tt_regfile (
    input  logic clk,
    input  logic rst_n,
    input  logic si,
    output logic so
);
  localparam int AWIDTH = 5;
  localparam int XLEN = 32;
  localparam int NIN = 1 + XLEN + 3 * AWIDTH;

  logic [NIN-1:0] in_r;
  logic [2*XLEN-1:0] out_w, out_r;

  always_ff @(posedge clk) in_r <= {in_r[NIN-2:0], si};

  regfile dut (
      .clk   (clk),
      .rst_n (rst_n),
      .we    (in_r[0]),
      .waddr (in_r[5:1]),
      .wdata (in_r[37:6]),
      .raddr1(in_r[42:38]),
      .raddr2(in_r[47:43]),
      .rdata1(out_w[31:0]),
      .rdata2(out_w[63:32])
  );

  always_ff @(posedge clk) out_r <= out_w;
  always_ff @(posedge clk) so <= ^out_r;
endmodule
