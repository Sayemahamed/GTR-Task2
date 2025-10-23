import asyncio
import re
from urllib.parse import quote_plus

import sqlalchemy as sa
from API.config import settings
from API.db import Device, get_agent_session
from API.schemas import DeviceSchema
from API.tools.sql_validator import is_safe_where_clause
from firecrawl import Firecrawl
from psycopg import OperationalError

firecrawl = Firecrawl(api_key=settings.FIRECRAWL_API_KEY)


async def add_device(model_name: str):
    encoded_model_name = quote_plus(model_name)
    print(encoded_model_name)

    search_url = f"https://www.gsmarena.com/res.php3?sSearch={encoded_model_name}"
    scrape_result = await asyncio.to_thread(
        firecrawl.scrape,
        url=search_url,
        only_main_content=True,
    )
    print(scrape_result.markdown)
    pattern = r"\((https://www.gsmarena.com/.*?\.php)\)"
    match = re.search(pattern, scrape_result.markdown)  # type: ignore

    links = match.group(1)
    print(links)

    extraction = await asyncio.to_thread(
        firecrawl.extract,
        urls=[links],
        prompt=f"Extract the device specifications for {model_name}.",
        schema=DeviceSchema.model_json_schema(),
    )
    if extraction.data is None:
        return "Device not found"
    print(extraction)
    async with get_agent_session() as session:
        device = Device(
            battery_mah=extraction.data["battery_mah"],
            camera_specs=extraction.data["camera_specs"],
            display=extraction.data["display"],
            model_name=extraction.data["model_name"],
            price_cents=extraction.data["price_cents"],
            ram_gb=extraction.data["ram_gb"],
            release_date=extraction.data["release_date"],
            storage_gb=extraction.data["storage_gb"],
        )
        session.add(device)
        await session.commit()
    return device


async def query_devices(where_clause: str) -> str:
    """
    Executes a read-only SQL query to find devices based on specific criteria.
    Use this for complex questions that involve multiple conditions, comparisons (>, <, =),
    or text matching (LIKE).

    The available columns on the 'devices' table are:
    - model_name (string)
    - release_date (date, format 'YYYY-MM-DD')
    - display (string)
    - battery_mah (integer)
    - ram_gb (integer)
    - storage_gb (integer)
    - camera_specs (string)
    - price_cents (integer)

    IMPORTANT: String values must be enclosed in single quotes.
    For example, to find all Samsung phones with more than 8GB of RAM, the
    `where_clause` would be: "model_name LIKE '%Samsung%' AND ram_gb > 8".
    """
    if not is_safe_where_clause(where_clause):
        return "Error: Your query contains forbidden or unsafe SQL commands. You can only use SELECT statements with a WHERE clause."

    full_sql_query = f"SELECT * FROM devices WHERE {where_clause};"

    try:
        async with get_agent_session() as session:
            statement = sa.text(full_sql_query)
            print(statement)
            result = await session.exec(statement)  # type: ignore
            devices = result.all()

        if not devices:
            return f"No devices were found that match the criteria: {where_clause}"

        response_lines = [f"Found {len(devices)} matching devices:"]
        for device_row in devices:
            device = device_row._asdict()
            details = (
                f"- Model: {device['model_name']}, RAM: {device['ram_gb']}GB, "
                f"Storage: {device['storage_gb']}GB, Price: ${device['price_cents'] / 100:.2f}"
            )
            response_lines.append(details)
        return "\n".join(response_lines)

    except OperationalError as e:
        return f"Error executing query. The database reported an error, likely due to a syntax mistake in the WHERE clause: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
