import sqlalchemy as sa
from API.config import settings
from API.db import Device, get_agent_session
from API.schemas import DeviceSchema
from firecrawl import Firecrawl
from sqlalchemy.exc import OperationalError

from .sql_validator import is_safe_where_clause

firecrawl = Firecrawl(api_key=settings.FIRECRAWL_API_KEY)


async def add_device(model_name: str):
    """
    Adds a device to the database using firecrawl.

    Args:
        model_name (str): The model name of the device to add.

    Returns:
        str: A success message if the device was added successfully, otherwise a failure message.
    """
    res = firecrawl.extract(
        urls=["https://m.gsmarena.com/*"],
        prompt=f"get  model name, release date,display, battery, camera, RAM, storage, and price of {model_name}",
        schema=DeviceSchema.model_json_schema(),
    )
    if not res.data:
        return "No data found"
    device = Device(
        model_name=res.data["model_name"],
        release_date=res.data["release_date"],
        display=res.data["display"],
        battery_mah=res.data["battery_mah"],
        ram_gb=res.data["ram_gb"],
        storage_gb=res.data["storage_gb"],
        camera_specs=res.data["camera_specs"],
        price_cents=res.data["price_cents"],
    )

    async with get_agent_session() as session:
        session.add(device)
        await session.commit()
        return "Device added successfully"


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
            result = await session.exec(statement)
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
