# claisen‑symptom‑logger (Python CLI)

### ➤ Description  
A minimal command‑line tool to record, view and export daily gastrointestinal symptom logs (bloating, gas, heartburn) into JSON or CSV files.

### ➤ Key Features  
- **`claisen-log init`**  
  Initialise a local symptom database (creates `~/.claisen/data.db`).
- **`claisen-log add --symptoms gas,bloating --severity 3`**  
  Append a timestamped entry (validates fields with Pydantic).  
- **`claisen-log show [--last 7]`**  
  Display the last N days in a colourised table.  
- **`claisen-log export --format csv --out ~/symptoms.csv`**  
  Dump all data to CSV or JSON.

