from __future__ import annotations

from time import monotonic
from typing import Any


class MemoryCache:

    def __init__(self, ttl_seconds: float = 300.0) -> None:
        self._ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[float | None, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None

        expires_at, value = entry
        if expires_at is not None and monotonic() >= expires_at:
            del self._store[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        expires_at = None
        if self._ttl_seconds > 0:
            expires_at = monotonic() + self._ttl_seconds
        self._store[key] = (expires_at, value)

    def clear(self) -> None:
        self._store.clear()
