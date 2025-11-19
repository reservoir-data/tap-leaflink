"""Scrape the LeafLink OpenAPI spec."""  # noqa: INP001

import json
import re
from pathlib import Path

import requests
import rich

DOCS_URL = "https://developer.leaflink.com/legacy/v2/api/ref/"
OUTPUT_DIR = Path("tap_leaflink/openapi_specs")
OUTPUT_FILE = OUTPUT_DIR / "leaflink.json"


def extract_openapi_spec_from_html(html_content: str) -> dict | None:
    """Extract the OpenAPI spec from the HTML content.

    Args:
        html_content: HTML content of the documentation page

    Returns:
        The OpenAPI spec as a dictionary, or None if not found
    """
    # Look for the __redoc_state variable that contains the spec
    pattern = r'const __redoc_state\s*=\s*({.*?"spec".*?});'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        # Try alternative pattern
        pattern = r'"spec":\s*({.*?"openapi".*?})'
        match = re.search(pattern, html_content, re.DOTALL)

    if match:
        try:
            # Parse the JavaScript object
            redoc_state = json.loads(match.group(1))

            # Extract the spec from the __redoc_state object
            if "spec" in redoc_state and "data" in redoc_state["spec"]:
                return redoc_state["spec"]["data"]
            if "openapi" in redoc_state or "swagger" in redoc_state:
                return redoc_state

        except json.JSONDecodeError as e:
            rich.print(f"[red]Failed to parse JSON: {e}[/red]")

    return None


def download_openapi_spec(url: str, output_path: Path) -> None:
    """Download the LeafLink OpenAPI spec.

    Args:
        url: URL to the documentation page
        output_path: Path to save the downloaded spec
    """
    rich.print(f"Downloading page from {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    rich.print("Extracting OpenAPI spec from HTML...")
    spec = extract_openapi_spec_from_html(response.text)

    if spec:
        output_path.write_text(json.dumps(spec, indent=2))
        rich.print(f"[green]✓[/green] Successfully downloaded to {output_path}")

        # Print some basic info about the spec
        rich.print(f"[blue]OpenAPI version: {spec.get('openapi', 'unknown')}[/blue]")
        rich.print(f"[blue]API title: {spec.get('info', {}).get('title', 'unknown')}[/blue]")
        if "paths" in spec:
            rich.print(f"[blue]Number of endpoints: {len(spec['paths'])}[/blue]")
    else:
        rich.print("[red]✗[/red] Could not extract OpenAPI spec from HTML")
        msg = "Could not download OpenAPI spec"
        raise RuntimeError(msg)


def main() -> None:
    """Download the LeafLink OpenAPI spec."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    download_openapi_spec(DOCS_URL, OUTPUT_FILE)


if __name__ == "__main__":
    main()
