# Architecture Documentation
## Project: Tamper-Evident Audit Logging Using Hash Chaining

### 1. Objective
Build a small audit logging application that detects unauthorized modifications to stored records by using SHA-256 hashes and links between consecutive records.

### 2. High-level architecture

```text
+-----------------------------+
| User / Demonstrator         |
+--------------+--------------+
               |
               v
+-----------------------------+
| Streamlit Web Interface     |
| Add Event | Verify | Export |
+--------------+--------------+
               |
               v
+-----------------------------+
| Audit Logging Engine        |
| - Validate inputs           |
| - Create timestamp/event ID |
| - Link previous hash        |
| - Calculate SHA-256         |
| - Verify records and links  |
+--------------+--------------+
               |
               v
+-----------------------------+
| Local JSON Storage          |
| audit_log.json              |
+--------------+--------------+
               |
               v
+-----------------------------+
| Integrity Verification      |
| VALID / TAMPERING FOUND     |
+-----------------------------+
```

### 3. Technologies
- Python: application logic
- Streamlit: web interface
- `hashlib`: SHA-256 hashing
- `json`: consistent serialization and file storage
- `uuid`: unique event identifiers
- `datetime`: UTC timestamps
- `pytest`: automated tests

### 4. Audit record schema
Each record contains:
- `id`: sequential number in the file
- `event_id`: unique UUID
- `timestamp_utc`: UTC time in ISO 8601 format
- `username`: actor label entered by the demonstrator
- `action`: selected event category
- `details`: event description
- `previous_hash`: previous record's `entry_hash`; all zeroes for the first record
- `entry_hash`: SHA-256 of all the other record fields, serialized consistently

### 5. Hash-chain algorithm
1. Start with a fixed genesis hash consisting of 64 zero characters.
2. For a new event, take the last record's `entry_hash` as `previous_hash`.
3. Serialize all fields other than `entry_hash` using sorted JSON keys and compact separators.
4. Encode the serialized string as UTF-8.
5. Calculate SHA-256 and store the hexadecimal digest as `entry_hash`.
6. During verification, recalculate every entry hash and confirm the `previous_hash` points to the preceding stored hash.

### 6. Verification conditions
The verifier checks required fields, sequential record IDs, unique event IDs, previous-hash linkage, and the content hash. An empty chain is considered valid.

### 7. Data flow
User input → validation → event construction → previous-hash assignment → SHA-256 calculation → JSON storage → verification → status shown to user.

### 8. Threat model and limitations
The system is designed to demonstrate detection of accidental or unauthorized edits to records when trusted prior hashes are preserved. It does not prevent someone with full write access from rewriting all records and hashes. Production-grade deployments should add OS and application access controls, remote append-only storage, signed checkpoints stored separately, alerting, backup and key management.

### 9. Privacy and operational notes
Use sample data for classroom demonstration. Do not enter real passwords, sensitive personal data, or confidential production logs.
