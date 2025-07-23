#!/usr/bin/env python3
import os
import json
import argparse
from datetime import date, datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, ValidationError, validator
from rich.console import Console
from rich.table import Table
from claisen_data.triage_questions import TRIAGE_QUESTIONS
from claisen_data.triage_engine import assign_profile

SYMPTOMS = ['bloating', 'gas', 'heartburn']
# Store data in the user's home directory
DATA_DIR = os.path.expanduser('~/.claisen')
DATA_FILE = os.path.join(DATA_DIR, 'data.db')
console = Console()

class SymptomEntry(BaseModel):
    name: str
    severity: int

    @validator('name')
    def name_must_be_valid(cls, v):
        if v not in SYMPTOMS:
            raise ValueError(f"Invalid symptom: {v}")
        return v

    @validator('severity')
    def severity_must_be_1_5(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("Severity must be between 1 and 5")
        return v

class DayLog(BaseModel):
    date: str
    symptoms: List[SymptomEntry]
    notes: Optional[str] = ''

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
        console.print(f"[green]Initialized new symptom log at {DATA_FILE}")
    else:
        console.print(f"[yellow]Symptom log already exists at {DATA_FILE}")

def prompt_symptoms_with_severity():
    console.print("Which symptoms are you experiencing today? (comma-separated)")
    console.print(f"Options: {', '.join(SYMPTOMS)}")
    raw = input("Symptoms: ").strip().lower()
    selected = [s.strip() for s in raw.split(',') if s.strip() in SYMPTOMS]
    symptoms = []
    for s in selected:
        while True:
            try:
                sev = int(input(f"Severity for {s} (1-5): "))
                entry = SymptomEntry(name=s, severity=sev)
                symptoms.append(entry.dict())
                break
            except (ValueError, ValidationError) as e:
                console.print(f"[red]{e}")
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

def add_entry_cli(symptoms_arg, severity_arg, notes_arg):
    today = str(date.today())
    data = load_data()
    if any(entry['date'] == today for entry in data):
        console.print(f"[yellow]You have already logged symptoms for today.")
        return
    symptoms = []
    if symptoms_arg and severity_arg:
        for s in symptoms_arg.split(','):
            s = s.strip()
            try:
                entry = SymptomEntry(name=s, severity=int(severity_arg))
                symptoms.append(entry.dict())
            except ValidationError as e:
                console.print(f"[red]{e}")
                return
    else:
        symptoms = prompt_symptoms_with_severity()
    notes = notes_arg or input("Any notes? (optional): ").strip()
    try:
        entry = DayLog(date=today, symptoms=symptoms, notes=notes)
    except ValidationError as e:
        console.print(f"[red]{e}")
        return
    data.append(entry.dict())
    save_data(data)
    console.print("\n[bold green]Triage:[/bold green]")
    console.print(triage(symptoms))

def show_entries(last_n=None):
    data = load_data()
    if not data:
        console.print("[yellow]No entries found.")
        return
    if last_n:
        data = data[-last_n:]
    table = Table(title="Symptom Log")
    table.add_column("Date", style="cyan")
    table.add_column("Symptoms (severity)", style="magenta")
    table.add_column("Notes", style="white")
    for entry in data:
        sym_str = ', '.join(f"{s['name']}({s['severity']})" for s in entry['symptoms'])
        table.add_row(entry['date'], sym_str, entry.get('notes',''))
    console.print(table)

def export_entries(fmt, out):
    data = load_data()
    if fmt == 'json':
        with open(out, 'w') as f:
            json.dump(data, f, indent=2)
        console.print(f"[green]Exported to {out} (JSON)")
    elif fmt == 'csv':
        import csv
        with open(out, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'symptom', 'severity', 'notes'])
            for entry in data:
                for s in entry['symptoms']:
                    writer.writerow([entry['date'], s['name'], s['severity'], entry.get('notes','')])
        console.print(f"[green]Exported to {out} (CSV)")
    else:
        console.print("[red]Unknown format. Use 'json' or 'csv'.")

def run_advanced_triage(answers_arg=None, followup_day=None):
    answers = {}
    # If answers_arg is provided, parse it (as JSON or key=value pairs)
    import json
    if answers_arg:
        try:
            if answers_arg.strip().startswith('{'):
                answers = json.loads(answers_arg)
            else:
                for pair in answers_arg.split(','):
                    k, v = pair.split('=', 1)
                    answers[k.strip()] = v.strip()
        except Exception as e:
            console.print(f"[red]Failed to parse --answers: {e}[/red]")
            return
    # Interactive mode for missing answers
    for q in TRIAGE_QUESTIONS:
        if 'ask_if' in q:
            cond = q['ask_if']
            key, val = list(cond.items())[0]
            if answers.get(key) != val:
                continue
        if q['id'] in answers:
            continue
        if q['type'] == 'choice':
            console.print(f"[bold]{q['text']}[/bold]")
            for idx, opt in enumerate(q['options'], 1):
                console.print(f"  {idx}. {opt}")
            while True:
                resp = input("Enter number: ").strip()
                if resp.isdigit() and 1 <= int(resp) <= len(q['options']):
                    answers[q['id']] = q['options'][int(resp)-1]
                    break
                else:
                    console.print("[red]Invalid choice. Try again.[/red]")
        elif q['type'] == 'int':
            while True:
                resp = input(f"{q['text']} ").strip()
                try:
                    answers[q['id']] = int(resp)
                    break
                except ValueError:
                    console.print("[red]Please enter a valid number.[/red]")
        else:
            answers[q['id']] = input(f"{q['text']} ").strip()
    # Assign profile
    profile_result = assign_profile(answers)
    console.print(f"\n[bold cyan]Dosing Profile: {profile_result['profile']}[/bold cyan]")
    console.print(f"[green]{profile_result['reason']}[/green]")
    # Store in data
    today = str(date.today())
    data = load_data()
    entry = {
        'date': today,
        'triage_answers': answers,
        'profile': profile_result['profile'],
        'profile_reason': profile_result['reason'],
        'followup_day': followup_day
    }
    data.append(entry)
    save_data(data)
    console.print("[bold green]Triage result saved.[/bold green]")

def main():
    parser = argparse.ArgumentParser(description="Claisen Symptom Logger")
    subparsers = parser.add_subparsers(dest='command')

    # init
    subparsers.add_parser('init', help='Initialize the symptom log database')

    # add
    add_parser = subparsers.add_parser('add', help='Add a new symptom entry for today')
    add_parser.add_argument('--symptoms', type=str, help='Comma-separated list of symptoms')
    add_parser.add_argument('--severity', type=int, help='Severity for all symptoms (1-5)')
    add_parser.add_argument('--notes', type=str, help='Optional notes')

    # show
    show_parser = subparsers.add_parser('show', help='Show recent entries')
    show_parser.add_argument('--last', type=int, default=None, help='Show only the last N entries')

    # export
    export_parser = subparsers.add_parser('export', help='Export entries to CSV or JSON')
    export_parser.add_argument('--format', choices=['csv', 'json'], required=True, help='Export format')
    export_parser.add_argument('--out', required=True, help='Output file path')

    triage_parser = subparsers.add_parser('triage', help='Run advanced triage and dosing profile assignment')
    triage_parser.add_argument('--answers', type=str, help='Non-interactive: JSON or comma-separated key=value pairs for answers')
    triage_parser.add_argument('--followup', type=int, choices=[7, 14, 28], help='Day of follow-up session (7, 14, 28)')

    args = parser.parse_args()

    if args.command == 'init':
        init_db()
    elif args.command == 'add':
        add_entry_cli(args.symptoms, args.severity, args.notes)
    elif args.command == 'show':
        show_entries(args.last)
    elif args.command == 'export':
        export_entries(args.format, args.out)
    elif args.command == 'triage':
        run_advanced_triage(answers_arg=args.answers, followup_day=args.followup)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 