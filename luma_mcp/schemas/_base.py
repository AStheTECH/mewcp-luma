from typing import Any

from pydantic import BaseModel

class ToolError(BaseModel):
    code: str
    message: str
    details: Any = None

class ToolResult(BaseModel):
    success: bool
    statusCode: int
    retriable: bool = False
    retry_after_seconds: int | None = None
    error: ToolError | None = None
