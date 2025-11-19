"""Stream type classes for tap-leaflink."""

from __future__ import annotations

from importlib import resources

from singer_sdk import OpenAPISchema, StreamSchema

from tap_leaflink import openapi
from tap_leaflink.client import LeafLinkStream

__all__ = [
    "BatchesStream",
    "BrandsStream",
    "BuyerOrdersStream",
    "CompaniesStream",
    "CompanyStaffStream",
    "ContactsStream",
    "CustomersStream",
    "InventoryItemsStream",
    "LicenseTypesStream",
    "LicensesStream",
    "LineItemsStream",
    "OrderEventLogsStream",
    "OrderPaymentsStream",
    "OrderSalesRepsStream",
    "OrdersReceivedStream",
    "ProductCategoriesStream",
    "ProductsStream",
]


OPENAPI_SPEC = OpenAPISchema(source=resources.files(openapi) / "openapi.json")


class OrdersReceivedStream(LeafLinkStream):
    """Orders received stream.

    Retrieve orders from the seller's perspective.
    """

    name = "orders_received"
    path = "/orders-received/"
    primary_keys = ("number",)
    replication_key = "modified"

    schema = StreamSchema(OPENAPI_SPEC, key="OrderResponse")


class OrderPaymentsStream(LeafLinkStream):
    """Order payments stream."""

    name = "order_payments"
    path = "/order-payments/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="OrderPaymentResponse")


class LineItemsStream(LeafLinkStream):
    """Line items stream."""

    name = "line_items"
    path = "/line-items/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="LineItemResponse")


class CustomersStream(LeafLinkStream):
    """Customers stream."""

    name = "customers"
    path = "/customers/"
    primary_keys = ("id",)
    replication_key = "modified"

    schema = StreamSchema(OPENAPI_SPEC, key="CustomerResponse")


class ProductsStream(LeafLinkStream):
    """Products stream."""

    name = "products"
    path = "/products/"
    primary_keys = ("id",)
    replication_key = "modified"

    schema = StreamSchema(OPENAPI_SPEC, key="ProductResponse")


class BatchesStream(LeafLinkStream):
    """Batches/Inventory stream."""

    name = "batches"
    path = "/batches/"
    primary_keys = ("id",)
    replication_key = "modified"

    schema = StreamSchema(OPENAPI_SPEC, key="BatchResponse")


class CompaniesStream(LeafLinkStream):
    """Companies stream."""

    name = "companies"
    path = "/companies/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="CompanyResponse")


class BrandsStream(LeafLinkStream):
    """Brands stream."""

    name = "brands"
    path = "/brands/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="BrandResponse")


class LicensesStream(LeafLinkStream):
    """Licenses stream."""

    name = "licenses"
    path = "/licenses/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="ComplianceLicense")


class LicenseTypesStream(LeafLinkStream):
    """License types stream."""

    name = "license_types"
    path = "/license-types/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="LicenseType")


class BuyerOrdersStream(LeafLinkStream):
    """Buyer orders stream.

    Retrieve orders from the buyer's perspective.
    """

    name = "buyer_orders"
    path = "/buyer/orders/"
    primary_keys = ("id",)
    replication_key = "modified"

    schema = StreamSchema(OPENAPI_SPEC, key="BuyerOrderResponse")


class OrderEventLogsStream(LeafLinkStream):
    """Order event logs stream.

    Track order state changes and events.
    """

    name = "order_event_logs"
    path = "/order-event-logs/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="OrderEventLog")


class OrderSalesRepsStream(LeafLinkStream):
    """Order sales representatives stream."""

    name = "order_sales_reps"
    path = "/order-sales-reps/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="OrderSalesRepSerialzer")


class InventoryItemsStream(LeafLinkStream):
    """Inventory items stream."""

    name = "inventory_items"
    path = "/inventory/items/"
    primary_keys = ("id",)
    replication_key = "modified"

    schema = StreamSchema(OPENAPI_SPEC, key="InventoryItem")


class ProductCategoriesStream(LeafLinkStream):
    """Product categories stream."""

    name = "product_categories"
    path = "/product-categories/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="ProductCategoryResponse")


class ContactsStream(LeafLinkStream):
    """Contacts stream."""

    name = "contacts"
    path = "/contacts/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="Contact")


class CompanyStaffStream(LeafLinkStream):
    """Company staff stream."""

    name = "company_staff"
    path = "/company-staff/"
    primary_keys = ("id",)
    replication_key = None

    schema = StreamSchema(OPENAPI_SPEC, key="CompanyStaffResponse")
