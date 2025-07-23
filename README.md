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

## Usage

```sh
claisen-log init
claisen-log add --symptoms gas,bloating --severity 3 --notes "Felt worse after lunch"
claisen-log show --last 7
claisen-log export --format csv --out ~/symptoms.csv
```

- If you omit `--symptoms` and `--severity`, the tool will prompt you interactively.
- Data is stored at `~/.claisen/data.db`.
- Output is colorized using Rich.
- All input is validated with Pydantic.

---


Starting boxes:
1.⁠ ⁠Hello [Name]. What is your age?
2.⁠ ⁠⁠Which gender were you assigned at birth? Male/Female
3.⁠ ⁠⁠if Male, continue to next box. if Female, ask if the person is pregnant or plans or being pregnant. “Are you pregnant, or do you plan on being pregnant?”




SYMPTOM CHARACTERISATION
4. What type of discomfort do you most often experience in your chest or upper abdomen?
A) Burning sensation
B) Sharp/stabbing pain 
C) Pressure or tightness
D) Fullness or bloating
E) Sour or bitter taste in the mouth
F) Pain radiating to neck or back
G) No discomfort



5. Where exactly do you feel the discomfort?
A) Just below the breastbone (epigastric area)
B) Middle of the chest (retrosternal)
C) Upper abdomen
D) Throat or behind the sternum
E) Lower abdomen
F) Difficult to localise

6. How would you rate the intensity of your discomfort at its worst? (1 = mild, 10 = unbearable)
☐ 1–3: Mild
☐ 4–6: Moderate
☐ 7–8: Severe
☐ 9–10: Disabling
7. How frequently do you experience these symptoms?
A. Less than once a week
B. 1–2 times per week
C. 3–5 times per week
D. Daily
E. Multiple times daily

8. How long does each episode usually last?
A. Less than 10 minutes
B. 10–30 minutes
C. 30 minutes – 1 hour
D. Over 1 hour
E. Continuous throughout the day

9. How soon after eating do symptoms begin?
A. Immediately (<10 min)
B. 10–30 minutes
C. 30–60 minutes
D. 1–2 hours
E. No clear relation to meals

7. Do you notice worsening after certain foods or drinks?
A. Spicy foods
B. Fatty/fried foods
C. Chocolate/caffeine
D. Acidic foods (tomato, citrus)
E. Alcohol
F. No obvious triggers

8. Does physical activity affect your symptoms?
A. Worsens with bending over/lifting
B. Worsens with exertion (e.g. running)
C. No effect
D. Improves with movement


9. Do you experience symptoms when lying down or sleeping?
A. Yes, shortly after lying down
B. Yes, I wake up at night with symptoms
C. No, only daytime symptoms
D. No clear relation
10. How many hours do you sleep on average per night?
A. <5 hours
B. 5–6 hours
C. 6–8 hours
D. >8 hours

11. How do you position yourself when sleeping?
A. Flat on back
B. On left side
C. On right side
D. On stomach
E. Head elevated

12. Do you experience a sour or bitter taste in your mouth?
A. Never
B. Occasionally
C. Often (more than 3 days/week)
D. Daily, especially in the morning
E. Only after certain foods

13. Have you ever woken up choking or coughing at night?
A. Yes, frequently (weekly or more)
B. Occasionally (less than once a week)
C. Rarely (once or twice ever)
D. Never

14. Do you experience frequent burping or hiccups?
A. Yes, multiple times daily
B. Yes, after meals only
C. Occasionally, without pattern
D. No

15. Have you tried anything to relieve your symptoms already? If so, has it worked?
A. Antacids (Tums, Maalox) worked
B. Proton pump inhibitors (omeprazole) worked
C. Sitting upright
D. Eating bland food
E. Nothing provides consistent relief
F. Not tried anything

16. Does your discomfort spread anywhere else?
A. No, stays localised
B. Radiates to neck or throat
C. Radiates to back
D. Radiates to left arm

17. Do you experience chest tightness or palpitations during episodes?
A. Yes, regularly
B. Occasionally
C. Never

18. When was the last time you had no symptoms for 7 days straight without taking any medication?

A. Within the past month
B. 1–3 months ago
C. Over 3 months ago
D. Can’t recall being symptom-free


Cardiac Elimination Branch
Take arrows going from 4B, 8D going to this and say “If cardiac symptoms are suspected, additional screening will be employed”. 
1. Is this discomfort triggered or worsened by exertion (walking, climbing stairs, etc.)?
A. Yes, always with exertion
B. Sometimes with exertion
C. No correlation with activity
D. Symptoms improve with activity


2. Does your discomfort improve with antacids or food?
A. Yes, within 15–30 min
B. No effect from antacids
C. Worsens after eating
D. Not applicable / never tried



3. Do you have any of the following risk factors? (Select all that apply)
A. Age > 50 years
B. Current/former smoker
C. Diabetes mellitus
D. Hypertension
E. High cholesterol
F. Family history of early heart disease (<55 M, <65 F)
G. None of the above

4. Have you ever had a cardiac work-up (ECG, stress test, echocardiogram)?
A. Yes, normal within last 12 months
B. Yes, but >1 year ago
C. No, never
D. Don’t recall

5. Does the discomfort occur at rest, especially early morning or at night?
A. Yes, especially early morning
B. Yes, random times during rest
C. Only during meals or lying down
D. Only during activity

6. If ≥2 cardiac risk factors + exertional pain, immediate cardiology referral. If low risk and classic GERD features then return to the GERD algorithm. If uncertain, then recommend ECG for patients in any case.


Alarm Features
These questions identify patients who need urgent endoscopy, non-GERD differential diagnosis, or specialist referral. SEPARATE SECTION

19. Have you gained or lost significant weight in the past 6 months?

A. Lost >5% of my body weight
B. Lost <5% of my body weight
C. Gained weight intentionally (e.g. post-pregnancy, muscle gain)
D. Gained weight unintentionally
E. No weight loss or gain


20. Have you vomited blood (haematemesis) or noticed black, tarry stools (melena)?
A. Yes, vomited blood
B. Yes, black tarry stools
C. Both
D. No

21. Do you have trouble swallowing (dysphagia)?
A. Yes, progressively worsening
B. Yes, occasional or stable
C. No difficulty swallowing

22. Do you feel pain when swallowing (odynophagia)?
A. Yes, sharp or burning pain with food/liquids
B. No pain swallowing


23. Do you have a known family history of upper gastrointestinal cancer?
A. Yes, in a first-degree relative (parent/sibling)
B. Yes, but only distant relatives
C. No family history

24. Have your symptoms changed in nature or become more severe in the last 2–4 weeks?
A. Yes, new or rapidly worsening symptoms
B. Yes, but slowly and mildly
C. No change

25. Are you currently immunocompromised (HIV, chemotherapy, transplant, etc.)?
A. Yes
B. No

26. Have you had iron deficiency anaemia or low haemoglobin recently?
A. Yes, diagnosed in the last 3–6 months
B. No or unknown

27. Do you experience persistent nausea or vomiting unrelated to meals?
A. Yes, daily or nearly daily
B. Occasional nausea with meals
C. No

Dietary & Lifestyle Triggers
28. How large are your typical meal portions?
A. Small
B. Moderate
C. Large

29. How close to bedtime do you usually eat your last meal?
A. <1 hour before bed
B. 1–2 hours before bed
C. 2–3 hours before bed
D. >3 hours before bed

30. How often do you skip breakfast or have irregular meals?
A. Frequently
B. Occasionally
C. Rarely or never

31. How often do you consume caffeinated beverages (tea, coffee, energy drinks)?
A. >3 cups/day
B. 1–2 cups/day
C. Rarely or never

32. Do you smoke tobacco products?
A. Yes, daily
B. Occasionally/socially
C. Former smoker (quit >6 months ago)
D. Never

33. Do you consume alcohol?
A. Daily
B. 2–3 times/week
C. Socially, <1x/week
D. Never

34. What is your typical physical activity level overall?
A. Sedentary (mostly sitting, <3 days/week of exercise)
B. Light activity (walking, yoga, etc.)
C. Moderate activity (gym, sports 3–4 days/week)
D. High intensity (daily exercise, cardio/weights)


35. Do you wear tight-fitting clothing around your waist or abdomen?
A. Yes, daily (e.g., belts, shapewear)
B. Occasionally
C. No

Medication History


36. Have you taken omeprazole or any PPI in the last 3 months?
A. Yes
B. No

36. Are you taking any prescription medications that can worsen or mimic reflux symptoms? (Select all that apply)

A. NSAIDs (e.g. ibuprofen, naproxen, diclofenac)
B. Bisphosphonates (e.g. alendronate, risedronate)
C. Iron supplements or potassium chloride
D. Calcium channel blockers (e.g. amlodipine, nifedipine)
E. Anticholinergics or tricyclic antidepressants
F. Benzodiazepines or opioids
G. SSRIs (e.g. sertraline, fluoxetine)
H. None of the above

37. Do you use any herbal supplements for digestion or reflux?
A. Yes – ginger, slippery elm, licorice, etc.
B. Yes – unknown herbal mixtures
C. No supplements used

38. Are you currently on hormone therapy or birth control pills?
A. Yes – oestrogen or combined contraceptives
B. Yes – progesterone (e.g. IUD, oral, etc.)
C. No hormonal therapy

39. Do you take any supplements (e.g. calcium, magnesium, zinc)?
A. Yes, daily
B. Occasionally
C. No supplements


Bowel and GI History
40. Do you feel bloated or excessively full after eating?
A. Yes, even with small meals (early satiety)
B. Yes, mostly after large meals
C. No, I don’t feel unusually full
D. Only occasionally

41. Do you pass stool regularly (once daily or near daily)?
A. Yes, once daily
B. Yes, but not daily (3–5x/week)
C. No, <3 times per week
D. Too frequent (>3/day)

42. Do you ever experience constipation, diarrhoea, or alternating stool patterns?
A. Yes, alternating diarrhoea and constipation
B. Mostly constipation
C. Mostly diarrhoea
D. No abnormal bowel patterns

43. Have you ever been diagnosed with a stomach or duodenal ulcer?
A. Yes, previously confirmed via endoscopy
B. Suspected, but never confirmed
C. No history of ulcers
D. Not sure
44. Have you ever tested positive for Helicobacter pylori (H. pylori)?
A. Yes, tested positive and completed eradication therapy
B. Yes, but not treated / treatment incomplete
C. No, tested negative
D. Never been tested

45. Have you ever had a cholecystectomy (gallbladder removal)?
A. Yes
B. No


Respiratory / ENT Manifestations
46. Have you experienced persistent throat clearing or a chronic sensation of mucus in your throat (postnasal drip)?
A. Yes, daily or multiple times per day
B. Yes, but only occasionally
C. No

47. Do you experience hoarseness or a change in your voice quality, especially in the morning?
A. Yes, daily or several times a week
B. Occasionally, during colds or overuse
C. No voice issues

48. Have you ever been diagnosed with asthma or reactive airway disease (RAD)?
A. Yes
B. No

49. Have you experienced frequent sore throats or a lump-in-the-throat sensation (globus)?
A. Yes, sore throat and globus regularly
B. Only globus sensation without pain
C. No such symptoms


Psychosocial & Stress Factors
50. Do your symptoms worsen during times of stress, anxiety, or emotional upset?
A. Yes, significantly and predictably
B. Yes, but not always
C. No, symptoms unrelated to stress
D. Not sure / haven’t noticed


Dosing Profiles

DOSING PROFILE 1: MILD INFREQUENT GERD
Target: Patients with mild symptoms <2×/week, no red flags, no major sleep disturbance, good response to antacids.

Triggering Answers:
Q4: A, D, or G
Q6: 1–3 or 4–6
Q7: A or B
Q8: A–B
Q15: A or D (antacids or bland food help)
Q18: A or B
Q28–30: Large meals or <2 h before bed
Alarm and Cardiac: All NO
Recommendation: Lifestyle mods + on-demand calcium carbonate antacids. Avoid OTC PPIs.

Day 7 Follow-Up

1-1. How many days in the past week did you use antacids (Tums, Maalox, etc.)?
A) 0–1 days → Well controlled → Reinforce lifestyle, continue PRN.
B) 2–3 days → Mildly symptomatic → Consider checking food/sleep triggers.
C) 4+ days → Increasing frequency → Reassess severity → consider PPI trial (switch to Profile 2).

1-2. How often did your symptoms interfere with daily life or sleep?
A) Never → Stable → No change.
B) Once or twice → Monitor → Maintain the same treatment.
C) Several times → Functional impact emerging → Step up to Profile 2.

1-3. Have you noticed any new symptoms since starting lifestyle changes?
A) No → Good response
B) Yes – Night symptoms → Flag for Profile 3.
C) Yes – Nausea or dysphagia → Alarm Features check.

Day 14 Follow-Up

1-4. Compared to before treatment, how would you rate symptom improvement?
A) >75% improvement → Effective control → Continue lifestyle + PRN antacid.
B) 30–75% → Partial response → Introduce famotidine or trial PPI.
C) <30% or worsening → Inadequate control → Escalate to Profile 2 or investigate.

1-5. Are you still using antacids >3x/week?
A) No → Control achieved
B) Yes → Add famotidine bedtime or move to PPI (start Profile 2).

1-6. Have you adhered to meal timing, portion control, and sleep posture advice?
A) Yes → Proceed based on symptom control
B) No → Re-emphasise counselling, reassess in 7 days.

Day 28 Follow-Up

1-7. Over the past 2 weeks, how many symptom-free days have you had without antacids?
A) >10 days → Consider tapering down follow-up
B) 5–10 days → Continue same plan
C) <5 days → Step up to Profile 2.

1-8. Are you currently requiring any night-time relief medication (famotidine or antacids)?
A) No → Maintain PRN status
B) Yes → Review for nocturnal GERD → Profile 3.

1-9. Have you experienced any weight change, vomiting, black stools, or new difficulty swallowing?
A) No → Continue plan
B) Yes → Alarm Features triggered → Urgent referral.



Next Steps Based on Day 28 Evaluation:

If well controlled → Discharge to annual review.

If moderate symptoms persist → Escalate to Profile 2.

If new alarm symptoms emerge → Switch to Profile 5.


DOSING PROFILE 2: MODERATE CLASSIC GERD
Target: Patients with daily or near-daily symptoms, burning, sour taste, known reflux triggers, sleep disturbance.
Triggering Answers:
Q4: A or E
Q6: 5–7
Q7: C–D
Q9: A–C
Q12: C or D

Q13: B or C

Q15: B helped or F (no therapy tried)
Alarm and Cardiac: All NO
Recommendation: Omeprazole 20 mg morning × 14 days only (per FDA OTC limit) + lifestyle changes + diary. Reassess at Day 14. No further PPI extension unless transitioned to Rx-based care.


Day 7 Follow-Up

2-1. Have you taken your PPI medication daily as prescribed?
A) Yes, every day before breakfast → Proceed to 2-2.
B) Missed a few doses → Reinforce adherence, reassess in 7 days.
C) Inconsistent intake (e.g. taken at night, irregularly) → Re-educate on dosing time.

2-2. How would you describe your symptoms compared to Day 0?
A) Much improved → Continue PPI plan.
B) Mild improvement → Monitor; emphasise trigger avoidance.
C) No change or worse → Flag for Profile 4 (non-PPI responsive or functional dyspepsia).

2-3. Are you still needing rescue antacids in addition to PPI?
A) No → Good response.
B) Yes, 1–2x/week → Acceptable early response.
C) Yes, >3x/week → Consider step up to BID dosing or alternate diagnosis.

Day 14 Follow-Up

2-4. On most days, are your symptoms:
A) Absent or barely noticeable → STOP PPI, switch to lifestyle + PRN antacid.
B) Present but manageable → STOP PPI, offer H2RA bedtime × 7–10 days if nocturnal.
C) Severe or unchanged → Transition to Profile 4 and refer for evaluation.

2-5. Any new onset of alarm symptoms since starting treatment?
A) No → Continue observation off PPI.
B) Yes → Switch to alarm protocol (Profile 5).

2-6. Do you feel your symptoms return in the evening or night?
A) No → Complete 14-day PPI course, no further acid suppression.
B) Yes → Offer famotidine bedtime × 7–10 days maximum; reassess.

Step-Down Plan – Profile 2
Omeprazole must not exceed 14 days (FDA-compliant).
After 14 days: If symptom-free → Discontinue all medications.
If mild symptoms persist → PRN antacids OR bedtime H2RA for ≤10 days.
If symptoms rebound or worsen → Flag for Profile 3 or 4.
No continuous acid suppression without physician-supervised prescription.





Dosing Profile 3: Nocturnal / Positional GERD (PPI + HOB Elevation + H2RA HS)

Target: Patients with nighttime symptoms, lying-down reflux, choking/regurgitation at night, positional exacerbation.
Triggering Answers:
Q4: A or EQ9: A or BQ11: A, DQ13: AQ15: A, B, or FAlarm and Cardiac: All NO

Recommendation: Omeprazole 20 mg AM × 14 days + Famotidine 10–20 mg bedtime × 14 days + strict head-of-bed elevation + lifestyle.

Day 7 Follow-Up
3-1. Are you elevating the head of the bed (pillow wedge or risers)?
A) Yes → Proceed.
B) No → Re-educate on positional therapy.

3-2. Have you taken both PPI (morning) and famotidine (bedtime) daily?
A) Yes → Continue.
B) Missed doses or incorrect timing → Reinforce timing.

3-3. Are night-time symptoms (cough, choking, sour taste) improved?
A) Yes → Continue.
B) Partial → Emphasise posture, avoid late meals
C) No → Consider non-acid reflux → move to Profile 4.

Day 14 Follow-Up

3-4. Are your symptoms now absent during sleep?
A) Yes → Discontinue both medications, continue posture.
B) Mild occasional symptoms → Discontinue medications, consider PRN H2RA only.
C) Persistent symptoms → Switch to Profile 4 (evaluate non-acid or delayed clearance).

3-5. Any side effects from either drug?
A) No → Proceed.
B) Yes → Discuss alternative regimens.

Step-Down Plan – Profile 3

PPI + H2RA combo must stop at 14 days per OTC regulations.
If night symptoms resolve → Continue only lifestyle + posture.

If mild relapse → PRN antacids 
Persistent symptoms → Evaluate for dual pathology or Profile 4.
No extended daily PPI/H2RA use unless under prescription.




DOSING PROFILE 4: SUSPECTED FUNCTIONAL / REFRACTORY GERD
Target: Patients with persistent symptoms despite correct PPI use, poor PPI response, or overlapping dyspepsia/IBS traits.
Triggering Answers:
Q4: A or C with minimal improvement to PPIs
Q6: 5–10 even after 7–14 days of therapy
Q15: Tried multiple treatments without success
Q18: No symptom-free periods
Day 14 from Profile 2 or 3: Response = "C" (unchanged) Alarm and Cardiac: All NO
Recommendation: Discontinue PPI/H2RA per FDA OTC limits. Refer to gastroenterology for:
pH monitoring
Impedance testing
Functional dyspepsia workup
Offer interim relief:
Simethicone or alginate-based agents
Dietary reprogramming (low-FODMAP.)
Follow-Up Questions for Profile 4
4-1. Have you undergone formal endoscopy or pH probe in the past 12 months?
A) Yes, normal → Likely functional → Diet and stress route.
B) Yes, abnormal (erosive) → May need Rx PPI.
C) No → Schedule pH study and endoscopy.
4-2. Do your symptoms worsen with stress or meals rich in fibre/fermentables?
A) Yes → Trial low-FODMAP + consider SSRI or SNRI.
B) No clear pattern → Continue symptom diary.
C) Worse with specific meals only → Dietitian referral.
4-3. Are you willing to pursue prescription therapy or specialist referral?
A) Yes → Initiate GI referral, hold acid suppression.
B) No → Reinforce non-drug therapy (e.g. posture, food, simethicone).


DOSING PROFILE 5: RED FLAG OR NON-GERD DIAGNOSIS PATH
Target: Patients presenting with any alarm features, red flags, or atypical patterns suggesting malignancy, bleeding, or severe systemic illness.
Triggering Answers:
Any "Yes" in Alarm Feature Section (Q19–Q27)
New or worsening symptoms + weight loss, bleeding, dysphagia, or odynophagia
Immunocompromised state or iron-deficiency anaemia
Recommendation:
Immediate GI referral → upper endoscopy (EGD) within 2 weeks
Lab tests: CBC, LFTs, ferritin, BUN/Cr
Stop all OTC PPI/H2RA until workup complete
Triage Priority:
Haematemesis / melena → ED or urgent EGD within 48 hrs
Progressive dysphagia → Urgent endoscopy + biopsy
5% weight loss + alarm → 14-day cancer pathway
Family history of GI cancer → expedited scope
Initial Management Guidance – Profile 5
Reassure patient and escalate safely to GI specialist
Offer antacid for temporary relief ONLY if no active bleeding/vomiting
Document alarm features and duration clearly
Step-Down / Re-entry Plan – Profile 5
If scope and labs return negative → Reassess for functional GERD or Profile 4
If pathology confirmed → Follow oncology/gastroenterology management
Do not reintroduce PPI/H2RA without clear plan from specialist
