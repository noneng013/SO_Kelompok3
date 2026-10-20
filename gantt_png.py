#!/usr/bin/env python3
# gantt_png.py - gambar Gantt chart semua algoritma dari hasil simulator (perlu matplotlib)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from penjadwalan import ALGORITMA, simulasi
 
WARNA = {"P1": "#82B366", "P2": "#6C8EBF", "P3": "#D6B656", "P4": "#B85450", "P5": "#9673A6"}
fig, sumbu = plt.subplots(len(ALGORITMA), 1, figsize=(7.2, 7.6), sharex=True)
for ax, nama in zip(sumbu, ALGORITMA):
    proses, gantt, m = simulasi(nama)
    for pid, s, e in gantt:
        ax.barh(0, e - s, left=s, height=0.6, color=WARNA[pid], edgecolor="black")
        ax.text((s + e) / 2, 0, pid, ha="center", va="center", fontsize=8)
    ax.set_yticks([])
    ax.set_ylabel(nama, rotation=0, ha="right", va="center", fontsize=8)
    ax.set_xlim(0, 23)
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis="x", labelsize=7)
    ax.grid(axis="x", linestyle=":", linewidth=0.5)
sumbu[-1].set_xlabel("Waktu (satuan)")
fig.tight_layout()
fig.savefig("gantt_k2.png", dpi=200)
print("tersimpan: gantt_k2.png")
