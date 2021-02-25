from typing import Optional
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
import requests

router = APIRouter()

# 결제 요청
@router.get('/')
def kakaopay():
    url = "https://kapi.kakao.com/v1/payment/ready"
    APP_ADMIN_KEY = ""
    headers = {
        "Authorization" : f"KakaoAK {APP_ADMIN_KEY}", 
        "content-type" : "application/x-www-form-urlencoded;charset=utf-8"
    }
    query = f"?cid=TC0ONETIME&partner_order_id=partner_order_id&partner_user_id=partner_user_id&item_name=초코파이&quantity=1&total_amount=2200&vat_amount=200&tax_free_amount=0&approval_url=http://localhost:8000/kakaopayf/success&fail_url=http://localhost:8000/kakaopayf/fail&cancel_url=http://localhost:8000/kakaopayf/cancel"
    _res = requests.post(url= url+query, headers= headers)
    _result = _res.json()
    _next_redirect_pc_url = _result["next_redirect_pc_url"]
    _redirectUrl = RedirectResponse(_next_redirect_pc_url,)
    # _redirectUrl.set_cookie(key="ttid",value= str(_result["tid"]))
    # 쿠키 및 DB 대신 파일 활용
    f = open('/Users/doylekim/my/myFastApi/db/db.txt', mode='w',  encoding='utf-8')
    f.write(str(_result["tid"]))
    f.close()
    return _redirectUrl

# 결제 승인
@router.get('/success')
def kakaopay_success(request: Request, response: Response, pg_token: Optional[str]):
    url = "https://kapi.kakao.com/v1/payment/approve"
    APP_ADMIN_KEY = ""
    headers = {
        "Authorization" : f"KakaoAK {APP_ADMIN_KEY}", 
        "content-type" : "application/x-www-form-urlencoded;charset=utf-8"
    }
    # 쿠키 및 DB 대신 JSON 파일 활용
    # tid = request.cookies.get("ttid")
    tidDb = open('/Users/doylekim/my/myFastApi/db/db.txt', mode='r',  encoding='utf-8')
    tid = tidDb.read()
    tidDb.close()
    query = f"?cid=TC0ONETIME&tid={tid}&partner_order_id=partner_order_id&partner_user_id=partner_user_id&pg_token={pg_token}"
    _res = requests.post(url= url+query, headers= headers)
    _result = _res.json()
    viewFile = open('/Users/doylekim/my/myFastApi/views/kakaofPage.html', mode='r',  encoding='utf-8',)
    html_content = viewFile.read()
    viewFile.close()
    tidDbReset = open('/Users/doylekim/my/myFastApi/db/db.txt', mode='w',  encoding='utf-8')
    tidDbReset.write("")
    tidDbReset.close()
    print(_result)
    return HTMLResponse(content=html_content, status_code=200)

# 결제 실패 및 취소
@router.get('/fail')
def kakaopay_fail():
    return
@router.get('/cancel')
def kakaopay_cancel():
    return