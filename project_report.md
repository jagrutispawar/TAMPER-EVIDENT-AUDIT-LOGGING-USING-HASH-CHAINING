# PROJECT REPORT
## Tamper-Evident Audit Logging Using Hash Chaining

**Subject:** Cryptography & Information Security (CIS)  
**Student Name:** ____________________  
**Roll Number:** ____________________  
**Class / Division:** TY ____________________  
**Project Selection (PS) Code:** ____________________  
**Academic Year:** ____________________

---

## Abstract
Audit logs record important system activities and support troubleshooting, accountability, and security review. However, stored log records can be modified or deleted by a person with file access. This project demonstrates a tamper-evident logging approach using SHA-256 hashing and hash chaining. Each record contains event information, the previous record's hash, and its own calculated hash. During verification, the application recalculates hashes and checks chain links. Unexpected changes cause integrity verification to fail. The prototype is implemented in Python with a Streamlit interface and stores records in a local JSON file. It is intended for educational demonstration and does not claim to provide production-grade immutable storage.

## 1. Introduction
Audit logging is an important security practice because it records events such as logins, failed logins, file changes, and configuration updates. Logs are useful only when their integrity can be assessed. A simple editable log file may be changed without leaving an obvious sign. Hash chaining links records cryptographically so that a change to a record can be detected when the trusted chain is checked.

## 2. Problem Statement
How can a small audit logging application detect unexpected modifications to stored log records using cryptographic hashes without requiring a blockchain or a complex external service?

## 3. Objectives
1. Record sample audit events with timestamps and user labels.
2. Calculate a SHA-256 hash for every record.
3. Link each record to the preceding record through `previous_hash`.
4. Verify record content hashes and chain links.
5. Demonstrate tampering detection in a controlled environment.
6. Provide a simple interface to view and export records.
7. Document the architecture, tests, and limitations.

## 4. Scope
The prototype supports local event entry, SHA-256 hashing, sequential hash chaining, verification, a classroom tampering demonstration, table display, and JSON export. It is not intended for production security monitoring.

## 5. Existing System and Proposed System
### Existing/simple approach
A conventional plain-text or JSON log can be edited without automatic integrity checks. The application may not know that stored content has changed.

### Proposed approach
The application calculates a hash for each record and stores the previous record's hash. Verification recalculates hashes and validates links to detect changed content or broken chain references.

## 6. Technologies Used
- Python 3.10+
- Streamlit for the user interface
- SHA-256 via Python `hashlib`
- JSON for local storage
- UUID for event identifiers
- UTC ISO 8601 timestamps
- pytest for automated tests

## 7. Methodology
1. The user enters a username, action, and event details.
2. The application validates required fields.
3. It assigns a sequential record ID, UUID, and UTC timestamp.
4. It sets `previous_hash` to the previous record's hash, or the genesis hash for the first record.
5. It serializes record fields consistently and calculates SHA-256.
6. It stores the record in `audit_log.json`.
7. Verification recalculates each record hash and checks its previous-hash link.
8. A mismatch is reported as an integrity failure.

## 8. System Architecture
See `architecture.md` for the architecture diagram, record schema, workflow, verification rules, and limitations.

## 9. Implementation
The main application is in `app.py`. `calculate_hash()` calculates SHA-256 over canonical JSON. `add_log()` constructs and stores a linked record. `verify_logs()` validates required fields, record sequence, event ID uniqueness, previous-hash links, and content hashes. Streamlit provides event entry, verification, record display, export, and controlled tampering demonstration.

## 10. Testing and Expected Results
See `test_plan.md`. Expected tests include a valid chain, empty chain, changed record content, broken previous-hash link, and a duplicate event ID. In the UI, an unchanged log should display `VALID`; after the controlled tampering demonstration, verification should display `TAMPERING FOUND`.

**Actual results:** Fill this section after running the application and tests. Do not report tests as passed unless you have run them.

## 11. Advantages
- Simple and understandable demonstration of cryptographic integrity checks.
- Each record is linked to the preceding record.
- Detects ordinary edits and broken links during verification.
- Uses common Python libraries and local storage.
- Supports classroom demonstration and JSON export.

## 12. Limitations
- Local JSON storage can be rewritten by someone with sufficient access.
- Hash chaining alone does not prove who created a record.
- No login authentication, role-based access, or trusted external timestamp is implemented.
- An attacker able to rewrite every record and all hashes may recreate a valid chain unless a trusted external checkpoint exists.
- This prototype does not replace a hardened centralized logging system.

## 13. Future Enhancements
- Authentication and role-based authorization.
- Remote append-only storage.
- Digital signatures and separately stored signed checkpoints.
- Alerting on failed integrity verification.
- Database-backed storage and backup policies.
- Log retention policy and access auditing.

## 14. Conclusion
The project demonstrates how SHA-256 and hash chaining can make changes to audit records detectable. Each entry contains its own hash and a link to the preceding entry. Verification checks both content and links, and the controlled demonstration shows how a changed record causes verification to fail. The prototype illustrates a useful integrity concept while identifying additional controls required for production use.

## References
1. Python documentation: `hashlib` — https://docs.python.org/3/library/hashlib.html
2. Python documentation: `json` — https://docs.python.org/3/library/json.html
3. Streamlit documentation — https://docs.streamlit.io/
4. NIST FIPS PUB 180-4, Secure Hash Standard (SHS) — https://csrc.nist.gov/pubs/fips/180-4/upd1/final

---
**Submission note:** Replace the blank student details, add any required college cover page/certificate, and confirm the report structure against your department's template and assigned PS Code.
