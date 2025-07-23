# Triage questions and answer options, modularized for advanced CLI
# Each question is a dict with id, text, options, and optional branching/metadata

TRIAGE_QUESTIONS = [
    # Demographics
    {"id": "demographics_name", "text": "Hello! What is your name?", "type": "text"},
    {"id": "demographics_age", "text": "What is your age?", "type": "int"},
    {"id": "demographics_gender", "text": "Which gender were you assigned at birth?", "type": "choice", "options": ["Male", "Female"]},
    {"id": "demographics_pregnant", "text": "Are you pregnant, or do you plan on being pregnant?", "type": "choice", "options": ["Yes", "No"], "ask_if": {"demographics_gender": "Female"}},

    # Symptom Characterisation
    {"id": "symptom_type", "text": "What type of discomfort do you most often experience in your chest or upper abdomen?", "type": "choice", "options": ["Burning sensation", "Sharp/stabbing pain", "Pressure or tightness", "Fullness or bloating", "Sour or bitter taste in the mouth", "Pain radiating to neck or back", "No discomfort"]},
    {"id": "symptom_location", "text": "Where exactly do you feel the discomfort?", "type": "choice", "options": ["Just below the breastbone (epigastric area)", "Middle of the chest (retrosternal)", "Upper abdomen", "Throat or behind the sternum", "Lower abdomen", "Difficult to localise"]},
    {"id": "symptom_intensity", "text": "How would you rate the intensity of your discomfort at its worst? (1 = mild, 10 = unbearable)", "type": "choice", "options": ["1–3: Mild", "4–6: Moderate", "7–8: Severe", "9–10: Disabling"]},
    {"id": "symptom_frequency", "text": "How frequently do you experience these symptoms?", "type": "choice", "options": ["Less than once a week", "1–2 times per week", "3–5 times per week", "Daily", "Multiple times daily"]},
    {"id": "symptom_duration", "text": "How long does each episode usually last?", "type": "choice", "options": ["Less than 10 minutes", "10–30 minutes", "30 minutes – 1 hour", "Over 1 hour", "Continuous throughout the day"]},
    {"id": "symptom_postprandial", "text": "How soon after eating do symptoms begin?", "type": "choice", "options": ["Immediately (<10 min)", "10–30 minutes", "30–60 minutes", "1–2 hours", "No clear relation to meals"]},
    {"id": "symptom_food_triggers", "text": "Do you notice worsening after certain foods or drinks?", "type": "choice", "options": ["Spicy foods", "Fatty/fried foods", "Chocolate/caffeine", "Acidic foods (tomato, citrus)", "Alcohol", "No obvious triggers"]},
    {"id": "symptom_physical_activity", "text": "Does physical activity affect your symptoms?", "type": "choice", "options": ["Worsens with bending over/lifting", "Worsens with exertion (e.g. running)", "No effect", "Improves with movement"]},
    {"id": "symptom_lying_down", "text": "Do you experience symptoms when lying down or sleeping?", "type": "choice", "options": ["Yes, shortly after lying down", "Yes, I wake up at night with symptoms", "No, only daytime symptoms", "No clear relation"]},
    {"id": "sleep_hours", "text": "How many hours do you sleep on average per night?", "type": "choice", "options": ["<5 hours", "5–6 hours", "6–8 hours", ">8 hours"]},
    {"id": "sleep_position", "text": "How do you position yourself when sleeping?", "type": "choice", "options": ["Flat on back", "On left side", "On right side", "On stomach", "Head elevated"]},
    {"id": "sour_taste", "text": "Do you experience a sour or bitter taste in your mouth?", "type": "choice", "options": ["Never", "Occasionally", "Often (more than 3 days/week)", "Daily, especially in the morning", "Only after certain foods"]},
    {"id": "night_choking", "text": "Have you ever woken up choking or coughing at night?", "type": "choice", "options": ["Yes, frequently (weekly or more)", "Occasionally (less than once a week)", "Rarely (once or twice ever)", "Never"]},
    {"id": "burping_hiccups", "text": "Do you experience frequent burping or hiccups?", "type": "choice", "options": ["Yes, multiple times daily", "Yes, after meals only", "Occasionally, without pattern", "No"]},
    {"id": "relief_attempts", "text": "Have you tried anything to relieve your symptoms already? If so, has it worked?", "type": "choice", "options": ["Antacids (Tums, Maalox) worked", "Proton pump inhibitors (omeprazole) worked", "Sitting upright", "Eating bland food", "Nothing provides consistent relief", "Not tried anything"]},
    {"id": "symptom_radiation", "text": "Does your discomfort spread anywhere else?", "type": "choice", "options": ["No, stays localised", "Radiates to neck or throat", "Radiates to back", "Radiates to left arm"]},
    {"id": "chest_palpitations", "text": "Do you experience chest tightness or palpitations during episodes?", "type": "choice", "options": ["Yes, regularly", "Occasionally", "Never"]},
    {"id": "symptom_free_period", "text": "When was the last time you had no symptoms for 7 days straight without taking any medication?", "type": "choice", "options": ["Within the past month", "1–3 months ago", "Over 3 months ago", "Can’t recall being symptom-free"]},

    # Cardiac Elimination Branch (triggered by certain answers)
    {"id": "cardiac_exertion", "text": "Is this discomfort triggered or worsened by exertion (walking, climbing stairs, etc.)?", "type": "choice", "options": ["Yes, always with exertion", "Sometimes with exertion", "No correlation with activity", "Symptoms improve with activity"]},
    {"id": "cardiac_antacid_response", "text": "Does your discomfort improve with antacids or food?", "type": "choice", "options": ["Yes, within 15–30 min", "No effect from antacids", "Worsens after eating", "Not applicable / never tried"]},
    {"id": "cardiac_risk_factors", "text": "Do you have any of the following risk factors? (Select all that apply)", "type": "multi_choice", "options": ["Age > 50 years", "Current/former smoker", "Diabetes mellitus", "Hypertension", "High cholesterol", "Family history of early heart disease (<55 M, <65 F)", "None of the above"]},
    {"id": "cardiac_workup", "text": "Have you ever had a cardiac work-up (ECG, stress test, echocardiogram)?", "type": "choice", "options": ["Yes, normal within last 12 months", "Yes, but >1 year ago", "No, never", "Don’t recall"]},
    {"id": "cardiac_rest_discomfort", "text": "Does the discomfort occur at rest, especially early morning or at night?", "type": "choice", "options": ["Yes, especially early morning", "Yes, random times during rest", "Only during meals or lying down", "Only during activity"]},

    # Alarm Features (Q19–Q27)
    {"id": "weight_change", "text": "Have you gained or lost significant weight in the past 6 months?", "type": "choice", "options": ["Lost >5% of my body weight", "Lost <5% of my body weight", "Gained weight intentionally (e.g. post-pregnancy, muscle gain)", "Gained weight unintentionally", "No weight loss or gain"]},
    {"id": "vomiting_blood", "text": "Have you vomited blood (haematemesis) or noticed black, tarry stools (melena)?", "type": "choice", "options": ["Yes, vomited blood", "Yes, black tarry stools", "Both", "No"]},
    {"id": "dysphagia", "text": "Do you have trouble swallowing (dysphagia)?", "type": "choice", "options": ["Yes, progressively worsening", "Yes, occasional or stable", "No difficulty swallowing"]},
    {"id": "odynophagia", "text": "Do you feel pain when swallowing (odynophagia)?", "type": "choice", "options": ["Yes, sharp or burning pain with food/liquids", "No pain swallowing"]},
    {"id": "family_gi_cancer", "text": "Do you have a known family history of upper gastrointestinal cancer?", "type": "choice", "options": ["Yes, in a first-degree relative (parent/sibling)", "Yes, but only distant relatives", "No family history"]},
    {"id": "symptom_change", "text": "Have your symptoms changed in nature or become more severe in the last 2–4 weeks?", "type": "choice", "options": ["Yes, new or rapidly worsening symptoms", "Yes, but slowly and mildly", "No change"]},
    {"id": "immunocompromised", "text": "Are you currently immunocompromised (HIV, chemotherapy, transplant, etc.)?", "type": "choice", "options": ["Yes", "No"]},
    {"id": "anaemia", "text": "Have you had iron deficiency anaemia or low haemoglobin recently?", "type": "choice", "options": ["Yes, diagnosed in the last 3–6 months", "No or unknown"]},
    {"id": "persistent_nausea", "text": "Do you experience persistent nausea or vomiting unrelated to meals?", "type": "choice", "options": ["Yes, daily or nearly daily", "Occasional nausea with meals", "No"]},

    # ... (continue for all remaining questions: lifestyle, medication, GI, respiratory, psychosocial, etc.)
]

# For brevity, only a subset is shown. The full list should be completed for all questions in the README, following this structure. 