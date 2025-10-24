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
    """
    Asynchronously adds a device to the database.

    Args:
        model_name (str): The model name of the device to be added.

    Returns:
        Device: The added device, or "Device not found" if the device is not found.
    """
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

    if links is None:
        return "Device not found"

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

    --- EXAMPLES ---

    1.  **Simple Text Search (LIKE):**
        - User Question: "Find all the Google Pixel phones."
        - `where_clause`: "model_name LIKE '%Google Pixel%'"

    2.  **Numerical Range (AND):**
        - User Question: "Show me phones that cost between $700 and $900."
        - `where_clause`: "price_cents >= 70000 AND price_cents <= 90000"

    3.  **Combining Multiple Conditions (AND with different types):**
        - User Question: "Find iPhones released in 2023 with at least 256GB of storage."
        - `where_clause`: "model_name LIKE '%iPhone%' AND release_date >= '2023-01-01' AND storage_gb >= 256"

    4.  **Using OR logic:**
        - User Question: "I want phones with a huge battery (over 5000 mAh) or a lot of RAM (16GB or more)."
        - `where_clause`: "battery_mah > 5000 OR ram_gb >= 16"

    5.  **Checking for Missing Data (IS NULL):**
        - User Question: "List all devices where the price has not been announced yet."
        - `where_clause`: "price_cents IS NULL"

    6.  **Specific Date:**
        - User Question: "Were any phones released on May 1st, 2024?"
        - `where_clause`: "release_date = '2024-05-01'"

    7.  **Complex Combination with Parentheses:**
        - User Question: "Find either Samsung or Google phones that have 12GB of RAM and cost less than $1000."
        - `where_clause`: "(model_name LIKE '%Samsung S20%' OR model_name LIKE '%Samsung Galaxy A26%') AND ram_gb = 12 AND price_cents < 100000"

    --- IMPORTANT RULES ---
    - String values MUST be enclosed in single quotes (e.g., 'Samsung').
    - Dates MUST be in 'YYYY-MM-DD' format and enclosed in single quotes.
    - Column names are case-sensitive and must match the list above exactly
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
                f"Storage: {device['storage_gb']}GB, Price: ${device['price_cents'] :.2f}"
            )
            response_lines.append(details)
        return "\n".join(response_lines)

    except OperationalError as e:
        return f"Error executing query. The database reported an error, likely due to a syntax mistake in the WHERE clause: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
