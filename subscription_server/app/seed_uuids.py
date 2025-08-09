import argparse, asyncio, uuid
from .database import SessionLocal
from .models import UID, UIDStatus

async def seed(count: int):
    async with SessionLocal() as session:
        for _ in range(count):
            session.add(UID(uid=str(uuid.uuid4()), status=UIDStatus.free.value))
        await session.commit()
    print(f"Seeded {count} UUIDs.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=500)
    args = parser.parse_args()
    asyncio.run(seed(args.count))
