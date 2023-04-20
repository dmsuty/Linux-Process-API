import os
import signal
import psutil
import time

class Process:
    def __init__(self, py_path: str):
        self.py_path = py_path
        self.process = None

    def run(self):
        pid = os.fork()
        if pid == 0:
            os.execlp("python3", "python3", self.py_path)
        self.process = psutil.Process(pid)

    def is_alive(self) -> bool:
        return self.process is not None and\
            self.process.status() == psutil.STATUS_RUNNING

    def get_cpu_percent(self) -> int:
        return self.process.cpu_percent()

    def get_mem_info(self) -> dict:
        mem = self.process.memory_full_info()
        return {"RSS": mem[0], "VMS": mem[1]}

    def get_work_time(self) -> int:
        return time.time() - self.process.create_time()

    def get_cpu_time(self):
        return self.process.cpu_times()

    def status(self) -> dict:
        ans = self.get_mem_info()
        ans.update({"work time": self.get_work_time()})
        ans.update({"CPU used": self.get_cpu_percent()})
        return ans

    def kill(self):
        if self.is_alive():
            os.kill(self.pid, signal.SIGKILL)