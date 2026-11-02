#!/usr/bin/env python3
# deadlock_demo.py - tiga tugas kontrol berebut bus I2C, katup irigasi, dan pompa air
# pemakaian: python3 deadlock_demo.py [naif|urut|trylock] [jumlah_ulang]
import random
import sys
import threading
import time
 
SUMBER = {"I2C": threading.Lock(), "Katup": threading.Lock(), "Pompa": threading.Lock()}
URUTAN_GLOBAL = ["I2C", "Katup", "Pompa"]          # aturan pengambilan kunci (untuk mode urut)
TUGAS = {"T1": ("I2C", "Katup"), "T2": ("Katup", "Pompa"), "T3": ("Pompa", "I2C")}
BATAS = 0.5       # detik: menunggu lebih lama dari ini dianggap macet
KERJA = 0.02      # lama pekerjaan setelah semua sumber daya didapat
 
def ambil_dua(nama, a, b, mode, hasil):
    if mode == "urut":                              # meniadakan circular wait
        a, b = sorted((a, b), key=URUTAN_GLOBAL.index)
    while True:
        if not SUMBER[a].acquire(timeout=BATAS):
            hasil[nama] = "macet menunggu %s" % a
            return
        time.sleep(0.05)                            # memberi kesempatan tugas lain mengambil sumber daya kedua
        if SUMBER[b].acquire(timeout=BATAS):
            time.sleep(KERJA)                       # pekerjaan di critical section
            SUMBER[b].release()
            SUMBER[a].release()
            hasil[nama] = "selesai"
            return
        SUMBER[a].release()                         # tidak dapat sumber daya kedua
        if mode != "trylock":
            hasil[nama] = "macet: memegang %s, menunggu %s" % (a, b)
            return
        time.sleep(random.uniform(0.01, 0.1))       # trylock: lepas semua, mundur acak, coba lagi
 
def satu_percobaan(mode):
    hasil = {}
    ts = [threading.Thread(target=ambil_dua, args=(n, a, b, mode, hasil), daemon=True) for n, (a, b) in TUGAS.items()]
    t0 = time.perf_counter()
    for t in ts:
        t.start()
    for t in ts:
        t.join(BATAS * 6)
    macet = [n for n in TUGAS if hasil.get(n, "macet").startswith("macet")]
    return macet, time.perf_counter() - t0
 
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "naif"
    ulang = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    print("mode=%s  ulang=%d" % (mode, ulang))
    n_macet = 0
    for i in range(1, ulang + 1):
        for k in SUMBER:                            # setel ulang kunci agar tiap percobaan bersih
            SUMBER[k] = threading.Lock()
        macet, detik = satu_percobaan(mode)
        n_macet += bool(macet)
        print("%3d  %-8s  tugas macet: %-10s  %.2f s" % (i, "DEADLOCK" if macet else "lancar", ",".join(macet) or "-", detik))
    print("Ringkasan: %d dari %d percobaan mengalami deadlock" % (n_macet, ulang))
