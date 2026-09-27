import socket, json

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from lib.data_base import register
from lib.models import UserRegistration
from lib.tokenizer import hash_password, verify_password

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
from lib.config_init import logger, SECRET_KEY

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # разрешоные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/", response_class=HTMLResponse)
async def main():
    return RedirectResponse("http://192.168.0.108:8800/front/index.html")

@app.get("/api/v1/ping")
async def ping_server():
    return 200

@app.post("/api/v1/new_user")
async def new_user(user: UserRegistration):
    data = register(user.name, user.surname, user.email, hash_password(user.password), user.role, None, user.classU, user.devise_id)
    return data

@app.get("/api/v1/verify_refresh_token")
async def verify_refresh_token(token:str, time:float, devise_id:str):
    get_data_for_token(token, time, devise_id)

if __name__ == "__main__":
    import uvicorn
    ip = get_local_ip()
    print(f"IP: {ip}:8810")
    uvicorn.run(app, host=ip, port=8810)
