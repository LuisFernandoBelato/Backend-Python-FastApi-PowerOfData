"""Unit tests for main application endpoints."""

import pytest


class TestMainEndpoints:
    """Test suite for main application endpoints."""

    def test_healthcheck_endpoint(self, client):
        """Test the healthcheck endpoint returns ok status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "ok"}

    def test_root_endpoint_not_found(self, client):
        """Test that root endpoint returns 404 if not defined."""
        response = client.get("/")

        # Should return 404 as no root endpoint is defined
        assert response.status_code == 404
