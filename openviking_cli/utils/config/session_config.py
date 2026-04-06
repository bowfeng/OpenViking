# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: AGPL-3.0
from typing import Any, Dict

from pydantic import BaseModel, Field, field_validator


class SessionConfig(BaseModel):
    """Session configuration for OpenViking."""

    archive_wait_timeout: float = Field(
        default=600.0,
        description="Maximum time to wait for previous archive to complete before timing out. "
        "Used during session commit to wait for Phase 2 (memory extraction) of the previous archive. "
        "If the previous archive hasn't completed within this time, it's treated as failed. "
        "Can be overridden by environment variable ARCHIVE_WAIT_TIMEOUT_SECONDS.",
    )

    model_config = {"extra": "forbid"}

    @field_validator("archive_wait_timeout")
    @classmethod
    def validate_archive_wait_timeout(cls, value: float) -> float:
        """Validate archive_wait_timeout is positive."""
        if value <= 0:
            raise ValueError("archive_wait_timeout must be a positive number (in seconds)")
        return value

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "SessionConfig":
        """Create configuration from dictionary."""
        return cls(**config)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.model_dump()