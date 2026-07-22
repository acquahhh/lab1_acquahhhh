# Lab 1: Grade Evaluator & Archiver

A Python application that computes a student's final academic standing from a CSV
of course grades, plus a Bash script that archives and resets the grades file.

## Repository Contents

| File | Description |
|------|-------------|
| `grade-evaluator.py` | Reads `grades.csv`, validates it, computes GPA, decides Pass/Fail, and reports resubmission eligibility. |
| `organizer.sh` | Archives `grades.csv` with a timestamp, resets the workspace with a fresh empty file, and logs every run. |
| `grades.csv` | Sample grade data. |
| `Readme.md` | This file. |

## Requirements

- Python 3.x
- A Bash shell (Linux, macOS, or WSL on Windows)

## 1. Running the Python Application

```bash
python3 grade-evaluator.py
```

When prompted, enter the CSV filename:

```
Enter the name of the CSV file to process (e.g., grades.csv): grades.csv
```

### What it does

- **Score validation** — every score must be between 0 and 100.
- **Weight validation** — weights must total **100**, with **Formative = 60** and **Summative = 40**.
- **GPA** — `GPA = (Total Grade / 100) * 5.0`.
- **Pass/Fail** — a student passes only with **≥ 50% in BOTH** the Formative and Summative categories.
- **Resubmission** — if the student failed, the failed formative assignment(s) with the **highest weight** are listed. Ties are all shown.

### CSV format

```csv
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20
```

`group` must be either `Formative` or `Summative`.

### Edge cases handled

- Missing file → clear error, no crash.
- Empty file (e.g. the one left by `organizer.sh`) → clear error, no crash.
- Non-numeric score/weight → reports the offending line.
- Scores out of range or weights not matching the 60/40/100 split → reported before grading stops.

## 2. Running the Shell Script

Make it executable once, then run it:

```bash
chmod +x organizer.sh
./organizer.sh
```

### What it does

1. Creates an `archive/` directory if one does not exist.
2. Generates a timestamp (`YYYYMMDD-HHMMSS`).
3. Moves `grades.csv` into `archive/` renamed as `grades_<timestamp>.csv`.
4. Creates a fresh, empty `grades.csv` in the current directory.
5. Appends a record of the operation to `organizer.log` (entries accumulate across runs).

### Example

```
Created archive directory: archive
Archived 'grades.csv' -> 'archive/grades_20251105-170000.csv'
Created a fresh empty 'grades.csv'.
Logged operation to 'organizer.log'.
```

Sample `organizer.log` entry:

```
[20251105-170000] Original: grades.csv | Archived as: archive/grades_20251105-170000.csv
```

## Typical Workflow

```bash
# 1. Grade the current batch
python3 grade-evaluator.py

# 2. Archive it and reset for the next batch
./organizer.sh

# 3. Add the next batch of grades into the fresh grades.csv, repeat.
```
