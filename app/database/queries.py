from app.database import connection

async def create_user(
        telegram_id: int,
        username: str | None,
        first_name: str | None,
) -> None:
    if connection.pool is None:
        raise RuntimeError('Database pool has not been initialized.')

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO users (TelegramID, UserName, FirstName)
                VALUES (%s, %s, %s)
                ON CONFLICT (TelegramID) DO NOTHING;
                """,
                (telegram_id, username, first_name)
            )
        await conn.commit()

# Products
async def retrieve_products(page: int, products_per_page: int) -> tuple[list, bool]:
    if connection.pool is None:
        raise RuntimeError('Database pool has not been initialized.')

    offset = (page - 1) * products_per_page

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT ProductID, ProductName, ProductCategory, Price, Stock
                FROM products
                ORDER BY ProductID
                LIMIT %s OFFSET %s
                """,
                (products_per_page + 1, offset)
            )

            products = await cur.fetchall()

    has_next_page = len(products) > products_per_page

    return products[:products_per_page], has_next_page

async def add_product(
        name: str,
        category: str,
        price: int,
        stock: int
) -> None:
    if connection.pool is None:
            raise RuntimeError('Database pool has not been initialized.')

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO products (ProductName, Price, Stock, ProductCategory)
                VALUES (%s, %s, %s, %s)
                """,
                (name, price, stock, category)
            )

        await conn.commit()

# Support requests
async def create_support_request(user_id: int, username: str, message: str) -> None:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO support_requests (UserID, Username, Message)
                VALUES (%s, %s, %s)
                """,
                (user_id, username, message)
            )

        await conn.commit()

async def get_user_id(telegram_id: int) -> int | None:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT UserID
                FROM users
                WHERE TelegramID = %s
                """,
                (telegram_id,)
            )

            result = await cur.fetchone()

    return result[0] if result else None