from asyncio import get_event_loop

from asyncpg import Connection

from app.core.shared.database import db
from app.resources.initial_data.list_of_categories import CATEGORIES
from app.resources.initial_data.list_of_disciplines import DISCIPLINES
from app.resources.initial_data.list_of_item_types import ITEM_TYPES


async def main():
    await db.connect()
    try:
        async with db.pool.acquire() as connection:
            db_: Connection = connection
            await db_.execute(
                "INSERT INTO public.remote_config (id, urgent_message, show_from, show_to, minimum_app_version, deleted_at) "
                + " VALUES (0, '', '2024-01-01T00:00:00+00:00', '2024-12-31T23:59:59+00:00', '2.4.0', null)"
                + " ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.school_year (id, name, deleted_at) "
                + " VALUES ('537d3234-7d18-11f0-8de9-0242ac120002', '2024/2025', null) ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.school_year (id, name, deleted_at) "
                + " VALUES ('537d3235-7d18-11f0-8de9-0242ac120002', '2025/2026', null) ON CONFLICT (id) DO NOTHING;"
            )
            # discipline types
            await db_.execute(
                "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                + " VALUES (-1, 'NONE', 'nezařazeno', '', 'uncategorized', '', null) ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                + " VALUES (1, 'ASC', 'běhy', 'běhy+překážky', 'runs', 'runs+hurdles', null) ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                + " VALUES (2, 'DESC', 'vertikální skoky', 'vertikální skoky+běhy na čas', 'vertical jumps', 'vertical jumps+timed runs', null) ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                + " VALUES (3, 'ASC', 'štafety', 'štafetové běhy', 'relays', 'run relays', null) ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                + " VALUES (4, 'DESC', 'víceboje', '', 'combined events', '', null) ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                + " VALUES (5, 'DESC', 'horizontální skoky', '', 'horizontal jumps', '', null) ON CONFLICT (id) DO NOTHING;"
            )
            await db_.execute(
                "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                + " VALUES (6, 'DESC', 'hody', '', 'throws', '', null) ON CONFLICT (id) DO NOTHING;"
            )
            for category in CATEGORIES:
                await db_.execute(
                    "INSERT into kurim.category (id, description, short_description, description_en, short_description_en, sex, age, deleted_at) "
                    + " VALUES ($1, $2, $3, $4, $5, $6, $7, null) ON CONFLICT (id) DO NOTHING; ",
                    category["Id"],
                    category["Description"],
                    category["ShortDescription"],
                    category["DescriptionEn"],
                    category["ShortDescription"],
                    category["Sex"],
                    category["Age"],
                )
            for discipline in DISCIPLINES:
                await db_.execute(
                    "INSERT into kurim.discipline (id, description, short_description, description_en, short_description_en, discipline_type_id, traditional, deleted_at) "
                    + " VALUES ($1, $2, $3, $4, $5, $6, 1, null) ON CONFLICT (id) DO NOTHING; ",
                    discipline["Id"],
                    discipline["Description"],
                    discipline["ShortDescription"],
                    discipline["DescriptionEn"],
                    discipline["ShortDescriptionEn"],
                    discipline["DisciplineType"],
                )
            for item_type in ITEM_TYPES:
                await db_.execute(
                    "INSERT into kurim.item_type (id, name, type, deleted_at) "
                    + " VALUES ($1, $2, $3, null) ON CONFLICT (id) DO NOTHING; ",
                    item_type["id"],
                    item_type["name"],
                    item_type["type"],
                )
    except Exception as e:
        print(e)
    finally:
        await db.disconnect()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    pass
# TODO add other initial data such as disciplines, discipline types, etc.
