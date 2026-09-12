import os
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv()

DB_CONN_STRING = (
    f"host={os.getenv('DB_HOST')} "
    f"port={os.getenv('DB_PORT')} "
    f"dbname={os.getenv('DB_NAME')} "
    f"user={os.getenv('DB_USER')} "
    f"password={os.getenv('DB_PASSWORD')}"
)

pool: AsyncConnectionPool | None = None

async def init_db() -> None:
    global pool

    pool = AsyncConnectionPool(
        conninfo=DB_CONN_STRING,
        min_size=1,
        max_size=10,
        open=False
    )

    await pool.open()

async def close_db() -> None:
    if pool is not None:
        await pool.close()

# Connection test
async def test_connection() -> None:
    if pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1")
            result = await cur.fetchone()

            print(f"Database connection successful: {result}")
