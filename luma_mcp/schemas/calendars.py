from pydantic import BaseModel, ConfigDict
from ._base import ToolResult


class CalendarLocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    city: str | None = None
    region: str | None = None
    country: str | None = None
    country_code: str | None = None
    timezone: str | None = None


class CalendarCoordinate(BaseModel):
    model_config = ConfigDict(extra="allow")

    longitude: float | None = None
    latitude: float | None = None


class CalendarData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    slug: str | None = None
    avatar_url: str | None = None
    url: str | None = None
    description: str | None = None
    social_image_url: str | None = None
    cover_image_url: str | None = None
    is_personal: bool | None = None
    location: CalendarLocation | None = None
    coordinate: CalendarCoordinate | None = None
    instagram_handle: str | None = None
    twitter_handle: str | None = None
    youtube_handle: str | None = None
    website: str | None = None


class CalendarResult(ToolResult):
    data: CalendarData | None = None
