from app.database import connection

# User initialization
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

# User products
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

# Admin products
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

# Admin support requests
async def retrieve_open_requests(
        page: int,
        requests_per_page: int
) -> tuple[list, bool]:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    offset = (page - 1) * requests_per_page

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT
                    sr.SupportRequestID,
                    sr.UserID,
                    u.UserName,
                    sr.CreatedAt,
                    sr.Status
                FROM support_requests sr
                JOIN users u ON sr.UserID = U.UserID
                WHERE sr.Status = 'open'
                ORDER BY sr.CreatedAt
                LIMIT %s OFFSET %s
                """,
                (requests_per_page + 1, offset)
            )

            requests = await cur.fetchall()

    has_next_page = len(requests) > requests_per_page

    return requests[:requests_per_page], has_next_page

async def get_request_telegram_id(request_id: int) -> int | None:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT u.TelegramID
                FROM support_requests sr
                JOIN users u ON sr.UserID = u.UserID
                WHERE sr.SupportRequestID = %s
                """,
                (request_id,)
            )

            result = await cur.fetchone()

    return result[0] if result else None

# Support requests
async def create_support_request(user_id: int, message: str) -> int:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO support_requests (UserID)
                VALUES (%s)
                RETURNING SupportRequestID
                """,
                (user_id,)
            )

            request_id = (await cur.fetchone())[0]

            await cur.execute(
                """
                INSERT INTO support_messages (
                    SupportRequestID,
                    SenderType,
                    Message
                )
                VALUES (%s, %s, %s)
                """,
                (request_id, 'user', message)
            )

        await conn.commit()

    return request_id

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

async def get_request(request_id: int) -> tuple | None:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT
                sr.SupportRequestID,
                sr.UserID,
                u.UserName,
                TO_CHAR(sr.CreatedAt, 'MM/DD HH24:MI'),
                sr.Status
                FROM support_requests sr
                JOIN users u ON sr.UserID = u.UserID
                WHERE sr.SupportRequestID = %s
                """,
                (request_id,)
            )

            request = await cur.fetchone()

    return request

async def get_request_messages(request_id: int) -> list[tuple]:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT
                    SenderType,
                    Message,
                    TO_CHAR(CreatedAt, 'MM/DD HH24:MI')
                FROM support_messages
                WHERE SupportRequestID = %s
                ORDER BY CreatedAt
                """,
                (request_id,)
            )

            messages = await cur.fetchall()

    return messages

async def add_request_message(request_id: int, sender_type: str, message: str) -> None:
    if connection.pool is None:
            raise RuntimeError("Database pool has not been initialized.")

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO support_messages (
                    SupportRequestID,
                    SenderType,
                    Message
                )
                VALUES (%s, %s, %s)
                """,
                (request_id, sender_type, message)
            )

        await conn.commit()

async def get_user_requests(telegram_id: int, page: int, requests_per_page: int) -> tuple[list, bool]:
    if connection.pool is None:
        raise RuntimeError("Database pool has not been initialized.")

    offset = (page - 1) * requests_per_page

    async with connection.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT
                    sr.SupportRequestID,
                    TO_CHAR(sr.CreatedAt, 'MM/DD HH24:MI'),
                    sr.Status
                FROM support_requests sr
                JOIN users u ON sr.UserID = u.UserID
                WHERE u.TelegramID = %s
                ORDER BY sr.SupportRequestID DESC
                LIMIT %s OFFSET %s
                """,
                (telegram_id, requests_per_page + 1, offset)
            )
            requests = await cur.fetchall()

    has_next_page = len(requests) > requests_per_page

    return requests[:requests_per_page], has_next_page