from typing import Optional

from pydantic import BaseModel, Field


class DeviceSchema(BaseModel):
    """A simplified schema for extracting device data from a web page."""

    model_name: Optional[str] = Field(
        None,
        description="The model name of the device, e.g., 'Samsung Galaxy Tab A11'.",
    )
    release_date: Optional[str] = Field(
        None, description="The release date, preferably in YYYY-MM-DD format."
    )
    display: Optional[str] = Field(
        None, description="Description of the display, e.g., '6.7-inch OLED, 120Hz'."
    )
    battery_mah: Optional[int] = Field(
        None,
        description="Battery capacity in milliampere-hours (mAh), just the number.",
    )
    ram_gb: Optional[int] = Field(
        None, description="RAM size in gigabytes (GB), just the number."
    )
    storage_gb: Optional[int] = Field(
        None, description="Internal storage size in gigabytes (GB), just the number."
    )
    camera_specs: Optional[str] = Field(
        None,
        description="Description of the camera system, e.g., '50MP Main, 12MP Ultrawide'.",
    )
    price_cents: Optional[int] = Field(
        None,
        description="Price in the Bangladesh taka currency(bdt) unit . Convert it to bdt if needed.",
    )


class DeviceQuerySchema(BaseModel):
    """Input schema for the execute_device_query tool."""

    where_clause: str = Field(
        ...,
        description=(
            "A valid SQL WHERE clause to filter devices based on their attributes. "
            "Example: \"ram_gb >= 8 AND release_date > '2023-01-01'\""
        ),
    )
class AskRequest(BaseModel):
    question: str