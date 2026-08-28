import aiosqlite

file_name = 'bot.db'


async def init_db():
    async with aiosqlite.connect(file_name) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                phone TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def add_user(user_id: int, username: str, full_name: str):
    async with aiosqlite.connect(file_name) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
        """,
            (user_id, username, full_name),
        )
        await db.commit()


async def add_order(user_id: int, name: str, phone: str, desc: str) -> int:
    async with aiosqlite.connect(file_name) as db:
        cursor = await db.execute(
            """
            INSERT INTO orders (user_id, name, phone, description)
            VALUES (?, ?, ?, ?)
        """,
            (user_id, name, phone, desc),
        )
        await db.commit()
        return cursor.lastrowid