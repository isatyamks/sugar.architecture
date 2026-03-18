"""
Model registry seeder.

Reads model_versions/registry.yaml and validates the manifest.
Can be extended to download model weights or warm up providers.

Usage:
    python scripts/seed_models.py
"""

import yaml
import sys
from pathlib import Path


def seed() -> None:
    """
    Validate and display the model registry.

    Steps:
    1. Load registry.yaml
    2. Validate required fields per entry
    3. Print summary
    4. Optionally verify checkpoint paths exist on disk
    """
    registry_path = Path(__file__).parent.parent / "model_versions" / "registry.yaml"

    if not registry_path.exists():
        print(f"ERROR: Registry not found at {registry_path}")
        sys.exit(1)

    with open(registry_path) as f:
        data = yaml.safe_load(f)

    models = data.get("models", [])
    print(f"Found {len(models)} model version(s):\n")

    for m in models:
        active = "✓ ACTIVE" if m.get("is_active") else "  inactive"
        print(f"  [{active}] {m['version_id']} — {m['model_name']} ({m['provider']})")
        print(f"           {m['description']}")
        print()


if __name__ == "__main__":
    seed()
