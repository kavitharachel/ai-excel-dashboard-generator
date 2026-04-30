from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = file.filename.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file.file, engine="openpyxl")
        else:
            raise HTTPException(status_code=400, detail="Upload only .xlsx or .csv files")

        # Convert dates and blanks safely
        df = df.replace({np.nan: ""})
        df = df.astype(str)

        columns = list(df.columns)
        preview = df.head(10).to_dict(orient="records")

        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": columns,
            "preview": preview
        }

    except Exception as e:
        return {"error": str(e)}