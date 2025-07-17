from pydantic import BaseModel, Field, validator
from typing import Optional


class ConfidenceScore(BaseModel):
    """Value object for AI confidence scores"""

    value: float = Field(..., ge=0.0, le=1.0)

    @validator('value')
    def validate_confidence_score(cls, v):
        """Validate confidence score is within business acceptable range"""
        if v < 0.0 or v > 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")

        # Business rule: minimum confidence for actionable insights
        if v < 0.3:
            raise ValueError(
                "Confidence score too low for actionable insights")

        return round(v, 2)

    def is_high_confidence(self) -> bool:
        """Check if confidence is high enough for strong recommendations"""
        return self.value >= 0.8

    def is_medium_confidence(self) -> bool:
        """Check if confidence is medium for general insights"""
        return 0.5 <= self.value < 0.8

    def is_low_confidence(self) -> bool:
        """Check if confidence is low (but still actionable)"""
        return 0.3 <= self.value < 0.5

    def __str__(self) -> str:
        return f"{self.value:.2f}"
