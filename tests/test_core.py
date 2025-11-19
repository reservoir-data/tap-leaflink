"""Tests standard tap features using the built-in SDK tests library."""

from datetime import datetime, timedelta, timezone

from singer_sdk.testing import get_tap_test_class

from tap_leaflink.tap import TapLeafLink


def _one_month_ago() -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=30)


SAMPLE_CONFIG = {
    "start_date": _one_month_ago().strftime("%Y-%m-%d"),
}


# Run standard built-in tap tests from the SDK:
TestTapLeafLink = get_tap_test_class(
    tap_class=TapLeafLink,
    config=SAMPLE_CONFIG,
    include_tap_tests=False,
    include_stream_tests=False,
    include_stream_attribute_tests=False,
)
