import socket, os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/front", StaticFiles(directory = "frontend"), name = "front")

cache = {}

# обновление кеша при каждом запросе, по факту делает кеш безполеным но для тестов пойдет
RELOAD = True

def html_reader(html, path="frontend"):
    if html in cache.keys() and not RELOAD:
        return cache[html]
    else:
        cache[html] = open(os.path.join(os.getcwd(), path, html), 'r').read()
        return cache[html]
        
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
    return html_reader("index.html") #RedirectResponse("/front/index.html")

@app.get("/account", response_class=HTMLResponse)
def account():
    return html_reader("account.html")

@app.get("/account/teacher", response_class=HTMLResponse)
def account():
    return html_reader("personal_account_teacher.html")

@app.get("/account/student", response_class=HTMLResponse)
def account():
    return html_reader("personal_account_student.html")

@app.get("/created_test", response_class=HTMLResponse)
def account():
    return html_reader("created_test.html")

if __name__ == "__main__":
    import uvicorn
    ip = get_local_ip()
    print(f"IP: {ip}:8800")
    uvicorn.run(app, host=ip, port=8800)  # Запуск FastAPI
