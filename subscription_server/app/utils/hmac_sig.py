import hmac, hashlib, time
from ..config import HMAC_SECRET

def sign(payload: str) -> str:
    return hmac.new(HMAC_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

def verify(payload: str, sig: str) -> bool:
    expected = sign(payload)
    return hmac.compare_digest(expected, sig)

def now_ts() -> int:
    return int(time.time())
