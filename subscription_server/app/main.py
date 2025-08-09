from fastapi import FastAPI
from .routers import public, admin

app = FastAPI(title="ZerologsVPN Subscription API", version="1.0.0")
app.include_router(admin.router)
app.include_router(public.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
