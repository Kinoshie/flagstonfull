
from fastapi import FastAPI
from pydantic import BaseModel
from flagstonefullscriptwithcaption import run_my_script

app = FastAPI()

class InputData(BaseModel):
    input_text: str = ""

@app.post("/run-script")
def run_script(data: InputData):
    return run_my_script(data.input_text)