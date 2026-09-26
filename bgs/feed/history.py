"""Feed timeline built from the stream."""

from __future__ import annotations

from typing import Any, Iterable

from ..store.records import Record

BATCH_KIND = "feed.batch"
OPEN_KIND = "feed.open"


def batch_timeline(records: Iterable[Record]) -> list[dict[str, Any]]:
    """Turn the feed records into a timeline the console can list.

    Every entry carries the batch identifier, quantity and generation read
    straight from the durable record, so the timeline can be reconciled with
    the batch registry without guessing from the surrounding state.
    """

    timeline: list[dict[str, Any]] = []
    for record in records:
        if record.kind not in (BATCH_KIND, OPEN_KIND):
            continue
        payload = record.payload
        entry: dict[str, Any] = {
            "seq": record.seq,
            "kind": record.kind,
            "tick": record.tick,
            "generation": record.generation,
            "batch_id": payload.get("batch_id"),
        }
        if record.kind == BATCH_KIND:
            entry["quantity"] = payload.get("quantity")
            entry["unit"] = payload.get("unit")
        timeline.append(entry)
    return timeline
