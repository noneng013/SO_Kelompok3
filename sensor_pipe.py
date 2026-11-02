#!/usr/bin/env python3
# sensor_pipe.py - PRODUSEN: simulasi node sensor, kirim pesan lewat named pipe (FIFO)
import os, random, sys, time
 
FIFO = "/tmp/kebun_fifo"
JUMLAH = int(sys.argv[1]) if len(sys.argv) > 1 else 5
 
def main():
    try:
        os.mkfifo(FIFO)              # berkas khusus bertipe pipe di sistem file
    except FileExistsError:
        pass
    print("sensor: membuka FIFO (menunggu logger)...", flush=True)
    with open(FIFO, "w") as f:       # open() tertahan sampai ada proses pembaca
        for i in range(JUMLAH):
            pesan = "N01;%.1f;%.1f" % (random.uniform(24, 34), random.uniform(20, 60))
            f.write(pesan + "\n")
            f.flush()                # dorong pesan ke pipe sekarang juga
            print("sensor: kirim", pesan, flush=True)
            time.sleep(1)
        f.write("SELESAI\n")
 
main()
