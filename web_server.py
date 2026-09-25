from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import socket

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/front", StaticFiles(directory = "frontend"), name = "front")

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

@app.get("/ping")
def ping_server():
    return 200

@app.get("/", response_class=HTMLResponse)
async def main():
    return RedirectResponse("/front/index.html")

if __name__ == "__main__":
    import uvicorn
    ip = get_local_ip()
    print(f"IP: {ip}:8800")
    uvicorn.run(app, host=ip, port=8800)  # Запуск FastAPI
