from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import socket

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Не важно, что эта IP не существует, нам нужен только сокет
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.get("/api/v1/ping")
def ping_server():
    return 200

@app.get("/", response_class=HTMLResponse)
async def main():
    return RedirectResponse("http://192.168.0.108:8800/front/index.html")

if __name__ == "__main__":
    import uvicorn
    ip = get_local_ip()
    print(f"IP: {ip}:8810")
    uvicorn.run(app, host=ip, port=8810)
