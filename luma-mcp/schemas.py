from typing import Optional
from typing import TypedDict


class LumaGenerationAssets(TypedDict, total=False):
    video: Optional[str]


class LumaGeneration(TypedDict, total=False):
    id: str
    state: str          # queued | dreaming | completed | failed
    prompt: Optional[str]
    created_at: str
    assets: Optional[LumaGenerationAssets]
    failure_reason: Optional[str]
    model: Optional[str]


class LumaGenerationListResponse(TypedDict):
    generations: list[LumaGeneration]
    has_more: bool
    total_count: int


class LumaCameraMotion(TypedDict):
    id: str
    description: str


class LumaCreateResponse(TypedDict):
    id: str
    state: str
    prompt: Optional[str]
    created_at: str
