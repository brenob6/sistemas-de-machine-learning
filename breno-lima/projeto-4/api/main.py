import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

PROCESS_DIR = "process"


@app.get("/ping")
def read_root():
    return {"message": "pong"}


@app.get("/csv")
def read_csv(company: str, year: int, quarter: int):
    csv_path = os.path.join(PROCESS_DIR, company, str(year), f"Q{quarter}.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(
            status_code=404,
            detail=f"CSV não encontrado para {company} {year} Q{quarter}",
        )
    return FileResponse(
        csv_path,
        media_type="text/csv",
        filename=f"{company}_{year}_Q{quarter}.csv",
    )
