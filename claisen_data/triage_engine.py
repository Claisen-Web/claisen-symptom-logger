from typing import Dict

# Placeholder: import the question structure
from .triage_questions import TRIAGE_QUESTIONS

def assign_profile(answers: Dict) -> Dict:
    """
    Assign dosing profile (1-5) based on advanced triage logic from README.
    """
    # Profile 5: Alarm features (Q19–Q27)
    alarm_keys = [
        'weight_change', 'vomiting_blood', 'dysphagia', 'odynophagia',
        'family_gi_cancer', 'symptom_change', 'immunocompromised',
        'anaemia', 'persistent_nausea'
    ]
    for k in alarm_keys:
        v = answers.get(k, '')
        if v and (v.startswith('Yes') or v.startswith('Lost') or v.startswith('Gained')) and v not in ['No', 'No pain swallowing', 'No family history', 'No change', 'No or unknown']:
            return {"profile": 5, "reason": f"Alarm feature detected: {k.replace('_',' ')}"}

    # Profile 1: Mild, infrequent GERD
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Fullness or bloating', 'No discomfort'] and
        answers.get('symptom_intensity') in ['1–3: Mild', '4–6: Moderate'] and
        answers.get('symptom_frequency') in ['Less than once a week', '1–2 times per week'] and
        answers.get('symptom_duration') in ['Less than 10 minutes', '10–30 minutes'] and
        answers.get('relief_attempts') in ['Antacids (Tums, Maalox) worked', 'Eating bland food'] and
        answers.get('symptom_free_period') in ['Within the past month', '1–3 months ago']
    ):
        return {"profile": 1, "reason": "Mild, infrequent symptoms, good response to antacids, no red flags."}

    # Profile 2: Moderate classic GERD
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Sour or bitter taste in the mouth'] and
        answers.get('symptom_intensity') in ['4–6: Moderate', '7–8: Severe'] and
        answers.get('symptom_frequency') in ['3–5 times per week', 'Daily'] and
        answers.get('symptom_postprandial') in ['Immediately (<10 min)', '10–30 minutes', '30–60 minutes'] and
        answers.get('sour_taste') in ['Often (more than 3 days/week)', 'Daily, especially in the morning']
    ):
        return {"profile": 2, "reason": "Moderate, classic GERD symptoms, daily or near-daily, sleep disturbance, known triggers."}

    # Profile 3: Nocturnal/positional GERD
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Sour or bitter taste in the mouth'] and
        answers.get('symptom_lying_down') in ['Yes, shortly after lying down', 'Yes, I wake up at night with symptoms'] and
        answers.get('night_choking', '').startswith('Yes')
    ):
        return {"profile": 3, "reason": "Nocturnal or positional GERD: night symptoms, lying-down reflux, choking/regurgitation at night."}

    # Profile 4: Suspected functional/refractory GERD
    if (
        answers.get('symptom_type') in ['Burning sensation', 'Pressure or tightness'] and
        answers.get('symptom_intensity') in ['5–10: Severe', '7–8: Severe', '9–10: Disabling'] and
        answers.get('relief_attempts') in ['Nothing provides consistent relief', 'Proton pump inhibitors (omeprazole) worked', 'Not tried anything'] and
        answers.get('symptom_free_period') == 'Can’t recall being symptom-free'
    ):
        return {"profile": 4, "reason": "Persistent symptoms despite correct PPI use, poor response, or overlapping dyspepsia/IBS traits."}

    # Default: Profile 2 (moderate)
    return {"profile": 2, "reason": "Default: moderate symptoms (expand logic as needed)"} 