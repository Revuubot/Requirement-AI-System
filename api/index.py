import os
import sys
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # root/api
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)

# 2. FAIL-SAFE INITIALIZATION
try:
    # Import routes and logic
    from api.routes import router
    
    app = FastAPI(
        title="Requirement Intelligence Agent",
        version="1.0"
    )

    # Static files and Templates using paths relative to the root
    app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "static")), name="static")
    templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "templates"))

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "message": "Requirement Intelligence API is running"}

    app.include_router(router, prefix="/api")

except Exception as e:
    # 3. RESCUE APP: If any error happens during import/startup, catch it here.
    # This minimal app will display the traceback so we can debug the 500 error.
    app = FastAPI(title="Rescue App (Debug Mode)")
    
    error_traceback = traceback.format_exc()

    @app.get("/{full_path:path}")
    async def rescue_route(request: Request, full_path: str):
        return HTMLResponse(
            content=f"""
            <html>
                <head><title>500 Internal Server Error (Debug Output)</title></head>
                <body style="font-family: monospace; background: #111; color: #ff5555; padding: 20px;">
                    <h1>🚨 Startup Error Detected (Vercel)</h1>
                    <p>The application failed to start due to an error during initialization.</p>
                    <hr/>
                    <h2>Error Message:</h2>
                    <pre style="background: #222; padding: 15px; border-radius: 5px;">{str(e)}</pre>
                    <h2>Traceback:</h2>
                    <pre style="background: #222; padding: 15px; border-radius: 5px;">{error_traceback}</pre>
                </body>
            </html>
            """,
            status_code=500
        )

# Export for Vercel
app = app
