# Renders alu_waveform.svg (the README ALU waveform) from alu_wave.csv.
# The ALU is combinational, so each column is one applied operation rather than a
# clock cycle: alu_op selects the operation, and result/zero/lt/ltu are the
# settled outputs for that operand pair.
#
# Regenerate the whole figure from the repo root:
#   iverilog -g2012 -s alu_wave_tb -o awave.vvp rtl/alu_pkg.sv rtl/alu.sv docs/alu_wave_tb.sv && vvp awave.vvp
#   python3 docs/alu_waveform.py
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OPS = ['ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND']

rows = list(csv.DictReader(open('alu_wave.csv')))
def col(n): return [int(r[n]) for r in rows]
alu_op = col('alu_op')
a, b, result = col('a'), col('b'), col('result')
zero, lt, ltu = col('zero'), col('lt'), col('ltu')
N = len(rows)

x = list(range(N))

# Lane order, top to bottom
hexbuses = [('a', a), ('b', b), ('result', result)]
bits = [('zero', zero), ('lt', lt), ('ltu', ltu)]
nlanes = 1 + len(hexbuses) + len(bits)      # +1 for the alu_op mnemonic lane
lane_h, gap = 0.72, 0.55
pitch = lane_h + gap

fig, ax = plt.subplots(figsize=(13, 0.62 * nlanes + 1.4))
SIG, GREY = '#08306b', '#dfe6ee'            # one dark-blue colour for every trace
LABEL_X = -0.9                              # signal names centred in a narrow left margin

def base_of(lane_from_top):
    return (nlanes - 1 - lane_from_top) * pitch

def name_label(base, name):
    ax.text(LABEL_X, base + lane_h / 2, name, ha='center', va='center',
            fontsize=11, family='monospace')

def draw_bus(base, vals, fmt):
    top, bot = base + lane_h, base
    seg_start = 0
    for i in range(1, N + 1):
        if i == N or vals[i] != vals[i - 1]:
            val = vals[seg_start]
            ax.plot([seg_start, i], [top, top], color=SIG, lw=1.7, zorder=3)
            ax.plot([seg_start, i], [bot, bot], color=SIG, lw=1.7, zorder=3)
            ax.plot([seg_start, seg_start], [bot, top], color=SIG, lw=1.2, zorder=3)
            ax.plot([i, i], [bot, top], color=SIG, lw=1.2, zorder=3)
            ax.text((seg_start + i) / 2, base + lane_h / 2, fmt(val),
                    ha='center', va='center', fontsize=9.0, family='monospace', color=SIG)
            seg_start = i

lane = 0
# alu_op mnemonic bus: every step is its own segment
base = base_of(lane); lane += 1
name_label(base, 'alu_op')
for i in range(N):
    top, bot = base + lane_h, base
    ax.plot([i, i + 1], [top, top], color=SIG, lw=1.7, zorder=3)
    ax.plot([i, i + 1], [bot, bot], color=SIG, lw=1.7, zorder=3)
    ax.plot([i, i], [bot, top], color=SIG, lw=1.2, zorder=3)
    ax.plot([i + 1, i + 1], [bot, top], color=SIG, lw=1.2, zorder=3)
    ax.text(i + 0.5, base + lane_h / 2, OPS[alu_op[i]], ha='center', va='center',
            fontsize=8.5, family='monospace', color=SIG)

for name, vals in hexbuses:
    base = base_of(lane); lane += 1
    name_label(base, name)
    draw_bus(base, vals, lambda v: f'0x{v & 0xFFFFFFFF:08X}')

for name, vals in bits:
    base = base_of(lane); lane += 1
    ax.axhline(base, color=GREY, lw=0.8, zorder=0)
    seg = vals + [vals[-1]]
    ax.step(list(range(N + 1)), [base + v * lane_h for v in seg], where='post',
            color=SIG, lw=1.8, zorder=3)
    name_label(base, name)

ax.set_xlim(-1.7, N)
ax.set_ylim(-0.4, base_of(0) + lane_h + 0.4)
ax.set_yticks([])
ax.set_xlabel('operation step', fontsize=10)
ax.set_xticks([i + 0.5 for i in range(N)])
ax.set_xticklabels([str(i) for i in range(N)], fontsize=9)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('ALU: representative operations (XLEN = 32)', fontsize=13, pad=16)
plt.tight_layout()
plt.savefig('alu_waveform.svg', bbox_inches='tight', facecolor='white')
print('wrote alu_waveform.svg; rows', N)
