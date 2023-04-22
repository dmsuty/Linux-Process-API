import os
import signal
import psutil
import time
from subprocess import PIPE

# TODO make an interface later
class PIDProcess:
    """
    the class provides a mechanism for interacting
    with a process obtained using its PID
    """
    pid: int
    process: psutil.Process
    killed: bool

    dead_statuses = (
        psutil.STATUS_DEAD,
        psutil.STATUS_ZOMBIE
    )

    def __init__(self, pid: int):
        self.killed = True

    def run(self, pid: int):
        self.pid = pid
        self.process = psutil.Process(pid)
        self.killed = False

    def is_running(self) -> bool:
        return not self.killed and\
            self.process.status() == psutil.STATUS_RUNNING

    def is_stopped(self) -> bool:
        return not self.killed and\
            self.process.status() == psutil.STATUS_STOPPED

    def is_sleeping(self) -> bool:
        return not self.killed and\
            self.process.status() == psutil.STATUS_SLEEPING

    def is_alive(self) -> bool:
        """
        if someone else kills the process it will cause problems
        TODO may be caught by exceptions
        """
        return not self.killed and\
            self.process.status() not in self.dead_statuses

    def stop(self):
        if self.is_running():
            os.kill(self.pid, signal.SIGSTOP)

    def run(self):
        if self.is_stopped():
            os.kill(self.pid, signal.SIGCONT)

    def kill(self):
        if self.is_alive():
            self.process.terminate()
        self.killed = True

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
        if not self.is_alive():
            return "process was killed"
        ans = {"current status": self.process.status()}
        if self.is_alive():
            ans.update(self.get_mem_info())
            ans.update({
                "work time": self.get_work_time(),
                "CPU used": self.get_cpu_percent(),
                "current status": self.process.status()
            })
        return ans


class NewProcess(PIDProcess):
    """
    the class provides a mechanism for interacting
    with a process created by user's command
    """
    pid: int
    process: psutil.Popen
    killed: bool

    def __init__(self):
        self.killed = True

    def run(self, command: list):
        self.process = psutil.Popen(command, stdout=PIPE)
        self.pid = self.process.pid
        self.killed = False

    def run_py(self, py_path: str):
        self.run(["/usr/bin/python3", py_path])

    def get_result(self) -> str:
        self.process.wait()
        output = self.process.stdout.read()
        return output.decode()
