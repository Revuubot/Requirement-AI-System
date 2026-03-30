import os
import sys

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # root/api
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)

# 2. MINIMUM VIABLE ASGI HANDLER (ZERO DEPENDENCIES)
# This will determine if the Vercel infrastructure itself is working.
async def app(scope, receive, send):
    if scope['type'] != 'http':
        return
    
    body = b"MINIMUM VIABLE HANDLER ONLINE (Vercel Infrastructure Check)"

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
            [b'content-length', str(len(body)).encode('utf-8')],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': body,
    })

# Export exactly as 'app' to match Vercel's legacy expectations
app = app
