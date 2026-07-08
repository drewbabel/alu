`timescale 1ns / 1ps
// Throwaway testbench that generates alu_wave.csv for the README waveform figure.
// The ALU is combinational, so this steps a representative operand/op sequence
// through the DUT and samples every output after it settles, producing one CSV
// row per step (add, sub, the shifts, both compares, and the logic ops).
//
// Regenerate the CSV from the repo root:
//   iverilog -g2012 -s alu_wave_tb -o awave.vvp rtl/alu_pkg.sv rtl/alu.sv docs/alu_wave_tb.sv && vvp awave.vvp
// then render the PNG with docs/alu_waveform.py
module alu_wave_tb;
  import alu_pkg::*;
  localparam int XLEN = 32;

  logic [XLEN-1:0] a, b;
  alu_pkg::alu_op_e alu_op;
  logic [XLEN-1:0] result;
  logic zero, lt, ltu;

  alu #(.XLEN(XLEN)) dut (
      .a(a), .b(b), .alu_op(alu_op),
      .result(result), .zero(zero), .lt(lt), .ltu(ltu)
  );

  integer f;
  task automatic step(input alu_pkg::alu_op_e op,
                      input logic [XLEN-1:0] av, input logic [XLEN-1:0] bv);
    a = av; b = bv; alu_op = op;
    #5;  // let the combinational logic settle
    $fwrite(f, "%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
            op, a, b, result, zero, lt, ltu);
    #5;
  endtask

  initial begin
    f = $fopen("alu_wave.csv", "w");
    $fwrite(f, "alu_op,a,b,result,zero,lt,ltu\n");
    step(ALU_ADD,  32'd5,          32'd3);           // 8
    step(ALU_SUB,  32'd5,          32'd3);           // 2
    step(ALU_SUB,  32'd3,          32'd5);           // -2, signed lt
    step(ALU_SLL,  32'd1,          32'd4);           // 0x10
    step(ALU_SLT,  32'hFFFFFFFF,   32'd1);           // -1 < 1 signed
    step(ALU_SLTU, 32'hFFFFFFFF,   32'd1);           // not < unsigned
    step(ALU_XOR,  32'h000000F0,   32'h0000000F);    // 0xFF
    step(ALU_SRL,  32'h000000F0,   32'd4);           // 0x0F
    step(ALU_SRA,  32'h80000000,   32'd4);           // 0xF8000000
    step(ALU_OR,   32'h000000F0,   32'h0000000F);    // 0xFF
    step(ALU_AND,  32'h000000FF,   32'h0000000F);    // 0x0F
    step(ALU_ADD,  32'd0,          32'd0);           // 0, zero flag
    $fclose(f);
    $finish;
  end
endmodule
