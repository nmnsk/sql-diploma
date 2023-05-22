from typing import Any
from asyncio import sleep

import docker
import psycopg2

from app.settings import settings


def update_attrs(instance: Any, **kwargs: Any) -> None:
    for k, v in kwargs.items():
        setattr(instance, k, v)


async def create_container_if_not_exists(username: str) -> None:
    client = docker.from_env()
    if not client.containers.list(filters={"name": username}):
        container = client.containers.run(
            'sql-diploma-db_demo',
            environment=[f"POSTGRES_USER={settings.DB_DEMO_USER}", f"POSTGRES_PASSWORD={settings.DB_DEMO_PASSWORD}"],
            name=username, network='sql-diploma_default',
            hostname=username, detach=True)
        await sleep(30)
        container.exec_run("psql -f demo_small.sql -U postgres")


def get_db_demo_connection(username: str):
    return psycopg2.connect(database=settings.DB_DEMO_DATABASE, user=settings.DB_DEMO_USER,
                            password=settings.DB_DEMO_PASSWORD, host=username, port=settings.DB_DEMO_PORT)


async def analyze_query(query: str, username: str):
    await create_container_if_not_exists(username)
    conn = get_db_demo_connection(username)
    with conn:
        with conn.cursor() as cur:
            cur.execute("EXPLAIN ANALYZE " + query.removesuffix("EXPLAIN ANALYZE"))
            ans_from_explain = cur.fetchall()
    conn.rollback()
    rows = 0
    for ans_part in ans_from_explain:
        if "rows" in ans_part[0]:
            rows += int(ans_part[0][ans_part[0].rfind("rows") + 5: ans_part[0].rfind("loops") - 1])
    full_time = float(ans_from_explain[-1][0][ans_from_explain[-1][0].find(":") + 2: ans_from_explain[-1][0].find("ms") - 1])
    full_time += float(ans_from_explain[-2][0][ans_from_explain[-2][0].find(":") + 2: ans_from_explain[-2][0].find("ms") - 1])
    return rows, full_time
