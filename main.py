from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")


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
