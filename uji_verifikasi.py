#!/usr/bin/env python3
# uji_verifikasi.py - bandingkan hasil simulator dengan perhitungan MANUAL (ditulis tangan di laporan)
from penjadwalan import ALGORITMA, simulasi, teks_gantt, DATA
 
# Nilai yang dihitung manual: (Gantt, rata-rata WT, rata-rata TAT, rata-rata RT)
MANUAL = {
    "FCFS": ("P1:0-3 P2:3-9 P3:9-13 P4:13-21 P5:21-23", 7.4, 12.0, 7.4),
    "SJF (non-preemptive)": ("P1:0-3 P3:3-7 P5:7-9 P2:9-15 P4:15-23", 5.0, 9.6, 5.0),
    "SRTF (preemptive)": ("P1:0-3 P3:3-4 P5:4-6 P3:6-9 P2:9-15 P4:15-23", 4.8, 9.4, 4.4),
    "Priority (non-preemptive)": ("P1:0-3 P3:3-7 P5:7-9 P2:9-15 P4:15-23", 5.0, 9.6, 5.0),
    "Priority (preemptive)": ("P1:0-3 P3:3-4 P5:4-6 P3:6-9 P2:9-15 P4:15-23", 4.8, 9.4, 4.4),
    "Round Robin q=2": ("P1:0-2 P2:2-4 P3:4-6 P1:6-7 P4:7-9 P5:9-11 P2:11-13 P3:13-15 P4:15-17 P2:17-19 P4:19-23", 8.6, 13.2, 2.6),
    "Round Robin q=3": ("P1:0-3 P2:3-6 P3:6-9 P4:9-12 P5:12-14 P2:14-17 P3:17-18 P4:18-23", 8.6, 13.2, 4.2),
}
 
lulus = 0
total_burst = sum(d[2] for d in DATA)
for nama in ALGORITMA:
    proses, gantt, m = simulasi(nama)
    g, wt, tat, rt = MANUAL[nama]
    ok = (teks_gantt(gantt) == g and abs(m["wt"] - wt) < 1e-9 and abs(m["tat"] - tat) < 1e-9 and abs(m["rt"] - rt) < 1e-9)
    # pemeriksaan invarian: tidak ada tumpang tindih, total waktu = total burst (tanpa CPU menganggur)
    berurutan = all(gantt[i][2] <= gantt[i + 1][1] for i in range(len(gantt) - 1))
    ok = ok and berurutan and m["selesai"] == total_burst and all(p["wt"] >= 0 for p in proses)
    print("%-26s %s" % (nama, "LULUS" if ok else "GAGAL"))
    lulus += ok
print("Ringkasan: %d dari %d algoritma sesuai dengan perhitungan manual" % (lulus, len(ALGORITMA)))
