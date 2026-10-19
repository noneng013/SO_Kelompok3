#!/usr/bin/env python3
# bench_ipc.py - bandingkan waktu kirim N pesan: pipe anonim vs multiprocessing.Queue
import multiprocessing as mp
import os, time
 
N = 20000
PESAN = b"N01;28.4;41.2\n"
 
def uji_pipe():
    r, w = os.pipe()                          # system call pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        for _ in range(N):
            os.write(w, PESAN)
        os.close(w)
        os._exit(0)
    os.close(w)
    t0 = time.perf_counter()
    total = 0
    with os.fdopen(r, "rb") as f:
        for _ in f:
            total += 1
    os.waitpid(pid, 0)
    return total, time.perf_counter() - t0
 
def kirim(q):
    for _ in range(N):
        q.put(PESAN)
    q.put(None)
 
def uji_queue():
    q = mp.Queue()
    p = mp.Process(target=kirim, args=(q,))
    t0 = time.perf_counter()
    p.start()
    total = 0
    while q.get() is not None:
        total += 1
    p.join()
    return total, time.perf_counter() - t0
 
if __name__ == "__main__":
    for nama, fungsi in (("pipe", uji_pipe), ("queue", uji_queue)):
        total, detik = fungsi()
        print("%-6s: %d pesan diterima dalam %.3f detik (%.0f pesan/detik)" % (nama, total, detik, total / detik))
