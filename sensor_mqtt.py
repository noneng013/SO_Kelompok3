#!/usr/bin/env python3
# sensor_mqtt.py - PENERBIT (publisher): 2 node menerbitkan suhu dan kelembapan tanah
import random, subprocess, time
 
NODE = ["N01", "N02"]
PUTARAN = 5
 
def terbit(topik, nilai):
    subprocess.run(["mosquitto_pub", "-t", topik, "-m", str(nilai)], check=True)
 
for i in range(PUTARAN):
    for n in NODE:
        terbit("kebun/%s/suhu" % n, round(random.uniform(24, 34), 1))
        terbit("kebun/%s/tanah" % n, round(random.uniform(20, 60), 1))
    print("sensor: putaran", i + 1, "terkirim", flush=True)
    time.sleep(1)

