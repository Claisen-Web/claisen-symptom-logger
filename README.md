# claisen‑symptom‑logger (Python CLI)

## ➤ Description
A highly advanced command-line tool to record, analyze, and export daily gastrointestinal symptom logs (bloating, gas, heartburn, etc.) with AI/NLP-powered triage, dosing profile assignment, and personalized recommendations.

## ➤ Features
- **AI/NLP-powered triage:** Extracts symptoms, severity, triggers, and urgency from free-text notes using spaCy and a custom classifier.
- **Dosing profile assignment:** Assigns one of five evidence-based GERD management profiles, with subtypes and edge-case logic.
- **Personalized recommendations:** Outputs detailed, actionable, and colorized advice for each profile, including lifestyle, medication, and follow-up.
- **Interactive and non-interactive CLI:** Supports both guided and scripted workflows.
- **Export and follow-up:** Export logs to CSV/JSON and run structured follow-up sessions.

## ➤ Installation
```sh
# Clone the repo
cd /path/to/claisen-symptom-logger
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## ➤ CLI Usage
```sh
# Initialize the database
python claisen_log.py init

# Add a quick entry (interactive or with CLI flags)
python claisen_log.py add --symptoms gas,bloating --severity 3 --notes "Mild after lunch"

# Run advanced AI/NLP triage (interactive)
python claisen_log.py triage

# Run advanced triage with free-text notes (NLP extraction)
python claisen_log.py triage --notes "I have burning pain at night, can't sleep, and feel anxious before bed."

# Non-interactive triage (all answers as JSON or key=value pairs)
python claisen_log.py triage --answers '{"symptom_type": "Burning sensation", "symptom_intensity": "7–8: Severe"}'

# Show recent entries
python claisen_log.py show --last 7

# Export all data
python claisen_log.py export --format csv --out ~/symptoms.csv
```

## ➤ Highly Detailed Example Workflow

### 1. **User runs advanced triage with free-text notes:**
```sh
python claisen_log.py triage --notes "I have burning pain at night, can't sleep, and feel anxious before bed."
```

### 2. **System prompts for any missing structured answers, then runs AI/NLP extraction:**
- **NLP extracts:**
  - Symptoms: burning pain
  - Triggers: night, anxiety
  - Severity: severe
  - Sentiment: urgent (if "can't sleep" or "anxious" is present)
- **Classifier detects urgency** (if language is alarming)

### 3. **Triage engine assigns profile and generates recommendation:**
- **Profile:** 3 (Nocturnal/positional GERD, severe)
- **Reason:** AI/NLP detected severe nocturnal symptoms in notes.
- **Recommendation:**
  - Start omeprazole 20 mg AM + famotidine 10–20 mg at bedtime for 14 days.
  - Elevate head of bed, avoid late meals, and sleep on left side.
  - [cyan]Reassess in 7–14 days. If persistent, escalate to Profile 4.[/cyan]
  - [yellow]Your notes suggest stress/anxiety as a trigger. Consider stress management or psychological support.[/yellow]
  - [cyan]AI/NLP extracted symptoms: burning pain[/cyan]
  - [green]AI/NLP entities: burning pain (SYMPTOM), night (TRIGGER), anxious (TRIGGER)[/green]

### 4. **All findings and recommendations are saved in the log:**
- Structured answers
- Free-text notes
- NLP/AI-extracted symptoms, triggers, entities
- Profile, reason, and recommendation

### 5. **User can export or review entries:**
```sh
python claisen_log.py show --last 3
python claisen_log.py export --format json --out ~/symptoms.json
```

### 6. **Follow-up sessions:**
```sh
python claisen_log.py triage --followup 7 --notes "Much better, only mild symptoms after spicy food."
```
- System updates recommendations and profile based on new input and NLP findings.

## ➤ AI/NLP Features Explained
- **spaCy NLP pipeline**: Extracts medical symptoms, triggers, and severity from free-text notes.
- **Custom EntityRuler**: Recognizes domain-specific entities (e.g., "burning pain", "night", "anxiety").
- **Urgency classifier**: Flags urgent cases for escalation.
- **AI-powered recommendations**: All findings are reflected in the personalized, colorized output.

## ➤ Data Storage
- All logs are stored at `~/.claisen/data.db` (JSON format).
- Each entry includes structured answers, free-text notes, NLP/AI findings, profile, and recommendations.

## ➤ Extending and Customizing
- Add more symptom entities or triggers in `triage_engine.py`.
- Train the urgency classifier on your own data for higher accuracy.
- Expand the triage logic for new profiles or comorbidities.

---

**For any issues or feature requests, open an issue or email support@claisen.com**
