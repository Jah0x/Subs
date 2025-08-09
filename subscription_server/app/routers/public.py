import json, datetime as dt
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy import select
from jinja2 import Template

from ..database import SessionLocal
from ..models import UID, UIDStatus
from ..utils.hmac_sig import verify, now_ts
from ..config import HOST, PORT, DEFAULT_SNI, DEFAULT_PBK, DEFAULT_SID, DEFAULT_FP

router = APIRouter(tags=["public"])

def _check_link(uid: str, sig: str | None, exp: int | None):
    if exp is None: exp = 0
    if sig is None: sig = ""
    if exp and now_ts() > int(exp):
        raise HTTPException(401, "Link expired")
    if exp or sig:
        payload = f"{uid}:{exp}"
        if not verify(payload, sig):
            raise HTTPException(401, "Bad signature")

async def _get_active_uid(uid: str) -> UID:
    async with SessionLocal() as session:
        q = await session.execute(select(UID).where(UID.uid == uid))
        row = q.scalar_one_or_none()
        if not row:
            raise HTTPException(404, "UID not found")
        if row.status not in (UIDStatus.assigned.value,):
            raise HTTPException(403, "UID inactive")
        if row.expires_at and dt.datetime.now(dt.timezone.utc) > row.expires_at:
            raise HTTPException(403, "UID expired")
        return row

def _entries_for(uid: str):
    return [{
        "uid": uid,
        "pbk": DEFAULT_PBK,
        "sid": DEFAULT_SID,
        "sni": DEFAULT_SNI
    }]

@router.get("/sub/{uid}", response_class=PlainTextResponse)
async def sub_txt(uid: str, sig: str | None = Query(None), exp: int | None = Query(None)):
    _check_link(uid, sig, exp)
    await _get_active_uid(uid)
    from importlib.resources import files
    tpl = (files("subscription_server.app.templates") / "vless.txt.j2").read_text()
    content = Template(tpl).render(entries=_entries_for(uid), host=HOST, port=PORT, sni=DEFAULT_SNI, fp=DEFAULT_FP)
    return PlainTextResponse(content.strip() + "\n")

@router.get("/sub/{uid}.yaml", response_class=PlainTextResponse)
async def sub_yaml(uid: str, sig: str | None = Query(None), exp: int | None = Query(None)):
    _check_link(uid, sig, exp)
    await _get_active_uid(uid)
    from importlib.resources import files
    tpl = (files("subscription_server.app.templates") / "clash.yaml.j2").read_text()
    content = Template(tpl).render(entries=_entries_for(uid), host=HOST, port=PORT, sni=DEFAULT_SNI, fp=DEFAULT_FP)
    return PlainTextResponse(content)

@router.get("/sub/{uid}.json", response_class=JSONResponse)
async def sub_json(uid: str, sig: str | None = Query(None), exp: int | None = Query(None)):
    _check_link(uid, sig, exp)
    await _get_active_uid(uid)
    from importlib.resources import files
    tpl = (files("subscription_server.app.templates") / "singbox.json.j2").read_text()
    rendered = Template(tpl).render(entries=_entries_for(uid), host=HOST, port=PORT, sni=DEFAULT_SNI, fp=DEFAULT_FP)
    return JSONResponse(json.loads(rendered))
