from fastapi import FastAPI, Body
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from process import PIDProcess, NewProcess

app = FastAPI()

processes_names = (
    "simple_long_process",
)
processes = dict()
for name in processes_names:
    processes[name] = NewProcess()

@app.get("/")
def read_root():
    return {"Hello, Kaspersky!"}

@app.get("/api/docs")
def docs():
    return RedirectResponse(url="http://127.0.0.1:8000/docs/")

@app.post("/api/{process_name}")
def change_status(process_name: str, item: str = Body(...)):
    if item == "STOP":
        processes[process_name].kill()
        return "process was killed"
    elif item == "START":
        processes[process_name].run_py(f"processes/{process_name}.py")
        return "process has been started"

@app.get("/api/{process_name}")
def get_status(process_name: str):
    return processes[process_name].get_status()

@app.get("/api/result/{process_name}")
def get_result(process_name: str):
    return processes[process_name].get_result()
