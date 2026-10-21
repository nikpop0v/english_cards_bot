import aiosqlite
import asyncio

async def init_db():
    db = await aiosqlite.connect("vocabulary.db")
    await db.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            level TEXT NOT NULL,
            part_of_speech TEXT NOT NULL
        )
    """)
    await db.close()


if __name__ == "__main__":
    asyncio.run(init_db())