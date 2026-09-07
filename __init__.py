"""Lightweight shared planning and safety primitives for Mac package migration."""

__version__ = "0.3.1"

from .core import (
    AUTOMATIC,
    REVIEW,
    Candidate,
    Identity,
    candidates_for,
    choose_candidate,
    dry_run,
    install_allowed,
    load_snapshot,
    plan_record,
)

__all__ = [
    "AUTOMATIC", "REVIEW", "Candidate", "Identity", "candidates_for",
    "choose_candidate", "dry_run", "install_allowed", "load_snapshot",
    "plan_record",
]
