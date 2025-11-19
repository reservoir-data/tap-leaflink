"""REST client handling, including LeafLinkStream base class."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qs, urlparse

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.pagination import BaseHATEOASPaginator
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class LeafLinkPaginator(BaseHATEOASPaginator):
    """LeafLink API HATEOAS paginator.

    LeafLink uses HATEOAS pagination with a 'next' URL in the response.
    """

    @override
    def get_next_url(self, response: requests.Response) -> str | None:
        data = response.json()
        return data.get("next")


class LeafLinkStream(RESTStream):
    """LeafLink stream class."""

    # LeafLink returns results in a 'results' array
    records_jsonpath = "$.results[*]"

    # Page size for pagination
    page_size = 100

    @override
    @property
    def url_base(self) -> str:
        """The API URL root, configurable via tap settings."""
        base_url = self.config.get("api_url", "https://app.leaflink.com")
        # Ensure URL ends without trailing slash (we add it in paths)
        return base_url.rstrip("/")

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        return APIKeyAuthenticator(
            key="Authorization",
            value=f"App {self.config['api_key']}",
            location="header",
        )

    @override
    def get_new_paginator(self) -> LeafLinkPaginator:
        return LeafLinkPaginator()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "limit": self.page_size,
        }

        if next_page_token:
            url = urlparse(next_page_token)
            params |= parse_qs(url.query)

        if (
            self.replication_key  # Stream supports incremental replication
            and (start_date := self.get_starting_replication_key_value(context))
        ):
            # LeafLink uses modified__gte for filtering by modification date
            params[f"{self.replication_key}__gte"] = start_date

        return params
