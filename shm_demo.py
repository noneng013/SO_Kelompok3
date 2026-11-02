import time
from multiprocessing import Process, shared_memory


def worker(shm_name):
    # Logika child process
    pass


def main():
    shm = shared_memory.SharedMemory(create=True, size=1024)
    p = Process(target=worker, args=(shm.name,))
    p.start()
    p.join()
    shm.close()
    shm.unlink()


# WAJIB ADA DI MULTIPROCESSING:
if __name__ == "__main__":
    main()
