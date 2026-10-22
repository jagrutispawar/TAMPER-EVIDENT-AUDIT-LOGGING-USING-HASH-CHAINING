# Tamper-Evident Audit Logging Using Hash Chaining

**Subject:** Cryptography & Information Security (CIS)  
**Application:** Python + Streamlit  
**Hash algorithm:** SHA-256  
**Storage:** Local JSON file

## Included files
- `app.py` — runnable application
- `requirements.txt` — Python dependency
- `architecture.md` — architecture and design documentation
- `project_report.md` — project report draft
- `test_plan.md` — test plan and expected outcomes
- `tests/test_audit_chain.py` — automated tests
- `viva_questions.md` — viva preparation
- `run_windows.bat` — Windows setup/run helper

## Requirements
- Python 3.10 or newer
- Internet access for installing Streamlit the first time
- VS Code or another terminal

## Run on Windows / VS Code
1. Extract the ZIP.
2. Open the extracted folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment (recommended):
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```
5. Install requirements:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Run:
   ```powershell
   python -m streamlit run app.py
   ```
7. Open the local address shown in the terminal if the browser does not open automatically.

## Demonstration sequence
1. In **Add Audit Event**, add a login event.
2. Add a second event such as `File Updated`.
3. Open **Verify Integrity** and click **Run Verification Now**; expect `VALID`.
4. Under **Controlled tampering demonstration**, choose an entry and click **Tamper with selected entry**.
5. Verify again; expect `TAMPERING FOUND`.
6. Explain that the stored hash no longer matches the calculated hash. The following record's previous-hash link may also fail.
7. Download the JSON records if required.

## Run automated tests
Install pytest:
```powershell
python -m pip install pytest
python -m pytest -v
```
The test suite uses Python's standard library plus pytest. It tests valid chains, altered content, broken links, and empty logs.

## Important
This is an educational prototype, not a production-grade immutable logging service. Review your assigned Project Selection (PS) Code and any additional faculty requirements before final submission. Do not claim security features that are not implemented.
