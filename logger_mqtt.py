#!/usr/bin/env python3
# logger_mqtt.py - PELANGGAN (subscriber): catat pesan MQTT ke file log
# pemakaian: python3 logger_mqtt.py [filter_topik] [jumlah_pesan] [nama_log]
import os, subprocess, sys, time
 
FILTER = sys.argv[1] if len(sys.argv) > 1 else "kebun/#"
BATAS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
LOG = os.path.expanduser("~/k1/" + (sys.argv[3] if len(sys.argv) > 3 else "log_mqtt.txt"))
 
# stdbuf -oL: keluaran per baris agar pesan tidak tertahan di penyangga pipe
perintah = ["stdbuf", "-oL", "mosquitto_sub", "-t", FILTER, "-v"]
with subprocess.Popen(perintah, stdout=subprocess.PIPE, text=True) as p, open(LOG, "a") as log:
    print("logger: berlangganan", FILTER, flush=True)
    jumlah = 0
    for baris in p.stdout:                # format: "<topik> <nilai>"
        waktu = time.strftime("%Y-%m-%d %H:%M:%S")
        log.write("%s mqtt %s" % (waktu, baris))
        log.flush()
        jumlah += 1
        print("logger: terima", baris.strip(), flush=True)
        if jumlah >= BATAS:
            break
    p.terminate()
print("logger: selesai, %d pesan dicatat" % jumlah)

