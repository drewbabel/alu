# Renders regfile_waveform.svg (the README register-file waveform) from regfile_wave.csv.
# Read port 1 tracks x5, read port 2 tracks x10, so each synchronous write shows up
# on rdata one cycle later. The x0 write is ignored and the x0 read stays zero.
#
# Regenerate the whole figure from the repo root:
#   iverilog -g2012 -s regfile_wave_tb -o rwave.vvp rtl/regfile.sv docs/regfile_wave_tb.sv && vvp rwave.vvp
#   python3 docs/regfile_waveform.py
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open('regfile_wave.csv')))
def _si(s):
    s = s.strip()
    return int(s) if s.lstrip('-').isdigit() else 0  # pre-reset 'x' -> 0
def col(n): return [_si(r[n]) for r in rows]
rst_n, we = col('rst_n'), col('we')
waddr, wdata = col('waddr'), col('wdata')
raddr1, rdata1 = col('raddr1'), col('rdata1')
raddr2, rdata2 = col('raddr2'), col('rdata2')
N = len(rows)

x = list(range(N))

DEC = lambda v: f'{v}'
HEX = lambda v: f'0x{v & 0xFFFFFFFF:08X}'

# Lane order, top to bottom
bits = [('rst_n', rst_n), ('we', we)]
buses = [('waddr', waddr, DEC), ('wdata', wdata, HEX),
         ('raddr1', raddr1, DEC), ('rdata1', rdata1, HEX),
         ('raddr2', raddr2, DEC), ('rdata2', rdata2, HEX)]
nlanes = len(bits) + len(buses)
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

lane = 0
for name, vals in bits:
    base = base_of(lane); lane += 1
    ax.axhline(base, color=GREY, lw=0.8, zorder=0)
    seg = vals + [vals[-1]]
    ax.step(list(range(N + 1)), [base + v * lane_h for v in seg], where='post',
            color=SIG, lw=1.8, zorder=3)
    name_label(base, name)

for name, vals, fmt in buses:
    base = base_of(lane); lane += 1
    top, bot = base + lane_h, base
    name_label(base, name)
    seg_start = 0
    for i in range(1, N + 1):
        if i == N or vals[i] != vals[i - 1]:
            val = vals[seg_start]
            ax.plot([seg_start, i], [top, top], color=SIG, lw=1.7, zorder=3)
            ax.plot([seg_start, i], [bot, bot], color=SIG, lw=1.7, zorder=3)
            ax.plot([seg_start, seg_start], [bot, top], color=SIG, lw=1.2, zorder=3)
            ax.plot([i, i], [bot, top], color=SIG, lw=1.2, zorder=3)
            ax.text((seg_start + i) / 2, base + lane_h / 2, fmt(val),
                    ha='center', va='center', fontsize=8.5, family='monospace', color=SIG)
            seg_start = i

ax.set_xlim(-1.7, N)
ax.set_ylim(-0.4, base_of(0) + lane_h + 0.4)
ax.set_yticks([])
ax.set_xlabel('clock cycles', fontsize=10)
ax.set_xticks(list(range(N)))
ax.set_xticklabels([str(t) for t in range(N)], fontsize=9)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('Register file: writes and reads (XLEN = 32)', fontsize=13, pad=16)
plt.tight_layout()
plt.savefig('regfile_waveform.svg', bbox_inches='tight', facecolor='white')
print('wrote regfile_waveform.svg; rows', N)
