"""Feed timeline built from the stream."""

from __future__ import annotations

from typing import Any, Iterable

from ..store.records import Record

BATCH_KIND = "feed.batch"
OPEN_KIND = "feed.open"
FERMENT_KIND = "feed.ferment"
TIMELINE_KINDS = (BATCH_KIND, OPEN_KIND, FERMENT_KIND)


def batch_timeline(records: Iterable[Record]) -> list[dict[str, Any]]:
    """Turn the feed records into a timeline the console can list.

    Every entry keeps the batch identifier, quantity and generation that the
    record itself was written with, so the ledger reconciles against the
    batch registry instead of guessing from the latest state.
    """

    timeline: list[dict[str, Any]] = []
    for record in records:
        if record.kind not in TIMELINE_KINDS:
            continue
        entry: dict[str, Any] = {
            "seq": record.seq,
            "kind": record.kind,
            "tick": record.tick,
            "generation": record.payload.get("generation", record.generation),
            "batch_id": record.payload.get("batch_id"),
        }
        if "quantity" in record.payload:
            entry["quantity"] = record.payload.get("quantity")
            entry["unit"] = record.payload.get("unit")
        if "active" in record.payload:
            entry["active"] = record.payload.get("active")
        timeline.append(entry)
    return timeline
