from typing import Any

from pydantic import BaseModel, Field


class Response(BaseModel):
    status: str = Field(..., description="Response status code (success, error)")
    message: str = Field(..., description="Descriptive message about response")
    data: Any | None = Field(None, description="Response data (payload)")
