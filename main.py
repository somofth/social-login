# pip3 install fastapi
# pip3 install uvicorn

from typing import Optional
from fastapi import FastAPI, Response, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

# CORS
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:8000",
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