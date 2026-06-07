import db

from fastapi import FastAPI, HTTPException

app = FastAPI()

PROCESS_DIR = "process"


@app.get("/ping")
def read_root():
    return {"message": "pong"}


@app.get("/data/{company}/")
def get_data(company: str):
    documents = db.find_documents_by_company(company)
    if not documents:
        raise HTTPException(status_code=404, detail="Company not found")

    return {"company": company, "documents": documents}
