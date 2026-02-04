"""Shared helpers for services that materialize SWAPI resources."""

from __future__ import annotations

from typing import Any, Dict, Iterable
import asyncio
import json
import requests

from app.infrastructure.cache.memory_cache import MemoryCache


class BaseSwapiService:
    """Minimal helper that performs HTTP requests against the SWAPI."""

    request_timeout_seconds = 5
    cache_ttl_seconds = 300.0
    _cache = MemoryCache(ttl_seconds=cache_ttl_seconds)

    def _build_cache_key(self, url: str, params: Dict[str, Any] | None) -> str:
        if not params:
            return url

        serialized = json.dumps(params, sort_keys=True, default=str)
        return f"{url}?{serialized}"

    def _resolve_payload(self, url: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Fetches and validates a SWAPI resource payload."""

        if not url:
            raise ValueError("A SWAPI URL must be provided to resolve the entity")

        cache_key = self._build_cache_key(url, params)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        response = requests.get(
            url,
            params=params,
            timeout=self.request_timeout_seconds,
        )
        response.raise_for_status()

        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("SWAPI returned a payload that cannot be mapped to an entity")

        self._cache.set(cache_key, payload)

        return payload
    
    # def _resolve_related(
    #     self,
    #     service: BaseSwapiService,
    #     urls: Iterable[str],
    # ) -> list[object]:
    #     return [service.resolve_url(item_url) for item_url in urls]

    async def _resolve_related_async(
        self,
        service: BaseSwapiService,
        urls: Iterable[str],
    ) -> list[object]:
        if not urls:
            return []

        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(None, service.resolve_url, url) for url in urls]
        return await asyncio.gather(*tasks)
