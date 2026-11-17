"""
CloudForge Feature Inventory Tracking System

This module implements the feature tracking lifecycle:
  NOT IMPLEMENTED → IMPLEMENTED → TESTED → DOCUMENTED → PRODUCTION VALIDATED

Each feature progresses through these stages, and the system tracks
the status, ownership, and validation of each feature across the project.
"""

from .tracker import FeatureTracker, FeatureStatus
from .models import Feature, FeatureMetadata

__all__ = ["FeatureTracker", "FeatureStatus", "Feature", "FeatureMetadata"]


# Example usage:
# tracker = FeatureTracker()
# feature = tracker.get_feature("api-gateway-jwt-auth")
# print(feature.status)
# tracker.update_status("api-gateway-jwt-auth", FeatureStatus.IMPLEMENTED)
