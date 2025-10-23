from API.db import Device, get_agent_session

async def add_device(device: Device):
        async with get_agent_session() as session:
                session.add(device)
                await session.commit()
                return "Device added successfully"

async def get_device(model_name: str):
        async with get_agent_session() as session:
                device = await session.get(Device, model_name)
                return device