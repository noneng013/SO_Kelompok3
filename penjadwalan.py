#!/usr/bin/env python3
# penjadwalan.py - simulator penjadwalan CPU: FCFS, SJF, SRTF, Priority (NP dan P), Round Robin
# Format data proses: (id, arrival, burst, prioritas); angka prioritas kecil = prioritas tinggi
from collections import deque
 
DATA = [("P1", 0, 3, 1), ("P2", 0, 6, 3), ("P3", 2, 4, 2), ("P4", 3, 8, 4), ("P5", 4, 2, 1)]
 
def buat(data):
    return [{"id": i, "at": a, "bt": b, "pr": p, "sisa": b, "mulai": None, "selesai": None, "no": n}
            for n, (i, a, b, p) in enumerate(data)]
 
def gabung(irisan):
    """Gabungkan irisan waktu berurutan milik proses yang sama: [(id, mulai, selesai), ...]"""
    hasil = []
    for pid, s, e in irisan:
        if hasil and hasil[-1][0] == pid and hasil[-1][2] == s:
            hasil[-1] = (pid, hasil[-1][1], e)
        else:
            hasil.append((pid, s, e))
    return hasil
 
def jalankan(p, t, lama, irisan):
    if p["mulai"] is None:
        p["mulai"] = t
    irisan.append((p["id"], t, t + lama))
    p["sisa"] -= lama
    if p["sisa"] == 0:
        p["selesai"] = t + lama
 
def nonpreemptive(proses, kunci):
    """SJF atau Priority tanpa preemption: pilih proses siap dengan kunci terkecil saat CPU bebas."""
    t, irisan = 0, []
    while any(p["sisa"] > 0 for p in proses):
        siap = [p for p in proses if p["at"] <= t and p["sisa"] > 0]
        if not siap:
            t += 1
            continue
        p = min(siap, key=lambda x: (kunci(x), x["at"], x["no"]))
        jalankan(p, t, p["bt"], irisan)
        t += p["bt"]
    return gabung(irisan)
 
def preemptive(proses, kunci):
    """SRTF atau Priority dengan preemption: keputusan diambil tiap satuan waktu."""
    t, irisan, sedang = 0, [], None
    while any(p["sisa"] > 0 for p in proses):
        siap = [p for p in proses if p["at"] <= t and p["sisa"] > 0]
        if not siap:
            sedang = None
            t += 1
            continue
        p = min(siap, key=lambda x: (kunci(x), 0 if x is sedang else 1, x["at"], x["no"]))
        jalankan(p, t, 1, irisan)
        sedang = p
        t += 1
    return gabung(irisan)
 
def fcfs(proses):
    t, irisan = 0, []
    for p in sorted(proses, key=lambda x: (x["at"], x["no"])):
        t = max(t, p["at"])
        jalankan(p, t, p["bt"], irisan)
        t += p["bt"]
    return gabung(irisan)
 
def round_robin(proses, q):
    """Aturan: proses yang datang tepat saat kuantum habis masuk antrean lebih dulu daripada proses yang baru dipreempt."""
    urut = sorted(proses, key=lambda x: (x["at"], x["no"]))
    antre, irisan, t, i = deque(), [], 0, 0
    while i < len(urut) and urut[i]["at"] <= t:
        antre.append(urut[i]); i += 1
    while antre or i < len(urut):
        if not antre:
            t = urut[i]["at"]
            while i < len(urut) and urut[i]["at"] <= t:
                antre.append(urut[i]); i += 1
        p = antre.popleft()
        lama = min(q, p["sisa"])
        jalankan(p, t, lama, irisan)
        t += lama
        while i < len(urut) and urut[i]["at"] <= t:
            antre.append(urut[i]); i += 1
        if p["sisa"] > 0:
            antre.append(p)
    return gabung(irisan)
 
ALGORITMA = {
    "FCFS": lambda ps: fcfs(ps),
    "SJF (non-preemptive)": lambda ps: nonpreemptive(ps, lambda x: x["bt"]),
    "SRTF (preemptive)": lambda ps: preemptive(ps, lambda x: x["sisa"]),
    "Priority (non-preemptive)": lambda ps: nonpreemptive(ps, lambda x: x["pr"]),
    "Priority (preemptive)": lambda ps: preemptive(ps, lambda x: x["pr"]),
    "Round Robin q=2": lambda ps: round_robin(ps, 2),
    "Round Robin q=3": lambda ps: round_robin(ps, 3),
}
 
def hitung(proses, gantt):
    n = len(proses)
    for p in proses:
        p["tat"] = p["selesai"] - p["at"]
        p["wt"] = p["tat"] - p["bt"]
        p["rt"] = p["mulai"] - p["at"]
    return {"wt": sum(p["wt"] for p in proses) / n, "tat": sum(p["tat"] for p in proses) / n,
            "rt": sum(p["rt"] for p in proses) / n, "pindah": len(gantt) - 1,
            "selesai": max(p["selesai"] for p in proses)}
 
def simulasi(nama, data=DATA):
    proses = buat(data)
    gantt = ALGORITMA[nama](proses)
    return proses, gantt, hitung(proses, gantt)
 
def teks_gantt(gantt):
    return " ".join("%s:%d-%d" % g for g in gantt)
 
if __name__ == "__main__":
    print("%-26s %6s %6s %6s %7s" % ("Algoritma", "WT", "TAT", "RT", "Pindah"))
    for nama in ALGORITMA:
        proses, gantt, m = simulasi(nama)
        print("%-26s %6.2f %6.2f %6.2f %7d" % (nama, m["wt"], m["tat"], m["rt"], m["pindah"]))
        print("   Gantt:", teks_gantt(gantt))
        for p in proses:
            print("   %s  CT=%2d TAT=%2d WT=%2d RT=%2d" % (p["id"], p["selesai"], p["tat"], p["wt"], p["rt"]))
    print("\nSapu kuantum Round Robin:")
    print("%3s %6s %6s %6s %7s" % ("q", "WT", "TAT", "RT", "Pindah"))
    for q in range(1, 9):
        proses = buat(DATA)
        gantt = round_robin(proses, q)
        m = hitung(proses, gantt)
        print("%3d %6.2f %6.2f %6.2f %7d" % (q, m["wt"], m["tat"], m["rt"], m["pindah"]))
