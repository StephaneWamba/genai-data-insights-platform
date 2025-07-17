from pydantic import BaseModel, Field, validator
from typing import Optional


class QueryText(BaseModel):
    """Value object for natural language query text"""

    value: str = Field(..., min_length=1, max_length=1000)

    @validator('value')
    def validate_query_text(cls, v):
        """Validate query text meets basic requirements"""
        if not v or not v.strip():
            raise ValueError("Query text cannot be empty")

        return v.strip()

    def __str__(self) -> str:
        return self.value

    def __len__(self) -> int:
        return len(self.value)
