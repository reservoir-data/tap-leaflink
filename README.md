# tap-leaflink

`tap-leaflink` is a Singer tap for the LeafLink Marketplace V2 API.

Built with the [Meltano Singer SDK](https://sdk.meltano.com) for Singer Taps.

## Features

- **17 Comprehensive Streams**: Complete coverage of orders, products, inventory, customers, and compliance data
- **Incremental Replication**: 6 streams support incremental syncs using modification timestamps
- **OpenAPI-Driven Schemas**: Automatically generated from the official LeafLink OpenAPI specification
- **HATEOAS Pagination**: Handles LeafLink's HATEOAS pagination automatically
- **Token Authentication**: Supports both App and User API tokens
- **Multiple Environments**: Production, sandbox, and integrations sandbox
- **Auto-Updated OpenAPI Spec**: Daily workflow keeps the API specification current

## Installation

```bash
# Install from GitHub
uv tool install git+https://github.com/reservoir-data/tap-leaflink.git@main
```

## Configuration

### Required Settings

- **api_key** (required): Your LeafLink API key (App or User token)
  - Get your API key from the LeafLink platform
  - Format: `Authorization: App {api_key}`

### Optional Settings

- **api_url** (default: `https://app.leaflink.com/api/v2`): API base URL
  - Production: `https://app.leaflink.com/api/v2`
  - Sandbox: `https://www.sandbox.leaflink.com/api/v2`
  - Integrations: `https://www.leaflink-integrations.leaflink.com/api/v2`
- **start_date**: Earliest record date for incremental replication
- **page_size** (default: 100): Records per page

### Example Configuration

Create a `config.json` file:

```json
{
  "api_key": "your_api_key_here",
  "api_url": "https://app.leaflink.com/api/v2",
  "start_date": "2024-01-01T00:00:00Z",
  "page_size": 100
}
```

### Authentication

LeafLink uses API key authentication with two token types:

1. **User Token**: Access to all companies where the user has permissions
2. **App Token**: Access to a single company (recommended for integrations)

The API enforces rate limiting:
- Standard: 300 requests/minute
- Burst: 1000 requests/minute
- Violations return `429 Too Many Requests`

See [LeafLink API Authorization](https://developer.leaflink.com/legacy/v2/api/authorization/) for details.

## Available Streams

### Orders & Payments (6 streams)

| Stream | Primary Key | Replication | Description |
|--------|-------------|-------------|-------------|
| `orders_received` | `number` | ✓ `modified` | Seller-side orders |
| `buyer_orders` | `id` | ✓ `modified` | Buyer-side orders |
| `order_payments` | `id` | - | Order payment records |
| `order_event_logs` | `id` | - | Order state changes and events |
| `order_sales_reps` | `id` | - | Sales representatives |
| `line_items` | `id` | - | Order line items |

### Products & Inventory (4 streams)

| Stream | Primary Key | Replication | Description |
|--------|-------------|-------------|-------------|
| `products` | `id` | ✓ `modified` | Product catalog |
| `product_categories` | `id` | - | Product categories |
| `batches` | `id` | ✓ `modified` | Product batches |
| `inventory_items` | `id` | ✓ `modified` | Inventory tracking |

### Customers & Contacts (2 streams)

| Stream | Primary Key | Replication | Description |
|--------|-------------|-------------|-------------|
| `customers` | `id` | ✓ `modified` | Customer accounts |
| `contacts` | `id` | - | Contact information |

### Companies & Staff (3 streams)

| Stream | Primary Key | Replication | Description |
|--------|-------------|-------------|-------------|
| `companies` | `id` | - | Company information |
| `company_staff` | `id` | - | Company staff/employees |
| `brands` | `id` | - | Brand catalog |

### Compliance (2 streams)

| Stream | Primary Key | Replication | Description |
|--------|-------------|-------------|-------------|
| `licenses` | `id` | - | License records |
| `license_types` | `id` | - | License types |

**Total: 17 streams** | **6 with incremental replication**

## Usage

### Discover Streams

```bash
tap-leaflink --config config.json --discover > catalog.json
```

### Sync Data

```bash
tap-leaflink --config config.json --catalog catalog.json
```

### Using with Meltano

Add to your `meltano.yml`:

```yaml
plugins:
  extractors:
    - name: tap-leaflink
      namespace: tap_leaflink
      pip_url: -e .
      config:
        api_key: ${TAP_LEAFLINK_API_KEY}
      select:
        - orders_received.*
        - buyer_orders.*
        - order_payments.*
        - line_items.*
        - customers.*
        - products.*
        - inventory_items.*
```

Run with Meltano:

```bash
meltano run tap-leaflink target-jsonl
```

## Development

### Setup

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --all-extras
```

### OpenAPI Spec Management

All stream schemas are automatically generated from the LeafLink OpenAPI specification:

```bash
# Download latest spec
uv run --group scrape python scripts/scrape_openapi_spec.py

# Spec is saved to: tap_leaflink/openapi/openapi.json
```

A GitHub Actions workflow automatically checks for spec updates daily and creates PRs when changes are detected. This ensures schemas stay in sync with the LeafLink API.

### Testing

```bash
# Run tests and code quality checks
uvx --with=tox-uv tox run-parallel
```

## Important API Notes

⚠️ **All API paths must end with a trailing slash (`/`)** - Requests without it return `400 Bad Request`

✅ Good: `/orders-received/`
❌ Bad: `/orders-received`

The tap handles this automatically for all streams.

## Resources

- [LeafLink API Documentation](https://developer.leaflink.com/legacy/v2/api/ref/)
- [LeafLink Authorization Guide](https://developer.leaflink.com/legacy/v2/api/authorization/)
- [Meltano Singer SDK](https://sdk.meltano.com)
- [Singer Specification](https://hub.meltano.com/singer/spec/)

## License

Apache 2.0
