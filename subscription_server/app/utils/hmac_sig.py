import os, hmac, hashlib, time
from dotenv import load_dotenv
load_dotenv()

SECRET = os.getenv("HMAC_SECRET", "change_me_super_secret_key")

def sign(payload: str) -> str:
    return hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

def verify(payload: str, sig: str) -> bool:
    expected = sign(payload)
    return hmac.compare_digest(expected, sig)

def now_ts() -> int:
    return int(time.time())
