# pip3 install fastapi
# pip3 install uvicorn

from typing import Optional
from fastapi import FastAPI, Response, WebSocket, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
import requests
from routers import items_router, kakao_pay_router, kakao_pay_routerf

app = FastAPI()
app.include_router(
    items_router.router,
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not ITEMS"}},
)
app.include_router(
    kakao_pay_router.router,
    prefix="/kakaopay",
    tags=["kakao"],
    responses={404: {"description": "Not KAKAO"}},
)
app.include_router(
    kakao_pay_routerf.router,
    prefix="/kakaopayf",
    tags=["kakaof"],
    responses={404: {"description": "Not KAKAOF"}},
)

# CORS
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json("FAST API")
    data = await websocket.receive_text()
    print(data)
    return

@app.get("/")
def read_root():
    return {"Hello": "World"} # content-type: application/json

# GET - DynamicPath & QS
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# 타입 지정 1
@app.get("/sendFile1")
def sendHTML1():
    content = """
    <html>
        <head>
            <title>Some HTML in here 1</title>
        </head>
        <body>
            <h1>Look ma! HTML! 1</h1>
        </body>
    </html>
    """
    return Response(content, media_type="text/html", status_code=200)

# 타입 지정 2
@app.get("/sendFile2")
def sendHTML2():
    html_content =  """
    <html>
        <head>
            <title>Some HTML in here 2</title>
        </head>
        <body>
            <h1>Look ma! HTML! 2</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# HTML 파일 사용
@app.get("/sendFile3")
def sendHTML3():
    f = open('/Users/doylekim/my/myFastApi/index.html', mode='r',  encoding='utf-8',)
    html_content = f.read()
    f.close()
    return HTMLResponse(content=html_content, status_code=200)

# POST - DynamicPath & QS
@app.post("/items/{item_id}")
def read_post_item(item_id: str, q: Optional[str]='아이템'):
    return {"id": item_id, "etc": q}

# 미들웨어 : 모든 Path 에서 동작
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print("전처리")
    response = await call_next(request)
    return response

# KakaO Login
@app.get('/kakao')
def kakao():
    REST_API_KEY = ""
    REDIRECT_URI = "http://127.0.0.1:8000/auth"
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&response_type=code&redirect_uri={REDIRECT_URI}"
    response = RedirectResponse(url)
    return response

@app.get('/auth')
async def kakaoAuth(response: Response, code: Optional[str]="NONE"):
    REST_API_KEY = ''
    REDIRECT_URI = 'http://127.0.0.1:8000/auth'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&code={code}&redirect_uri={REDIRECT_URI}'
    _res = requests.post(_url)
    _result = _res.json()
    response.set_cookie(key="kakao", value=str(_result["access_token"]))
    return {"code":_result}

@app.get('/kakaoLogout')
def kakaoLogout(request: Request, response: Response):
    url = "https://kapi.kakao.com/v1/user/unlink"
    KEY = request.cookies['kakao']
    headers = dict(Authorization=f"Bearer {KEY}")
    _res = requests.post(url,headers=headers)
    response.set_cookie(key="kakao", value=None)
    return {"logout": _res.json()}