`timescale 1ns / 1ps
// Throwaway testbench that generates regfile_wave.csv for the README waveform figure.
// Read port 1 watches x5 and read port 2 watches x10 the whole time, so the two
// synchronous writes appear one cycle after they are issued. A write to x0 is
// attempted and ignored, and read port 1 is pointed at x0 at the end to show it
// always reads zero.
//
// Regenerate the CSV from the repo root:
//   iverilog -g2012 -s regfile_wave_tb -o rwave.vvp rtl/regfile.sv docs/regfile_wave_tb.sv && vvp rwave.vvp
// then render the PNG with docs/regfile_waveform.py
module regfile_wave_tb;
  localparam int AWIDTH = 5;
  localparam int XLEN = 32;

  logic clk = 0, rst_n = 0, we = 0;
  logic [AWIDTH-1:0] waddr = 0, raddr1 = 5, raddr2 = 10;
  logic [XLEN-1:0] wdata = 0, rdata1, rdata2;

  regfile #(.AWIDTH(AWIDTH), .XLEN(XLEN)) dut (
      .clk(clk), .rst_n(rst_n), .we(we),
      .waddr(waddr), .wdata(wdata),
      .raddr1(raddr1), .raddr2(raddr2),
      .rdata1(rdata1), .rdata2(rdata2)
  );

  always #5 clk = ~clk;  // 10 ns period

  integer f;
  initial begin
    f = $fopen("regfile_wave.csv", "w");
    $fwrite(f, "rst_n,we,waddr,wdata,raddr1,rdata1,raddr2,rdata2\n");

    repeat (2) @(posedge clk);
    rst_n = 1'b1;
    @(posedge clk);

    #1 we = 1'b1; waddr = 5;  wdata = 32'hAA; @(posedge clk);   // write x5
    #1 we = 1'b1; waddr = 10; wdata = 32'hBB; @(posedge clk);   // write x10
    #1 we = 1'b1; waddr = 0;  wdata = 32'hCC; @(posedge clk);   // write x0 (ignored)
    #1 we = 1'b0; raddr1 = 0;                  @(posedge clk);   // read x0 -> 0
    #1 raddr1 = 5;                             @(posedge clk);   // read x5 -> 0xAA
    repeat (2) @(posedge clk);

    $fclose(f);
    $finish;
  end

  // Sample every clock into the CSV
  always @(posedge clk)
    $fwrite(f, "%b,%b,%0d,%0d,%0d,%0d,%0d,%0d\n",
            rst_n, we, waddr, wdata, raddr1, rdata1, raddr2, rdata2);

  initial begin
    #100000;
    $fclose(f);
    $display("TIMEOUT");
    $finish;
  end
endmodule
