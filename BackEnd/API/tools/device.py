from API.db import Device, get_agent_session
from API.config import settings
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key=settings.FIRECRAWL_API_KEY)

async def add_device(device_name: str):
        res = firecrawl.map(url="https://m.gsmarena.com/", search=device_name, limit=10)
        urls=[]
        for url in res:

        async with get_agent_session() as session:
                session.add(device)
                await session.commit()
                return "Device added successfully"

async def get_device(model_name: str):
        async with get_agent_session() as session:
                device = await session.get(Device, model_name)
                return device