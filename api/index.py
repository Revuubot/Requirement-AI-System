import os
import sys
import traceback

# 1. SETUP PATHS
# For Vercel, everything is bundled into the 'api' directory or accessible relative to it.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # This is root/api
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)

# 2. DEEP RESCUE ASGI APP (RAW PYTHON, NO DEPENDENCIES)
async def rescue_app(scope, receive, send):
    if scope['type'] != 'http':
        return
    
    error_body = f"""
    <html>
        <head><title>500 Deep Diagnostic Error</title></head>
        <body style="font-family: monospace; background: #1a1a1a; color: #ff5c5c; padding: 40px; line-height: 1.5;">
            <h1 style="border-bottom: 2px solid #ff5c5c; padding-bottom: 10px;">🚨 Deep Startup Error (Vercel)</h1>
            <p>The Python environment failed to initialize correctly.</p>
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

    # 4. PATHS (STATIC & TEMPLATES NOW INSIDE 'api/')
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

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
            # FIX: Use keyword arguments to avoid version-based positional argument mismatches
            return templates.TemplateResponse(request=request, name="index.html")
        else:
            return HTMLResponse(content="<h1>Dashboard (Templates Missing)</h1>", status_code=500)

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "message": "Requirement Intelligence API is running"}

    app.include_router(router, prefix="/api")

except Exception:
    app = rescue_app

# Export for Vercel
app = app
