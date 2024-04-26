from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="form.html")


@app.post("/postdata")
async def postdata(text=Form()):
    return {"text": text}


@app.on_event("startapp")
async def start_server():
    return True
