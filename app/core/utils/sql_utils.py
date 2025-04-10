import uuid


def generate_sql_insert(
    tenant_id: str,
    table: str,
    data: dict,
) -> tuple[str, tuple]:
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f"${i + 1}" for i in range(len(data))])
    return (
        f"INSERT INTO {tenant_id}.{table} ({columns}) VALUES ({placeholders});",
        tuple(data.values()),
    )


def generate_sql_insert_with_returning(
    tenant_id: str,
    table: str,
    data: dict,
    returning: list[str],
) -> tuple[str, tuple]:
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f"${i + 1}" for i in range(len(data))])
    returning_str = ", ".join(returning)
    return (
        f"INSERT INTO {tenant_id}.{table} ({columns}) VALUES ({placeholders}) RETURNING {returning_str};",
        tuple(
            data.values(),
        ),
    )


def generate_sql_read(
    tenant_id: str,
    table: str,
    columns: list[str],
    conditions: dict[str, dict] = {},
) -> tuple[str, tuple]:
    if table == "club":
        tenant_id = "public"
    if table == "remote_config":
        tenant_id = "public"

    columns = ", ".join(columns)
    conditions_str = " AND ".join(
        [
            f"{key} {conditions[key].get('operator', '=')} ${i + 1}"
            for i, key in enumerate(conditions.keys())
        ]
    )
    return (
        f"SELECT {columns} FROM {tenant_id}.{table} {"WHERE " if conditions_str != "" else ""}{conditions_str};",
        tuple(val.get("value") for val in conditions.values()),
    )


def generate_sql_read_with_join_table(
    tenant_id: str,
    table: str,
    columns: list[str],
    join_table: str,
    join_conditions: dict[str, dict],
    conditions: dict[str, dict] = {},
) -> tuple[str, tuple]:
    columns = ", ".join((f"{tenant_id}.{table}.{column}" for column in columns))
    join_conditions_str = " AND ".join(
        [
            f"{tenant_id}.{key} {join_conditions[key].get('operator', '=')} {join_conditions[key].get('direct_value', f'${i + 1}')}"
            for i, key in enumerate(join_conditions.keys())
        ]
    )
    conditions_str = " AND ".join(
        [
            f"{tenant_id}.{key} {conditions[key].get('operator', '=')} ${i + 1 + len(tuple(1 for key in join_conditions.keys() if join_conditions[key].get('direct_value') is None))}"
            for i, key in enumerate(conditions.keys())
        ]
    )
    return (
        f"SELECT {columns} FROM {tenant_id}.{table} JOIN {tenant_id}.{join_table} ON {join_conditions_str} WHERE {conditions_str};",
        tuple(
            (
                *(
                    val.get("value")
                    for val in join_conditions.values()
                    if val.get("value")
                ),
                *(val.get("value") for val in conditions.values() if val.get("value")),
            )
        ),
    )


def generate_sql_update(
    tenant_id: str,
    table: str,
    data: dict,
    conditions: dict,
) -> tuple[str, tuple]:
    columns = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(data.keys())])
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1}" for i, key in enumerate(conditions.keys())]
    )
    return (
        f"UPDATE {tenant_id}.{table} SET {columns} WHERE {conditions_str};",
        tuple(
            [*data.values(), *conditions.values()],
        ),
    )


def generate_sql_update_with_returning(
    tenant_id: str,
    table: str,
    data: dict,
    conditions: dict,
    returning: list[str],
) -> tuple[str, tuple]:
    columns = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(data.keys())])
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1 + len(data)}" for i, key in enumerate(conditions.keys())]
    )
    returning_str = ", ".join(returning)
    return (
        f"UPDATE {tenant_id}.{table} SET {columns} WHERE {conditions_str} RETURNING {returning_str};",
        tuple(
            [*data.values(), *conditions.values()],
        ),
    )


def generate_sql_delete_with_returning(
    tenant_id: str,
    table: str,
    conditions: dict,
) -> tuple[str, tuple]:
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1}" for i, key in enumerate(conditions.keys())]
    )
    return (
        f"DELETE FROM {tenant_id}.{table} WHERE {conditions_str} RETURNING id;",
        tuple(conditions.values()),
    )


def generate_sql_tables_updated_after(
    tenant_id: str,
    table_names: list[str],
) -> str:
    return "UNION ALL ".join(
        [
            f"(SELECT '{table_name}' as table_name FROM {tenant_id if table_name != 'club' and table_name != 'remote_config' else 'public'}.{table_name} WHERE updated_at > $1 LIMIT 1)"
            for table_name in table_names
        ]
    )


def convert_uuid_to_str(data: dict) -> dict:
    for key, value in data.items():
        print(key, value)
        if isinstance(value, uuid.UUID):
            print("here")
            data[key] = str(value)
    return data
