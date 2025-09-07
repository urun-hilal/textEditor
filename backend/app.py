"""
app.py

FastAPI backend service for editing text, YAML, and JSON files.
The service supports uploading files, fetching from Bitbucket, creating
new files, and persisting edits to disk. It also serves a minimal web
interface for interacting with the API.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

import requests
import yaml
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

ALLOWED_EXTENSIONS = {".txt", ".json", ".yaml", ".yml"}
STORAGE_DIR = Path(__file__).parent / "storage"
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def serve_index() -> HTMLResponse:
    """Return the main interface HTML.

    Returns:
        HTMLResponse: rendered index page.
    """

    # Step 1: Read and return index file
    index_path = FRONTEND_DIR / "index.html"
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


class FileContent(BaseModel):
    """Model representing file content."""

    content: str


class FileRecord(BaseModel):
    """In-memory record for a file and its state."""

    content: str
    dirty: bool = False


files: Dict[str, FileRecord] = {}


def _validate_extension(filename: str) -> None:
    """Validate the extension of the provided filename."""

    # Step 1: Ensure extension is allowed
    extension = Path(filename).suffix
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")


def _validate_content(filename: str, content: str) -> None:
    """Validate content according to file type."""

    # Step 1: Validate JSON content
    if filename.endswith(".json"):
        json.loads(content)
    # Step 2: Validate YAML content
    if filename.endswith(('.yaml', '.yml')):
        yaml.safe_load(content)


@app.post("/files/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """Upload a file and store it in memory."""

    # Step 1: Validate extension
    _validate_extension(file.filename)
    content = await file.read()
    text = content.decode("utf-8")

    # Step 2: Validate content
    _validate_content(file.filename, text)

    # Step 3: Store file in memory
    files[file.filename] = FileRecord(content=text, dirty=False)
    return {"filename": file.filename}


class FetchRequest(BaseModel):
    """Request model for fetching Bitbucket files."""

    url: str


@app.post("/files/fetch")
def fetch_file(payload: FetchRequest) -> Dict[str, str]:
    """Fetch file content from Bitbucket using a raw file URL."""

    # Step 1: Retrieve file via HTTP
    response = requests.get(payload.url, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Unable to fetch file")

    # Step 2: Derive filename and validate
    filename = os.path.basename(payload.url)
    _validate_extension(filename)
    text = response.text
    _validate_content(filename, text)

    # Step 3: Store file in memory
    files[filename] = FileRecord(content=text, dirty=False)
    return {"filename": filename}


class CreateRequest(BaseModel):
    """Request model for creating a new file."""

    filename: str
    content: str = ""


@app.post("/files/create")
def create_file(payload: CreateRequest) -> Dict[str, str]:
    """Create a new file in memory."""

    # Step 1: Validate extension and content
    _validate_extension(payload.filename)
    _validate_content(payload.filename, payload.content or "")

    # Step 2: Store file
    files[payload.filename] = FileRecord(content=payload.content, dirty=True)
    return {"message": "File created. Call save endpoint to persist."}


@app.get("/files/{filename}")
def read_file(filename: str) -> FileContent:
    """Read a file from memory."""

    # Step 1: Retrieve file from storage
    record = files.get(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    return FileContent(content=record.content)


@app.put("/files/{filename}")
def update_file(filename: str, payload: FileContent) -> Dict[str, str]:
    """Update an existing file and mark it as dirty."""

    # Step 1: Ensure file exists
    record = files.get(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    # Step 2: Validate new content
    _validate_content(filename, payload.content)

    # Step 3: Update record and prompt to save
    record.content = payload.content
    record.dirty = True
    return {"message": "Changes staged. Call save endpoint to persist."}


@app.post("/files/{filename}/save")
def save_file(filename: str) -> Dict[str, str]:
    """Persist a file to disk."""

    # Step 1: Ensure file exists and is dirty
    record = files.get(filename)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")
    if not record.dirty:
        return {"message": "No changes to save."}

    # Step 2: Write file to storage directory
    STORAGE_DIR.mkdir(exist_ok=True)
    path = STORAGE_DIR / filename
    path.write_text(record.content, encoding="utf-8")
    record.dirty = False
    return {"message": "File saved."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
