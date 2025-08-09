import os
from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv("HOSTNAME", "zerologsvpn.com")
PORT = int(os.getenv("XRAY_PORT", "443"))
DEFAULT_SNI = os.getenv("DEFAULT_SNI", "www.twitch.tv")
DEFAULT_PBK = os.getenv("DEFAULT_PBK", "CHANGE_ME_PBK")
DEFAULT_SID = os.getenv("DEFAULT_SID", "09c88c34c2a5fdb7")
DEFAULT_FP = os.getenv("DEFAULT_FP", "chrome")
LINK_TTL = int(os.getenv("LINK_TTL", "0"))
HMAC_SECRET = os.getenv("HMAC_SECRET", "change_me_super_secret_key")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_CHANNEL = os.getenv("REDIS_CHANNEL", "uid_events")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "subserver")
POSTGRES_USER = os.getenv("POSTGRES_USER", "subserver")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "subserver_pass")
DB_DSN = os.getenv("DB_DSN") or f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
