#!/usr/bin/env python3
import os
import json
from datetime import date

SYMPTOMS = ['bloating', 'gas', 'heartburn']
DATA_DIR = os.path.expanduser('~/.claisen')
DATA_FILE = os.path.join(DATA_DIR, 'symptoms.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def prompt_symptoms():
    print("Which symptoms are you experiencing today? (comma-separated)")
    print(f"Options: {', '.join(SYMPTOMS)}")
    raw = input("Symptoms: ").strip().lower()
    selected = [s.strip() for s in raw.split(',') if s.strip() in SYMPTOMS]
    return selected

def triage(symptoms):
    if not symptoms:
        return "No symptoms reported. Keep up the good work!"
    if 'heartburn' in symptoms:
        return "Heartburn detected. Consider reducing spicy or acidic foods."
    if 'bloating' in symptoms:
        return "Bloating detected. Try to monitor fiber intake and hydration."
    if 'gas' in symptoms:
        return "Gas detected. Consider tracking foods that may cause gas."
    return "Symptoms noted. Monitor and consult a professional if persistent."

def main():
    today = str(date.today())
    data = load_data()
    if today in data:
        print(f"You have already logged symptoms for today: {data[today]}")
        return
    symptoms = prompt_symptoms()
    data[today] = symptoms
    save_data(data)
    print("\nTriage:")
    print(triage(symptoms))

if __name__ == "__main__":
    main() 