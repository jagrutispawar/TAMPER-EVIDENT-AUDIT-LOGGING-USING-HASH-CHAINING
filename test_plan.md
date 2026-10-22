# Test Plan and Test Cases

## Purpose
Validate that the audit chain accepts unchanged records and detects common record changes.

## Test cases

| ID | Test | Expected result |
|---|---|---|
| TC-01 | Verify an empty list | Valid |
| TC-02 | Verify one correctly hashed record | Valid |
| TC-03 | Verify multiple correctly linked records | Valid |
| TC-04 | Change `details` without recalculating `entry_hash` | Invalid content hash |
| TC-05 | Change `previous_hash` | Invalid chain link |
| TC-06 | Remove a required field | Invalid record structure |
| TC-07 | Duplicate an `event_id` | Duplicate event ID detected |
| TC-08 | Change a record ID sequence | Record ID sequence inconsistent |

## Running the tests
1. Install the application requirements:
   `python -m pip install -r requirements.txt`
2. Install pytest:
   `python -m pip install pytest`
3. Run:
   `python -m pytest -v`

## Results
Record the actual test output after running the tests. Do not mark a test as passed unless it has actually passed in your environment.
