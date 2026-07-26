# alu

[![CI](https://github.com/drewbabel/alu/actions/workflows/ci.yml/badge.svg)](https://github.com/drewbabel/alu/actions/workflows/ci.yml)

A configurable RV32I arithmetic and logic unit and register file in SystemVerilog, with:

- Combinational add, subtract, logical, and shift operations from two operands and an operation select.
- Zero, signed less-than, and unsigned less-than flags for the branch instructions.
- A dual-port synchronous register file with masked write support.
- Shared RV32I types in `alu_pkg`, reused by a separate single-cycle RV32I core.

![ALU block diagram](docs/alu_block.svg)

![Register file block diagram](docs/regfile_block.svg)

## Verification

| Module | Method |
|--------|--------|
| `alu` | Self-checking testbench + exhaustive SymbiYosys proof |
| `regfile` | Self-checking testbench |

The ALU proof is exhaustive over every operand pair and operation, which the combinational datapath admits.

## Implementation

Synthesized for the Xilinx Artix-7 XC7A35T through sv2v, Yosys, and nextpnr-xilinx.

| Module | LUTs | Flip-flops | Fmax |
|--------|------|------------|------|
| `alu` | 492 | 0 | 88 MHz |
| `regfile` | 916 | 992 | 145 MHz |

`fmax.sh` places and routes each module in a registered-boundary harness. The frequencies come from nextpnr-xilinx, an experimental open-source flow with no vendor-signed timing analysis.

## Building and running

```
make MOD=alu                # run a module's testbench
make wave MOD=alu           # run the testbench and open the waveform in Surfer
make formal MOD=alu         # run the module's SymbiYosys proof
./synth_stats.sh alu        # report a module's synthesis cost
./fmax.sh alu tt_alu clk    # fmax and utilization
```

### Tool versions

Icarus Verilog 13.0, Yosys 0.66, nextpnr-xilinx 0.8.2, sv2v 0.0.13, and Surfer.
