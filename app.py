from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import router

app = FastAPI(
    title="Requirement Intelligence Agent",
    version="1.0"
)

#
# -------- STATIC + TEMPLATES --------
#

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


#
# -------- UI HOME PAGE --------
#

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#
# -------- HEALTH CHECK --------
#

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Requirement Intelligence API is running"}


#
# -------- API ROUTES --------
#
# NOTE: router has NO prefix — so we add "/api" here
#

app.include_router(router, prefix="/api")
