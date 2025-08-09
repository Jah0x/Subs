import json, datetime as dt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
import redis.asyncio as redis

from ..database import SessionLocal
from ..models import UID, UIDStatus
from ..utils.hmac_sig import sign, now_ts
from ..config import LINK_TTL, REDIS_URL, REDIS_CHANNEL

router = APIRouter(prefix="/api/admin", tags=["admin"])
rds = redis.from_url(REDIS_URL)

class AssignReq(BaseModel):
    user_id: int
    plan_id: int | None = None
    expires_at: dt.datetime | None = None

class LinkReq(BaseModel):
    uid: str
    fmt: str | None = "txt"
    exp_override: int | None = None

class RevokeReq(BaseModel):
    uid: str

async def publish_event(kind: str, payload: dict):
    await rds.publish(REDIS_CHANNEL, json.dumps({"kind": kind, "data": payload, "ts": now_ts()}))

@router.post("/assign")
async def api_assign(req: AssignReq):
    async with SessionLocal() as session:
        res = await session.execute(
            select(UID).where(UID.status == UIDStatus.free.value).limit(1).with_for_update(skip_locked=True)
        )
        row = res.scalar_one_or_none()
        if not row:
            raise HTTPException(409, "No free UIDs available")
        row.status = UIDStatus.assigned.value
        row.assigned_user_id = req.user_id
        row.plan_id = req.plan_id
        row.expires_at = req.expires_at
        await session.commit()
        await publish_event("uid.assign", {"uid": row.uid, "plan_id": req.plan_id, "expires_at": str(req.expires_at) if req.expires_at else None})
        return {"uid": row.uid}

@router.post("/revoke")
async def api_revoke(req: RevokeReq):
    async with SessionLocal() as session:
        res = await session.execute(select(UID).where(UID.uid == req.uid))
        row = res.scalar_one_or_none()
        if not row:
            raise HTTPException(404, "UID not found")
        row.status = UIDStatus.suspended.value
        await session.commit()
        await publish_event("uid.revoke", {"uid": row.uid})
        return {"ok": True}

@router.post("/link")
async def api_link(req: LinkReq):
    exp_secs = req.exp_override if req.exp_override is not None else LINK_TTL
    exp = now_ts() + exp_secs if exp_secs and exp_secs > 0 else 0
    payload = f"{req.uid}:{exp}"
    sig = sign(payload)
    ext = "" if (not req.fmt or req.fmt == "txt") else (".yaml" if req.fmt == "yaml" else ".json")
    url = f"/sub/{req.uid}{ext}?sig={sig}&exp={exp}"
    return {"url": url}
