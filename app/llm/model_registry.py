"""
Model version registry.

Loads model metadata from model_versions/registry.yaml.
Enables versioned rollback, A/B testing, and audit trail.
Each reflection response includes the model_version for traceability.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ModelVersion:
    """A registered model version."""

    version_id: str
    model_name: str
    provider: str
    checkpoint_path: Optional[str]
    description: str
    is_active: bool


class ModelRegistry:
    """
    Manages model version lifecycle.

    Reads from a YAML manifest and provides lookup/activation methods.
    """

    def __init__(self, registry_path: str = "model_versions/registry.yaml"):
        """
        Args:
            registry_path: Path to the YAML model version manifest.
        """
        self._registry_path = registry_path
        self._versions: List[ModelVersion] = []

    def load(self) -> None:
        """Parse the YAML file and populate the versions list."""
        ...

    def get_active_model(self) -> ModelVersion:
        """
        Return the currently active model version.

        Raises:
            ValueError: If no active model is found.
        """
        ...

    def list_versions(self) -> List[ModelVersion]:
        """List all registered model versions."""
        ...

    def activate_version(self, version_id: str) -> None:
        """
        Set a specific version as the active model.
        Deactivates all other versions.

        Args:
            version_id: ID of the version to activate.

        Raises:
            ValueError: If version_id is not found.
        """
        ...
