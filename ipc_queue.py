#!/usr/bin/env python3
# ipc_queue.py - 3 proses sensor (produsen) -> 1 proses logger (konsumen) lewat message queue
import multiprocessing as mp
import os, random, time
 
LOG = os.path.expanduser("~/k1/log_queue.txt")
NODE = ["N01", "N02", "N03"]
BACAAN = 5
 
def sensor(node, q):
    pid = os.getpid()
    for i in range(BACAAN):
        q.put((node, round(random.uniform(24, 34), 1), round(random.uniform(20, 60), 1), pid))
        time.sleep(random.uniform(0.2, 0.6))
    q.put((node, None, None, pid))           # tanda "node ini selesai"
 
def logger(q):
    selesai = 0
    jumlah = 0
    with open(LOG, "a") as log:
        while selesai < len(NODE):
            node, suhu, tanah, pid = q.get()  # tertahan sampai ada pesan
            if suhu is None:
                selesai += 1
                continue
            waktu = time.strftime("%Y-%m-%d %H:%M:%S")
            log.write("%s queue %s;%.1f;%.1f pid_sensor=%d\n" % (waktu, node, suhu, tanah, pid))
            log.flush()
            jumlah += 1
    print("logger (PID %d): %d pesan dicatat" % (os.getpid(), jumlah))
 
if __name__ == "__main__":
    q = mp.Queue()
    print("induk PID", os.getpid())
    proses_sensor = [mp.Process(target=sensor, args=(n, q)) for n in NODE]
    proses_logger = mp.Process(target=logger, args=(q,))
    proses_logger.start()
    for p in proses_sensor:
        p.start()
    for p in proses_sensor:
        p.join()
    proses_logger.join()
