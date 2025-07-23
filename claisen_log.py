#!/usr/bin/env python3
import os
import json
import argparse
from datetime import date, datetime
from typing import List, Dict

SYMPTOMS = ['bloating', 'gas', 'heartburn']
# Store data in the current project directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'claisen_data')
DATA_FILE = os.path.join(DATA_DIR, 'symptoms.json')

# Utility functions
def load_data() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data: List[Dict]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        save_data([])
        print(f"Initialized new symptom log at {DATA_FILE}")
    else:
        print(f"Symptom log already exists at {DATA_FILE}")

def prompt_symptoms_with_severity():
    print("Which symptoms are you experiencing today? (comma-separated)")
    print(f"Options: {', '.join(SYMPTOMS)}")
    raw = input("Symptoms: ").strip().lower()
    selected = [s.strip() for s in raw.split(',') if s.strip() in SYMPTOMS]
    symptoms = []
    for s in selected:
        while True:
            try:
                sev = int(input(f"Severity for {s} (1-5): "))
                if 1 <= sev <= 5:
                    symptoms.append({'name': s, 'severity': sev})
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid integer.")
    return symptoms

def triage(symptoms):
    if not symptoms:
        return "No symptoms reported. Keep up the good work!"
    messages = []
    for s in symptoms:
        if s['name'] == 'heartburn' and s['severity'] >= 3:
            messages.append("Heartburn (mod/severe): Consider reducing spicy or acidic foods.")
        if s['name'] == 'bloating' and s['severity'] >= 3:
            messages.append("Bloating (mod/severe): Monitor fiber intake and hydration.")
        if s['name'] == 'gas' and s['severity'] >= 3:
            messages.append("Gas (mod/severe): Consider tracking foods that may cause gas.")
    if not messages:
        return "Symptoms noted. Monitor and consult a professional if persistent."
    return '\n'.join(messages)

def add_entry():
    today = str(date.today())
    data = load_data()
    if any(entry['date'] == today for entry in data):
        print(f"You have already logged symptoms for today.")
        return
    symptoms = prompt_symptoms_with_severity()
    notes = input("Any notes? (optional): ").strip()
    entry = {
        'date': today,
        'symptoms': symptoms,
        'notes': notes
    }
    data.append(entry)
    save_data(data)
    print("\nTriage:")
    print(triage(symptoms))

def show_entries(last_n=None):
    data = load_data()
    if not data:
        print("No entries found.")
        return
    if last_n:
        data = data[-last_n:]
    print(f"{'Date':<12} {'Symptoms (severity)':<30} Notes")
    print("-"*60)
    for entry in data:
        sym_str = ', '.join(f"{s['name']}({s['severity']})" for s in entry['symptoms'])
        print(f"{entry['date']:<12} {sym_str:<30} {entry.get('notes','')}")

def export_entries(fmt, out):
    data = load_data()
    if fmt == 'json':
        with open(out, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Exported to {out} (JSON)")
    elif fmt == 'csv':
        import csv
        with open(out, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'symptom', 'severity', 'notes'])
            for entry in data:
                for s in entry['symptoms']:
                    writer.writerow([entry['date'], s['name'], s['severity'], entry.get('notes','')])
        print(f"Exported to {out} (CSV)")
    else:
        print("Unknown format. Use 'json' or 'csv'.")

def main():
    parser = argparse.ArgumentParser(description="Claisen Symptom Logger")
    subparsers = parser.add_subparsers(dest='command')

    # init
    subparsers.add_parser('init', help='Initialize the symptom log database')

    # add
    subparsers.add_parser('add', help='Add a new symptom entry for today')

    # show
    show_parser = subparsers.add_parser('show', help='Show recent entries')
    show_parser.add_argument('--last', type=int, default=None, help='Show only the last N entries')

    # export
    export_parser = subparsers.add_parser('export', help='Export entries to CSV or JSON')
    export_parser.add_argument('--format', choices=['csv', 'json'], required=True, help='Export format')
    export_parser.add_argument('--out', required=True, help='Output file path')

    args = parser.parse_args()

    if args.command == 'init':
        init_db()
    elif args.command == 'add':
        add_entry()
    elif args.command == 'show':
        show_entries(args.last)
    elif args.command == 'export':
        export_entries(args.format, args.out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 