"""LeafLink tap class."""

from __future__ import annotations

from typing import override

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_leaflink import streams


class TapLeafLink(Tap):
    """Singer tap for LeafLink."""

    name = "tap-leaflink"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,
            description="LeafLink API key for authentication (App or User token)",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://app.leaflink.com/api/v2",
            description=(
                "LeafLink API base URL. Use https://app.leaflink.com/api/v2 for "
                "production, https://www.sandbox.leaflink.com/api/v2 for sandbox, or "
                "https://www.leaflink-integrations.leaflink.com/api/v2 for "
                "integrations sandbox."
            ),
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description=(
                "The earliest record date to sync. Used for incremental replication "
                "on streams that support it."
            ),
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.LeafLinkStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            # Orders & Payments
            streams.OrdersReceivedStream(self),
            streams.BuyerOrdersStream(self),
            streams.OrderPaymentsStream(self),
            streams.OrderEventLogsStream(self),
            streams.OrderSalesRepsStream(self),
            streams.LineItemsStream(self),
            # Products & Inventory
            streams.ProductsStream(self),
            streams.ProductCategoriesStream(self),
            streams.BatchesStream(self),
            streams.InventoryItemsStream(self),
            # Customers & Contacts
            streams.CustomersStream(self),
            streams.ContactsStream(self),
            # Companies & Staff
            streams.CompaniesStream(self),
            streams.CompanyStaffStream(self),
            streams.BrandsStream(self),
            # Compliance
            streams.LicensesStream(self),
            streams.LicenseTypesStream(self),
        ]


if __name__ == "__main__":
    TapLeafLink.cli()
