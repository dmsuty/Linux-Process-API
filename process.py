import os
import signal
import psutil
import time
from subprocess import PIPE


class Process:
    """
    the class provides a mechanism for interacting
    with a process obtained using its PID
    """
    pid: int
    process: psutil.Process
    killed: bool

    def __init__(self, pid: int):
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
        return self.is_running() or self.is_stopped() or self.is_sleeping()

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
        if self.pid is None:
            return "process was killed"
        ans = {"current status": self.process.status()}
        if self.is_alive():
            ans.update(self.get_mem_info())
            ans.update({"work time": self.get_work_time()})
            ans.update({"CPU used": self.get_cpu_percent()})
            ans.update({"current status": self.process.status()})
        return ans


class NewProcess(Process):
    """
    the class provides a mechanism for interacting
    with a process created by user's command
    """
    pid: int
    process: psutil.Popen
    killed: bool

    def __init__(self, command: list):
        self.killed = False
        self.process = psutil.Popen(command, stdout=PIPE)
        self.pid = self.process.pid

    def get_result(self) -> str:
        """
        works only for processes that were created by crete_py_process method
        """
        self.process.wait()
        output = self.process.stdout.read()
        return output.decode()

    @staticmethod
    def py_process(py_path: str):
        return NewProcess(["/usr/bin/python3", py_path])
