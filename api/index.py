import os
import sys
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add the root directory to the Python path to ensure imports like 'api.*' and 'services.*' work
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # this is root/api
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)

# Import the router using the proper package notation
try:
    from api.routes import router
except ImportError:
    from .routes import router

app = FastAPI(
    title="Requirement Intelligence Agent",
    version="1.0"
)

# Global Exception Handler for Debugging on Vercel
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error (Vercel Debug Mode)",
            "message": str(exc),
            "traceback": traceback.format_exc(),
            "path": request.url.path
        }
    )

# Static files and Templates using paths relative to the root
app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        # Fallback to pure text if template fails
        return HTMLResponse(content=f"Template Error: {str(e)}<br><pre>{traceback.format_exc()}</pre>", status_code=500)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Requirement Intelligence API is running on Vercel"}

app.include_router(router, prefix="/api")

# Export for Vercel
app = app
