#!/usr/bin/env python3
# logger_pipe.py - KONSUMEN: baca pesan dari FIFO dan catat ke file log
import os, time
 
FIFO = "/tmp/kebun_fifo"
LOG = os.path.expanduser("~/k1/log_pipe.txt")
 
def main():
    try:
        os.mkfifo(FIFO)
    except FileExistsError:
        pass
    print("logger: menunggu data di", FIFO, flush=True)
    jumlah = 0
    with open(FIFO, "r") as fifo, open(LOG, "a") as log:
        for baris in fifo:           # read() tertahan sampai ada data
            baris = baris.strip()
            if baris == "SELESAI":
                break
            waktu = time.strftime("%Y-%m-%d %H:%M:%S")
            log.write("%s pipe %s\n" % (waktu, baris))
            log.flush()
            jumlah += 1
            print("logger: terima", baris, flush=True)
    print("logger: selesai, %d pesan dicatat" % jumlah)
 
main()
