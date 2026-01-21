from asyncio import get_event_loop

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session, sa_db
from app.core.database.resources.initial_data import CATEGORIES, DISCIPLINES, ITEM_TYPES


async def main():
    await sa_db.connect()
    try:
        async_session = sa_db.get_sessionmaker()
        async with async_session() as session:
            db_: AsyncSession = session
            await db_.execute(
                text(
                    "INSERT INTO kurim.club (id, name, description, deleted_at) "
                    "VALUES ('kurim', 'Atletický klub Kuřim, z.s.', '', null) ON CONFLICT (id) DO NOTHING;"
                )
            )

            await db_.execute(
                text(
                    "INSERT INTO kurim.remote_config (id, urgent_message, show_from, show_to, minimum_app_version, deleted_at) "
                    + " VALUES (0, '', '2024-01-01T00:00:00+00:00', '2024-12-31T23:59:59+00:00', '2.4.0', null)"
                    + " ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.school_year (id, name, deleted_at) "
                    + " VALUES ('537d3234-7d18-11f0-8de9-0242ac120002', '2024/2025', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.school_year (id, name, deleted_at) "
                    + " VALUES ('537d3235-7d18-11f0-8de9-0242ac120002', '2025/2026', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.school_year (id, name, deleted_at) "
                    + " VALUES ('537d3236-7d18-11f0-8de9-0242ac120002', '2026/2027', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            # discipline types
            await db_.execute(
                text(
                    "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                    + " VALUES (-1, 'NONE', 'nezařazeno', '', 'uncategorized', '', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                    + " VALUES (1, 'ASC', 'běhy', 'běhy+překážky', 'runs', 'runs+hurdles', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                    + " VALUES (2, 'DESC', 'vertikální skoky', 'vertikální skoky+běhy na čas', 'vertical jumps', 'vertical jumps+timed runs', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                    + " VALUES (3, 'ASC', 'štafety', 'štafetové běhy', 'relays', 'run relays', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                    + " VALUES (4, 'DESC', 'víceboje', '', 'combined events', '', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                    + " VALUES (5, 'DESC', 'horizontální skoky', '', 'horizontal jumps', '', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            await db_.execute(
                text(
                    "INSERT INTO kurim.discipline_type (id, sort, name, description, name_en, description_en, deleted_at) "
                    + " VALUES (6, 'DESC', 'hody', '', 'throws', '', null) ON CONFLICT (id) DO NOTHING;"
                )
            )
            for category in CATEGORIES:
                await db_.execute(
                    text(
                        f"INSERT into kurim.category (id, description, short_description, description_en, short_description_en, sex, age, deleted_at) "
                        + f" VALUES ({category['Id']}, '{category['Description']}', '{category['ShortDescription']}', '{category['DescriptionEn']}', '{category['ShortDescriptionEn']}', {category['Sex']}, '{category['Age']}', null) ON CONFLICT (id) DO NOTHING; ",
                    )
                )
            for discipline in DISCIPLINES:
                await db_.execute(
                    text(
                        f"INSERT into kurim.discipline (id, description, short_description, description_en, short_description_en, discipline_type_id, traditional, deleted_at) "
                        + f" VALUES ({discipline['Id']}, '{discipline['Description']}', '{discipline['ShortDescription']}', '{discipline['DescriptionEn']}', '{discipline['ShortDescriptionEn']}', {discipline['DisciplineType']}, 1, null) ON CONFLICT (id) DO NOTHING; ",
                    )
                )
            for item_type in ITEM_TYPES:
                await db_.execute(
                    text(
                        f"INSERT into kurim.item_type (id, name, type, deleted_at) "
                        + f" VALUES ('{item_type['id']}', '{item_type['name']}', '{item_type['type']}', null) ON CONFLICT (id) DO NOTHING; ",
                    )
                )

            await db_.commit()
            print("Initial data inserted successfully.")

    except Exception as e:
        print(e)
    finally:
        print("Disconnecting from the database...")
        await sa_db.disconnect()


if __name__ == "__main__":
    print("Inserting initial data...")
    loop = get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    pass
# TODO add other initial data such as disciplines, discipline types, etc.
