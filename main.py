from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import os


app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"


@app.get("/")
def home():
    return JSONResponse(
        content={"message": "Hello, World!"},
        media_type="application/json; charset=utf-8"
    )


@app.get("/greet/{name}")
def greet(name: str):
    return JSONResponse(
        content={"message": f"Привет, {name}!"},
        media_type="application/json; charset=utf-8"
    )


@app.get("/form")
def show_form(request: Request):
    return templates.TemplateResponse(
        name="form.html",
        context={"request": request}
    )


@app.post("/form")
def process_form(request: Request, username: str = Form(...)):
    greeting = f"Привет, {username}!"
    return templates.TemplateResponse(
        name="form.html",
        context={"request": request, "greeting": greeting}
    )


@app.get("/upload")
def show_upload_form(request: Request):
    return templates.TemplateResponse(
        name="upload.html",
        context={"request": request}
    )


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    content = await file.read()

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    file_info = {
        "filename": file.filename,
        "size": len(content),
        "content_type": file.content_type
    }

    return templates.TemplateResponse(
        name="upload.html",
        context={"request": request, "file_info": file_info}
    )
