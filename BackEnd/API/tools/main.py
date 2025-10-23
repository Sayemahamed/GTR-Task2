from firecrawl import Firecrawl
from rich import print
import datetime
from typing import Optional

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel

from pydantic import BaseModel, Field

# This is a simple Pydantic model, NOT a SQLModel.
# Its only job is to define a simple schema for Firecrawl.
class FirecrawlDeviceSchema(BaseModel):
    """A simplified schema for extracting device data from a web page."""
    model_name: Optional[str] = Field(None, description="The model name of the device, e.g., 'Samsung Galaxy Tab A11'.")
    release_date: Optional[str] = Field(None, description="The release date, preferably in YYYY-MM-DD format.")
    display: Optional[str] = Field(None, description="Description of the display, e.g., '6.7-inch OLED, 120Hz'.")
    battery_mah: Optional[int] = Field(None, description="Battery capacity in milliampere-hours (mAh), just the number.")
    ram_gb: Optional[int] = Field(None, description="RAM size in gigabytes (GB), just the number.")
    storage_gb: Optional[int] = Field(None, description="Internal storage size in gigabytes (GB), just the number.")
    camera_specs: Optional[str] = Field(None, description="Description of the camera system, e.g., '50MP Main, 12MP Ultrawide'.")
    price_cents: Optional[int] = Field(None, description="Price in the smallest currency unit (e.g., cents). If price is $199.99, this should be 19999.")
firecrawl = Firecrawl(api_key="")



# res = firecrawl.map(
#     url="https://m.gsmarena.com/", search="Samsung Galaxy Tab A11 spec and price", limit=5
#     ,
# )
print(FirecrawlDeviceSchema.schema())

res = firecrawl.extract(
    urls=["https://m.gsmarena.com/*"],
    prompt="get  model name, release date,display, battery, camera, RAM, storage, and price of Samsung Galaxy Tab A11",
    schema=FirecrawlDeviceSchema.model_json_schema(),
)
print(res)
# for url in list(res.links):
    # print(url.url)