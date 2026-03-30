import os
import sys
import traceback

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # root/api
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)

# 2. DEEP RESCUE ASGI APP (RAW PYTHON, NO DEPENDENCIES)
async def rescue_app(scope, receive, send):
    if scope['type'] != 'http':
        return
    
    error_header = b'Internal Server Error (Deep Diagnosis Mode)'
    error_body = f"""
    <html>
        <head><title>500 Deep Diagnostic Error</title></head>
        <body style="font-family: monospace; background: #1a1a1a; color: #ff5c5c; padding: 40px; line-height: 1.5;">
            <h1 style="border-bottom: 2px solid #ff5c5c; padding-bottom: 10px;">🚨 Deep Startup Error (Vercel)</h1>
            <p>The Python environment failed to initialize correctly. This usually happens when a required library (like FastAPI) fails to import.</p>
            <hr style="opacity: 0.1"/>
            <h2>Crash Traceback:</h2>
            <pre style="background: #2b2b2b; padding: 20px; border-radius: 8px; overflow-x: auto; color: #fff;">{traceback.format_exc()}</pre>
        </body>
    </html>
    """.encode('utf-8')

    await send({
        'type': 'http.response.start',
        'status': 500,
        'headers': [
            [b'content-type', b'text/html'],
            [b'content-length', str(len(error_body)).encode('utf-8')],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': error_body,
    })

# 3. TRY LOADING REAL APP
try:
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates

    # Import routes and logic
    from api.routes import router
    
    app = FastAPI(
        title="Requirement Intelligence Agent",
        version="1.0"
    )

    # 4. DEFENSIVE PATH HANDLING (NO CRASH ON MISSING DIRS)
    STATIC_DIR = os.path.join(ROOT_DIR, "static")
    TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")

    if os.path.exists(STATIC_DIR):
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    else:
        print(f"⚠️ Warning: Static directory {STATIC_DIR} not found.")

    if os.path.exists(TEMPLATES_DIR):
        templates = Jinja2Templates(directory=TEMPLATES_DIR)
    else:
        print(f"⚠️ Warning: Templates directory {TEMPLATES_DIR} not found.")
        templates = None

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        if templates:
            return templates.TemplateResponse("index.html", {"request": request})
        else:
            return HTMLResponse(content="<h1>Dashboard (Templates Missing)</h1><p>The templates directory was not found in the serverless environment.</p>", status_code=500)

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "message": "Requirement Intelligence API is running"}

    app.include_router(router, prefix="/api")

except Exception:
    # If the REAL app fails to load, the global 'app' will be the rescue app
    app = rescue_app

# Export for Vercel
# Important: Vercel expects 'app' to be an ASGI handler
app = app
