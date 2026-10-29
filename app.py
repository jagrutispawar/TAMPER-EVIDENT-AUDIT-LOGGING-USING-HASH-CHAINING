import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
LOG_FILE = APP_DIR / "audit_log.json"
GENESIS_HASH = "0" * 64
ACTIONS = [
    "User Login", "Login Failed", "User Logout", "File Created",
    "File Updated", "File Deleted", "Settings Changed", "Other"
]

st.set_page_config(page_title="Tamper-Evident Audit Logging", page_icon="🔐", layout="wide")


def canonical_json(data):
    """Serialize data consistently so the same record always produces the same hash."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def calculate_hash(record_without_hash):
    payload = canonical_json(record_without_hash).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_logs():
    if not LOG_FILE.exists():
        return []
    try:
        data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("The audit log root must be a JSON list.")
        return data
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        st.error(f"Could not read audit_log.json: {exc}")
        return []


def save_logs(logs):
    temp_file = LOG_FILE.with_suffix(".json.tmp")
    temp_file.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")
    temp_file.replace(LOG_FILE)


def add_log(username, action, details):
    logs = load_logs()
    previous_hash = logs[-1]["entry_hash"] if logs else GENESIS_HASH
    record = {
        "id": len(logs) + 1,
        "event_id": str(uuid.uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "username": username.strip(),
        "action": action,
        "details": details.strip(),
        "previous_hash": previous_hash,
    }
    record["entry_hash"] = calculate_hash(record)
    logs.append(record)
    save_logs(logs)


def verify_logs(logs):
    """Check record structure, each content hash, and every previous-hash link."""
    previous_hash = GENESIS_HASH
    seen_event_ids = set()

    for index, record in enumerate(logs):
        if not isinstance(record, dict):
            return False, index, "Record is not a JSON object."

        required = {
            "id", "event_id", "timestamp_utc", "username",
            "action", "details", "previous_hash", "entry_hash"
        }
        missing = required.difference(record.keys())
        if missing:
            return False, index, "Missing field(s): " + ", ".join(sorted(missing))

        if record["id"] != index + 1:
            return False, index, "Record ID sequence is inconsistent."

        if record["event_id"] in seen_event_ids:
            return False, index, "Duplicate event ID detected."
        seen_event_ids.add(record["event_id"])

        if record["previous_hash"] != previous_hash:
            return False, index, "Previous-hash link does not match."

        body = {key: value for key, value in record.items() if key != "entry_hash"}
        calculated = calculate_hash(body)
        if calculated != record["entry_hash"]:
            return False, index, "Record content does not match its stored SHA-256 hash."

        previous_hash = record["entry_hash"]

    return True, None, "All records passed hash and chain verification."


st.title("🔐 Tamper-Evident Audit Logging Using Hash Chaining")
st.write("Secure Audit Trail • SHA-256 Hash Chaining • Integrity Verification")
st.info(
    "SHA-256 Hash Chaining | Audit Log Integrity Verification"
)
logs = load_logs()
is_valid, bad_index, verify_message = verify_logs(logs)

m1, m2, m3 = st.columns(3)
m1.metric("Total log entries", len(logs))
m2.metric("Integrity status", "VALID" if is_valid else "TAMPERING FOUND")
m3.metric("Hash algorithm", "SHA-256")

tab_add, tab_verify, tab_records, tab_about = st.tabs(
    ["➕ Add Audit Event", "🛡️ Verify Integrity", "📋 View / Export Logs", "ℹ️ How It Works"]
)

with tab_add:
    st.subheader("Create an audit record")
    with st.form("add_event", clear_on_submit=True):
        col1, col2 = st.columns(2)
        username = col1.text_input("Username", placeholder="e.g. student01")
        action = col2.selectbox("Action", ACTIONS)
        details = st.text_area("Event details", placeholder="e.g. Updated report.txt", max_chars=500)
        submitted = st.form_submit_button("Add Log Entry", type="primary")

        if submitted:
            if not username.strip() or not details.strip():
                st.error("Username and event details are required.")
            else:
                current_logs = load_logs()
                ok, _, msg = verify_logs(current_logs)
                if not ok:
                    st.error("Cannot append to an invalid chain. Review or restore the log file first. " + msg)
                else:
                    add_log(username, action, details)
                    st.success("Audit entry added and linked to the previous entry.")
                    st.rerun()

    st.caption("Each new record contains a UTC timestamp, unique event ID, previous hash and its own SHA-256 hash.")

with tab_verify:
    st.subheader("Verify the audit log")
    current_logs = load_logs()
    ok, error_index, msg = verify_logs(current_logs)
    if ok:
        st.success("✅ " + msg)
    else:
        st.error(f"⚠️ {msg} Affected position: {error_index + 1}.")
    if st.button("Run Verification Now", type="primary"):
        st.rerun()

    st.markdown("### Controlled tampering demonstration")
    st.warning("For classroom demonstration only: this changes a record without recalculating its hash. Make a backup before demonstrating.")
    if current_logs:
        labels = [
            f"Entry {record.get('id', idx + 1)} — {record.get('action', 'Unknown')} — {record.get('username', 'Unknown')}"
            for idx, record in enumerate(current_logs)
        ]
        selected = st.selectbox("Choose a record", labels, key="tamper_selection")
        if st.button("Tamper with selected entry"):
            idx = labels.index(selected)
            altered = load_logs()
            altered[idx]["details"] = str(altered[idx].get("details", "")) + " [TAMPERED]"
            save_logs(altered)
            st.error("Record changed without updating its hash. Run verification again to observe detection.")
            st.rerun()
    else:
        st.info("Add at least one audit event before using the tampering demonstration.")

    st.markdown("### Reset demonstration data")
    st.caption("This permanently clears the local demo log. Download a backup first if you need the records.")
    confirm_reset = st.checkbox("I understand that resetting deletes all local demo records.")
    if st.button("Reset All Demo Logs", disabled=not confirm_reset):
        save_logs([])
        st.success("Demo log cleared.")
        st.rerun()

with tab_records:
    st.subheader("Audit records")
    current_logs = load_logs()
    if current_logs:
        st.dataframe(current_logs, use_container_width=True, hide_index=True)
        st.download_button(
            "Download audit_log.json",
            data=json.dumps(current_logs, indent=2, ensure_ascii=False),
            file_name="audit_log.json",
            mime="application/json"
        )
        chain_export = {
            "algorithm": "SHA-256",
            "genesis_hash": GENESIS_HASH,
            "record_count": len(current_logs),
            "verification": verify_logs(current_logs)[2],
            "records": current_logs
        }
        st.download_button(
            "Download verification bundle",
            data=json.dumps(chain_export, indent=2, ensure_ascii=False),
            file_name="audit_verification_bundle.json",
            mime="application/json"
        )
    else:
        st.info("No audit records yet. Add an event in the first tab.")

with tab_about:
    st.subheader("System workflow")
    st.markdown("""
    1. A user submits an audit event.
    2. The application records the event ID, UTC timestamp, username, action and details.
    3. The new record stores the previous record's hash (`previous_hash`).
    4. SHA-256 calculates the current record's `entry_hash`.
    5. Records are saved in `audit_log.json`.
    6. Verification recalculates each hash and checks every previous-hash link.
    7. A changed record or broken link causes verification to fail.
    """)
    st.subheader("Security limitations")
    st.markdown("""
    - Hash chaining makes unauthorized changes detectable when an attacker cannot also replace trusted references.
    - A local file can still be rewritten in full by someone with sufficient access. A production deployment should use restricted permissions, remote append-only storage, signed external checkpoints, monitoring and backups.
    - This prototype does not provide user authentication, access control, trusted third-party timestamps, or a guarantee of who performed an action.
    """)
