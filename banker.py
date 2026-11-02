#!/usr/bin/env python3
# banker.py - algoritma Banker: Need, uji safe state, dan uji permintaan sumber daya
# pemakaian: python3 banker.py [berkas.json] [--dot]
# Format berkas.json: {"sumber_daya": [...], "proses": [...], "alokasi": [[...]], "maks": [[...]], "tersedia": [...]}
import json
import sys
 
CONTOH = {   # contoh buku teks (BUKAN data kelas) untuk memverifikasi simulator
    "sumber_daya": ["A", "B", "C"],
    "proses": ["P0", "P1", "P2", "P3", "P4"],
    "alokasi": [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
    "maks": [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
    "tersedia": [3, 3, 2],
}
 
def kurang(a, b):
    return [x - y for x, y in zip(a, b)]
 
def tambah(a, b):
    return [x + y for x, y in zip(a, b)]
 
def lebih_kecil_sama(a, b):
    return all(x <= y for x, y in zip(a, b))
 
def hitung_need(maks, alokasi):
    return [kurang(m, a) for m, a in zip(maks, alokasi)]
 
def uji_aman(proses, alokasi, need, tersedia, cetak=False):
    """Algoritma keamanan. Mengembalikan (aman, urutan_aman). Pemindaian berurutan P0..Pn-1 berulang."""
    n = len(proses)
    kerja = list(tersedia)
    selesai = [False] * n
    urutan = []
    putaran = 0
    while True:
        putaran += 1
        maju = False
        for i in range(n):
            if not selesai[i] and lebih_kecil_sama(need[i], kerja):
                if cetak:
                    print("  putaran %d: %s: Need %s <= Work %s -> Work baru = %s + %s = %s"
                          % (putaran, proses[i], need[i], kerja, kerja, alokasi[i], tambah(kerja, alokasi[i])))
                kerja = tambah(kerja, alokasi[i])
                selesai[i] = True
                urutan.append(proses[i])
                maju = True
        if not maju:
            break
    return all(selesai), urutan
 
def minta(proses, alokasi, maks, tersedia, nama, permintaan, cetak=True):
    """Algoritma permintaan sumber daya. Mengembalikan (keputusan, alokasi_baru, tersedia_baru)."""
    i = proses.index(nama)
    need = hitung_need(maks, alokasi)
    if not lebih_kecil_sama(permintaan, need[i]):
        return "ditolak: melebihi Max", alokasi, tersedia
    if not lebih_kecil_sama(permintaan, tersedia):
        return "tunggu: sumber daya belum tersedia", alokasi, tersedia
    alok2 = [list(r) for r in alokasi]
    alok2[i] = tambah(alok2[i], permintaan)
    tersedia2 = kurang(tersedia, permintaan)
    need2 = hitung_need(maks, alok2)
    aman, urutan = uji_aman(proses, alok2, need2, tersedia2)
    if aman:
        return "diberikan (aman, urutan %s)" % "-".join(urutan), alok2, tersedia2
    return "ditolak: menghasilkan keadaan tidak aman", alokasi, tersedia
 
def dot(d):
    """Keluarkan Resource Allocation Graph (versi ringkas: label = jumlah unit) dalam format DOT."""
    out = ["digraph RAG {", "  rankdir=LR;", '  node [fontname="Helvetica"];']
    for p in d["proses"]:
        out.append('  %s [shape=circle, style=filled, fillcolor="#D5E8D4"];' % p)
    for j, r in enumerate(d["sumber_daya"]):
        out.append('  R%d [shape=box, style=filled, fillcolor="#DAE8FC", label="%s\\n(total %d)"];'
                   % (j, r, sum(row[j] for row in d["alokasi"]) + d["tersedia"][j]))
    need = hitung_need(d["maks"], d["alokasi"])
    for i, p in enumerate(d["proses"]):
        for j in range(len(d["sumber_daya"])):
            if d["alokasi"][i][j]:
                out.append('  R%d -> %s [label="alokasi %d"];' % (j, p, d["alokasi"][i][j]))
            if need[i][j]:
                out.append('  %s -> R%d [style=dashed, label="butuh %d"];' % (p, j, need[i][j]))
    out.append("}")
    return "\n".join(out)
 
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    d = json.load(open(args[0])) if args else CONTOH
    if "--dot" in sys.argv:
        print(dot(d))
        return
    P, A, M, T = d["proses"], d["alokasi"], d["maks"], d["tersedia"]
    need = hitung_need(M, A)
    print("Sumber daya:", d["sumber_daya"], " Available:", T)
    print("%-4s %-12s %-12s %-12s" % ("", "Allocation", "Max", "Need = Max - Allocation"))
    for i, p in enumerate(P):
        print("%-4s %-12s %-12s %-12s" % (p, A[i], M[i], need[i]))
    print("\nAlgoritma keamanan:")
    aman, urutan = uji_aman(P, A, need, T, cetak=True)
    print("Hasil: %s%s" % ("AMAN (safe state), urutan aman: " + " -> ".join(urutan) if aman else "TIDAK AMAN (unsafe state)",
                           "" if aman else ", proses yang dapat selesai: " + ", ".join(urutan)))
    if args == [] :
        print("\nUji permintaan (kumulatif, dimulai dari keadaan awal):")
        alok, ters = A, T
        for nama, req in (("P1", [1, 0, 2]), ("P4", [3, 3, 0]), ("P0", [0, 2, 0])):
            keputusan, alok, ters = minta(P, alok, M, ters, nama, req)
            print("  %s meminta %s -> %s" % (nama, req, keputusan))
 
if __name__ == "__main__":
    main()
