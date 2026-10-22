import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Importing app.py would start Streamlit UI, so these small pure-function
# equivalents keep the unit tests independent of the UI.
GENESIS_HASH = "0" * 64


def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def calculate_hash(record_without_hash):
    return hashlib.sha256(canonical_json(record_without_hash).encode("utf-8")).hexdigest()


def make_record(record_id, previous_hash, details="Sample event", event_id=None):
    record = {
        "id": record_id,
        "event_id": event_id or f"event-{record_id}",
        "timestamp_utc": "2026-01-01T00:00:00+00:00",
        "username": "student01",
        "action": "User Login",
        "details": details,
        "previous_hash": previous_hash,
    }
    record["entry_hash"] = calculate_hash(record)
    return record


def verify_logs(logs):
    previous_hash = GENESIS_HASH
    seen = set()
    required = {"id", "event_id", "timestamp_utc", "username", "action",
                "details", "previous_hash", "entry_hash"}
    for index, record in enumerate(logs):
        if not isinstance(record, dict) or not required.issubset(record):
            return False
        if record["id"] != index + 1 or record["event_id"] in seen:
            return False
        seen.add(record["event_id"])
        if record["previous_hash"] != previous_hash:
            return False
        body = {k: v for k, v in record.items() if k != "entry_hash"}
        if calculate_hash(body) != record["entry_hash"]:
            return False
        previous_hash = record["entry_hash"]
    return True


def valid_chain():
    first = make_record(1, GENESIS_HASH, "First event")
    second = make_record(2, first["entry_hash"], "Second event")
    return [first, second]


def test_empty_chain_is_valid():
    assert verify_logs([])


def test_unchanged_chain_is_valid():
    assert verify_logs(valid_chain())


def test_changed_content_is_detected():
    chain = valid_chain()
    chain[0]["details"] = "Altered event"
    assert not verify_logs(chain)


def test_broken_previous_hash_is_detected():
    chain = valid_chain()
    chain[1]["previous_hash"] = "f" * 64
    assert not verify_logs(chain)


def test_missing_field_is_detected():
    chain = valid_chain()
    del chain[0]["username"]
    assert not verify_logs(chain)


def test_duplicate_event_id_is_detected():
    chain = valid_chain()
    chain[1]["event_id"] = chain[0]["event_id"]
    chain[1]["entry_hash"] = calculate_hash(
        {k: v for k, v in chain[1].items() if k != "entry_hash"}
    )
    assert not verify_logs(chain)


def test_inconsistent_record_id_is_detected():
    chain = valid_chain()
    chain[1]["id"] = 7
    chain[1]["entry_hash"] = calculate_hash(
        {k: v for k, v in chain[1].items() if k != "entry_hash"}
    )
    assert not verify_logs(chain)
