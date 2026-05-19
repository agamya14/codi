from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile

from agent.workflow import LangGraphWorkflow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = LangGraphWorkflow()


@app.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
        temp.write(contents)
        temp_path = Path(temp.name)

    result = workflow.run_full_analysis(temp_path)

    return result