import datetime
from typing import Optional

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel


class Device(SQLModel, table=True):
    """Represents a mobile device or gadget with its key specifications."""

    __tablename__ = "devices"  # type: ignore
    model_name: str = Field(
        sa_column=Column(
            "model_name", String, primary_key=True, index=True, nullable=False
        )
    )
    release_date: Optional[datetime.date] = Field(
        default=None, description="The official release date of the device."
    )

    display: str = Field(
        description="Description of the display, e.g., '6.7-inch OLED, 120Hz'",
        max_length=255,
    )
    battery_mah: int = Field(
        ge=0, description="Battery capacity in milliampere-hours (mAh)."
    )
    ram_gb: int = Field(ge=0, description="RAM size in gigabytes (GB).")
    storage_gb: int = Field(
        ge=0, description="Internal storage size in gigabytes (GB)."
    )
    camera_specs: str = Field(
        description="Description of the camera system, e.g., '50MP Main, 12MP Ultrawide'",
        max_length=255,
    )
    price_cents: Optional[int] = Field(
        default=None,
        ge=0,
        description="Price in the smallest currency unit (e.g., cents).",
    )
