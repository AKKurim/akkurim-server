from asyncio import get_event_loop

from app.core.shared.database import db, get_db


async def main():
    await db.connect()
    try:
        async with db.pool.acquire() as connection:
            db_ = connection
            await db_.execute(
                "INSERT INTO public.remote_configs (id, urgent_message, show_from, show_to, minimum_app_version, deleted_at) "
                + " VALUES 0, '', '2024-01-01T00:00:00+00:00', '2024-12-31T23:59:59+00:00', '2.4.0', null"
            )
    except Exception as e:
        print(e)
    finally:
        await db.disconnect()


if __name__ == "__main__":
    loop = get_event_loop()
    main()
    loop.close()
    pass
