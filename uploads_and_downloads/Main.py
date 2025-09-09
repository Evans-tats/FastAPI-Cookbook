from fastapi import FastAPI,File,UploadFile,HTTPException,status
from fastapi.responses import FileResponse
import shutil
from pathlib import Path

app = FastAPI()

@app.post('/uploadfile')
async def upload_file(file: UploadFile = File(...)):
    with open (f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename" : file.filename}


@app.get("/downloadfile/{filename}")
async def download_file(filename: str):
    file_path = Path(f"uploads/{filename}")
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filename}' not found",
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )