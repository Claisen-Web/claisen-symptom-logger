from typing import Dict
from .triage_questions import TRIAGE_QUESTIONS
import spacy
import re

# Load spaCy English model (will require python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

def extract_symptoms_from_text(text: str) -> Dict:
    """
    Use spaCy to extract symptoms, severity, and triggers from free-text notes.
    Returns a dict of structured findings.
    """
    if not text or not nlp:
        return {}
    doc = nlp(text)
    findings = {"symptoms": [], "severity": None, "triggers": [], "timing": [], "sentiment": None}
    # Simple keyword-based extraction for demo
    SYMPTOM_KEYWORDS = ["bloating", "gas", "heartburn", "pain", "burning", "nausea", "vomiting", "cough", "choking", "burping", "hiccups", "sour taste", "fullness", "tightness", "pressure"]
    for token in doc:
        for kw in SYMPTOM_KEYWORDS:
            if kw in token.text.lower() and kw not in findings["symptoms"]:
                findings["symptoms"].append(kw)
    # Severity (look for numbers or adjectives)
    if re.search(r"severe|unbearable|can't sleep|awful|worst|disabling", text, re.I):
        findings["severity"] = "severe"
    elif re.search(r"mild|slight|occasional|manageable|better", text, re.I):
        findings["severity"] = "mild"
    elif re.search(r"moderate|bothersome|often|frequent", text, re.I):
        findings["severity"] = "moderate"
    # Triggers
    for trigger in ["night", "lying down", "after eating", "spicy", "fatty", "stress", "anxiety", "exercise", "alcohol", "caffeine"]:
        if trigger in text.lower():
            findings["triggers"].append(trigger)
    # Timing
    for timing in ["night", "morning", "after meals", "bedtime", "daily", "weekly"]:
        if timing in text.lower():
            findings["timing"].append(timing)
    # Sentiment (very basic)
    if re.search(r"can't cope|hopeless|urgent|worried|scared|afraid|emergency", text, re.I):
        findings["sentiment"] = "urgent"
    elif re.search(r"coping|ok|fine|improving|better", text, re.I):
        findings["sentiment"] = "stable"
    return findings

def assign_profile(answers: Dict, notes: str = None) -> Dict:
    """
    Assign dosing profile (1-5) based on advanced triage logic from README and all question domains.
    Returns dict with profile, reason, and detailed recommendation.
    Uses NLP on notes if provided.
    """
    nlp_extracted = extract_symptoms_from_text(notes) if notes else {}
    # Use NLP findings to influence triage
    nlp_severity = nlp_extracted.get("severity")
    nlp_symptoms = nlp_extracted.get("symptoms", [])
    nlp_triggers = nlp_extracted.get("triggers", [])
    nlp_sentiment = nlp_extracted.get("sentiment")
    # If NLP finds urgent sentiment, escalate
    if nlp_sentiment == "urgent":
        return {
            "profile": 5,
            "reason": "NLP detected urgent sentiment in notes.",
            "recommendation": (
                "[bold red]URGENT: Your notes suggest you may need immediate medical attention.[/bold red]\n"
                "- Please seek emergency care or contact your doctor immediately.\n"
            ),
            "nlp_extracted": nlp_extracted
        }
    # If NLP finds severe symptoms at night, suggest nocturnal GERD
    if nlp_severity == "severe" and ("night" in nlp_triggers or "night" in nlp_extracted.get("timing", [])):
        return {
            "profile": 3,
            "reason": "NLP detected severe nocturnal symptoms in notes.",
            "recommendation": (
                "[bold magenta]Severe night-time symptoms detected.[/bold magenta]\n"
                "- Start omeprazole 20 mg AM + famotidine 10–20 mg at bedtime for 14 days.\n"
                "- Elevate head of bed, avoid late meals, and sleep on left side.\n"
                "- [cyan]Reassess in 7–14 days. If persistent, escalate to Profile 4.[/cyan]"
            ),
            "nlp_extracted": nlp_extracted
        }
    # If NLP finds stress/anxiety as trigger, add to recommendations
    stress_nlp = any(t in nlp_triggers for t in ["stress", "anxiety"])
    # Continue with main triage logic, but add NLP findings to recommendations
    # Profile 5: Alarm features (Q19–Q27)
    alarm_keys = [
        'weight_change', 'vomiting_blood', 'dysphagia', 'odynophagia',
        'family_gi_cancer', 'symptom_change', 'immunocompromised',
        'anaemia', 'persistent_nausea', 'followup_alarm_features'
    ]
    for k in alarm_keys:
        v = answers.get(k, '')
        if v and (v.startswith('Yes') or v.startswith('Lost') or v.startswith('Gained')) and v not in ['No', 'No pain swallowing', 'No family history', 'No change', 'No or unknown']:
            return {
                "profile": 5,
                "reason": f"Alarm feature detected: {k.replace('_',' ')}",
                "recommendation": (
                    "[bold red]URGENT: Alarm features detected.[/bold red]\n"
                    "- Immediate GI referral for upper endoscopy (EGD) within 2 weeks.\n"
                    "- Lab tests: CBC, LFTs, ferritin, BUN/Cr.\n"
                    "- Stop all OTC PPI/H2RA until workup complete.\n"
                    "- If haematemesis/melena: ED or urgent EGD within 48 hrs.\n"
                    "- Progressive dysphagia: Urgent endoscopy + biopsy.\n"
                    "- 5% weight loss + alarm: 14-day cancer pathway.\n"
                    "- Family history of GI cancer: expedited scope.\n"
                    "- Document alarm features and duration clearly.\n"
                ),
                "nlp_extracted": nlp_extracted
            }

    # Profile 1: Mild, infrequent GERD (with subtypes)
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Fullness or bloating', 'No discomfort'] and
        answers.get('symptom_intensity') in ['1–3: Mild', '4–6: Moderate'] and
        answers.get('symptom_frequency') in ['Less than once a week', '1–2 times per week'] and
        answers.get('symptom_duration') in ['Less than 10 minutes', '10–30 minutes'] and
        answers.get('relief_attempts') in ['Antacids (Tums, Maalox) worked', 'Eating bland food'] and
        answers.get('symptom_free_period') in ['Within the past month', '1–3 months ago'] and
        answers.get('meal_portion_size') != 'Large' and
        answers.get('meal_bedtime_interval') in ['>3 hours before bed', '2–3 hours before bed'] and
        answers.get('alcohol_use') in ['Never', 'Socially, <1x/week'] and
        answers.get('tobacco_use') in ['Never', 'Former smoker (quit >6 months ago)']
    ):
        # Subtype: If stress is a trigger
        if answers.get('stress_worsen') in ['Yes, significantly and predictably', 'Yes, but not always']:
            stress_note = "- [yellow]Stress appears to be a trigger. Consider stress management techniques (mindfulness, CBT, relaxation).[/yellow]\n"
        else:
            stress_note = ""
        return {
            "profile": 1,
            "reason": "Mild, infrequent symptoms, good response to antacids, no red flags, healthy lifestyle.",
            "recommendation": (
                "[bold green]Lifestyle modifications + on-demand antacids.[/bold green]\n"
                "- Avoid large meals and late eating.\n"
                "- Maintain upright posture after meals.\n"
                "- Limit trigger foods/drinks.\n"
                "- Use calcium carbonate antacids as needed.\n"
                f"{stress_note}"
                "- No need for daily acid suppression.\n"
                "- [cyan]Follow up in 7 days to reassess control.[/cyan]"
            ),
            "nlp_extracted": nlp_extracted
        }

    # Profile 2: Moderate classic GERD (with subtypes)
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Sour or bitter taste in the mouth'] and
        answers.get('symptom_intensity') in ['4–6: Moderate', '7–8: Severe'] and
        answers.get('symptom_frequency') in ['3–5 times per week', 'Daily'] and
        answers.get('symptom_postprandial') in ['Immediately (<10 min)', '10–30 minutes', '30–60 minutes'] and
        answers.get('sour_taste') in ['Often (more than 3 days/week)', 'Daily, especially in the morning'] and
        answers.get('recent_ppi') == 'No' and
        answers.get('meal_portion_size') == 'Large'
    ):
        # Subtype: If caffeine or NSAIDs present
        med_note = ""
        if 'NSAIDs' in answers.get('meds_reflux', ''):
            med_note += "- [yellow]NSAIDs may worsen symptoms. Minimize or discuss alternatives with your doctor.[/yellow]\n"
        if answers.get('caffeine_intake') == '>3 cups/day':
            med_note += "- [yellow]High caffeine intake may contribute. Reduce to <2 cups/day.[/yellow]\n"
        return {
            "profile": 2,
            "reason": "Moderate, classic GERD symptoms, daily or near-daily, sleep disturbance, known triggers, no recent PPI use.",
            "recommendation": (
                "[bold yellow]Start omeprazole 20 mg every morning for 14 days (FDA OTC limit).[/bold yellow]\n"
                "- Continue lifestyle modifications as in Profile 1.\n"
                "- Keep a symptom diary.\n"
                f"{med_note}"
                "- [cyan]Reassess at Day 7 and Day 14. If improved, stop PPI and continue PRN antacids. If not, escalate to Profile 3 or 4.[/cyan]"
            ),
            "nlp_extracted": nlp_extracted
        }

    # Profile 3: Nocturnal/positional GERD (with subtypes)
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Sour or bitter taste in the mouth'] and
        answers.get('symptom_lying_down') in ['Yes, shortly after lying down', 'Yes, I wake up at night with symptoms'] and
        answers.get('night_choking', '').startswith('Yes') and
        answers.get('sleep_position') in ['Flat on back', 'On right side']
    ):
        return {
            "profile": 3,
            "reason": "Nocturnal or positional GERD: night symptoms, lying-down reflux, choking/regurgitation at night, suboptimal sleep posture.",
            "recommendation": (
                "[bold magenta]Start omeprazole 20 mg AM + famotidine 10–20 mg at bedtime for 14 days.[/bold magenta]\n"
                "- Strict head-of-bed elevation (wedge or risers).\n"
                "- Avoid late meals and alcohol.\n"
                "- Sleep on left side if possible.\n"
                "- [cyan]Reassess at Day 7 and Day 14. If persistent, consider Profile 4.[/cyan]"
            ),
            "nlp_extracted": nlp_extracted
        }
    # Profile 3 (alternate): High-risk lifestyle triggers
    if (
        answers.get('meal_portion_size') == 'Large' and
        answers.get('meal_bedtime_interval') == '<1 hour before bed' and
        answers.get('alcohol_use') == 'Daily' and
        answers.get('tobacco_use') == 'Yes, daily'
    ):
        return {
            "profile": 3,
            "reason": "Nocturnal/positional GERD with high-risk lifestyle triggers (large meals, late eating, daily alcohol/tobacco).",
            "recommendation": (
                "[bold magenta]Intensive lifestyle modification required.[/bold magenta]\n"
                "- Reduce meal size and avoid eating <3 hours before bed.\n"
                "- Eliminate or reduce alcohol and tobacco.\n"
                "- Elevate head of bed.\n"
                "- Consider short-term dual therapy (omeprazole + famotidine) if symptoms persist.\n"
            ),
            "nlp_extracted": nlp_extracted
        }

    # Profile 4: Suspected functional/refractory GERD (with subtypes)
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Pressure or tightness'] and
        answers.get('symptom_intensity') in ['7–8: Severe', '9–10: Disabling'] and
        answers.get('relief_attempts') in ['Nothing provides consistent relief', 'Proton pump inhibitors (omeprazole) worked', 'Not tried anything'] and
        answers.get('symptom_free_period') == 'Can’t recall being symptom-free' and
        (answers.get('recent_ppi') == 'Yes' or answers.get('meds_reflux', '') != 'None of the above')
    ):
        # Subtype: If IBS or stress
        ibs_note = ""
        if answers.get('bowel_pattern') == 'Yes, alternating diarrhoea and constipation':
            ibs_note = "- [yellow]IBS/functional overlap suspected. Consider low-FODMAP diet and GI referral.[/yellow]\n"
        if answers.get('stress_worsen') in ['Yes, significantly and predictably', 'Yes, but not always']:
            ibs_note += "- [yellow]Stress may be a major factor. Consider psychological support or therapy.[/yellow]\n"
        return {
            "profile": 4,
            "reason": "Persistent symptoms despite correct PPI use, poor response, or overlapping dyspepsia/IBS traits, or medication triggers.",
            "recommendation": (
                "[bold blue]Discontinue PPI/H2RA (FDA OTC limit reached). Refer to gastroenterology for pH monitoring, impedance testing, and functional workup.[/bold blue]\n"
                "- Consider simethicone or alginate-based agents for interim relief.\n"
                f"{ibs_note}"
                "- [cyan]Continue symptom diary and dietary reprogramming.[/cyan]"
            ),
            "nlp_extracted": nlp_extracted
        }

    # Profile 2 (alternate): Moderate symptoms with some lifestyle risk
    if (
        answers.get('symptom_intensity') in ['4–6: Moderate', '7–8: Severe'] and
        answers.get('symptom_frequency') in ['3–5 times per week', 'Daily'] and
        (answers.get('meal_portion_size') == 'Large' or answers.get('alcohol_use') == '2–3 times/week')
    ):
        return {
            "profile": 2,
            "reason": "Moderate symptoms with some lifestyle risk factors.",
            "recommendation": (
                "[bold yellow]Lifestyle modification + consider short PPI course.[/bold yellow]\n"
                "- Reduce meal size, avoid late eating, limit alcohol.\n"
                "- Reassess in 7–14 days.\n"
            ),
            "nlp_extracted": nlp_extracted
        }

    # Default: Profile 2 (moderate)
    result = {
        "profile": 2,
        "reason": "Default: moderate symptoms (expand logic as needed)",
        "recommendation": (
            "[bold yellow]Lifestyle modification + consider short PPI course.[/bold yellow]\n"
            "- Reduce meal size, avoid late eating, limit alcohol.\n"
            "- Reassess in 7–14 days.\n"
        ),
        "nlp_extracted": nlp_extracted
    }
    # If NLP found stress/anxiety, add to recommendation
    if stress_nlp:
        result["recommendation"] += "- [yellow]Your notes suggest stress/anxiety as a trigger. Consider stress management or psychological support.[/yellow]\n"
    # If NLP found specific symptoms, add to recommendation
    if nlp_symptoms:
        result["recommendation"] += f"- [cyan]NLP extracted symptoms: {', '.join(nlp_symptoms)}[/cyan]\n"
    return result 