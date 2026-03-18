"""
Analytics dashboard placeholder.

This module provides the integration point for a future analytics dashboard.
Current implementation is a no-op passthrough that can be replaced with
a real implementation without changing any calling code.

Planned capabilities:
- Prompt quality scoring over time
- Framework usage distribution
- Average reflection depth metrics
- Response latency percentiles (p50, p95, p99)
- Cache hit rates
- Model version comparison (A/B testing results)
- Per-activity reflection frequency
"""


class AnalyticsCollector:
    """
    No-op analytics collector.

    Replace with a real implementation backed by:
    - Grafana + Prometheus for metrics
    - Custom dashboard reading from SQLiteStore/PostgreSQL
    - Third-party analytics (PostHog, Mixpanel)
    """

    async def record_event(self, event_type: str, data: dict) -> None:
        """
        Record an analytics event.

        Args:
            event_type: Event category (e.g. "reflection_generated", "feedback_received").
            data: Event payload with relevant fields.
        """
        pass

    async def get_summary(self) -> dict:
        """
        Return a summary of analytics data.

        Returns:
            Dict with aggregated metrics.
        """
        return {"status": "not_implemented"}
