import socket, json

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from lib.data_base import register, get_data_for_token
from lib.models import UserRegistration
from lib.tokenizer import hash_password, verify_password

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
from lib.config_init import logger, SECRET_KEY, MEDIA_PATH

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
async def verify_refresh_token(token:str, time:str, devise_id:str, name:str, surname:str, email:str):
    return get_data_for_token(token, time, devise_id, name, surname, email)

@app.get("/api/v1/get_media")
async def get_media(media_id:str):
    return FileResponse(
        os.path.join(MEDIA_PATH, media_id),
        filename=f"{media_id}",
        media_type="application/file"
    )

@app.get("/api/v1/upload_media")
async def upload_media(file = File(...)):
    media_id = creat_media_id()
    if os.path.is_file(os.path.join(os.getcwd(), MEDIA_PATH, media_id)):
        with open(os.path.join(os.getcwd(), MEDIA_PATH, media_id), "wb") as f_d:
            buffer=b''
            while True:
                chunk = await upload_photo.read(1024)
                if not chunk:
                    break
                buffer += chunk
            f_d.write(buffer)

    return {"is_ok": True, "error_code":None, "details": None, "data":{"media_id":media_id}}


if __name__ == "__main__":
    import uvicorn
    ip = get_local_ip()
    print(f"IP: {ip}:8810")
    uvicorn.run(app, host=ip, port=8810)
