import csv
import sys
import os

# Category weight requirements
TOTAL_WEIGHT = 100
SUMMATIVE_WEIGHT = 40
FORMATIVE_WEIGHT = 60
PASS_MARK = 50  # minimum % required in each category


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print(f"Error: The file '{filename}' is empty. Nothing to process.")
                sys.exit(1)

            required = {'assignment', 'group', 'score', 'weight'}
            if not required.issubset(set(reader.fieldnames)):
                print("Error: CSV is missing one or more required columns "
                      "(assignment, group, score, weight).")
                sys.exit(1)

            for line_no, row in enumerate(reader, start=2):
                if all((v is None or str(v).strip() == "") for v in row.values()):
                    continue
                try:
                    assignments.append({
                        'assignment': row['assignment'].strip(),
                        'group': row['group'].strip(),
                        'score': float(row['score']),
                        'weight': float(row['weight'])
                    })
                except (ValueError, TypeError, AttributeError):
                    print(f"Error: Invalid data on line {line_no}. "
                          f"'score' and 'weight' must be numbers.")
                    sys.exit(1)

        if not assignments:
            print("Error: The file contains no grade records to process.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def validate_scores(data):
    """a) Ensure every score is within the 0-100 range."""
    ok = True
    for item in data:
        if not (0 <= item['score'] <= 100):
            print(f"  [INVALID SCORE] {item['assignment']}: {item['score']} "
                  f"is outside the 0-100 range.")
            ok = False
    return ok


def validate_weights(data):
    """b) Verify total weights (Total=100, Summative=40, Formative=60)."""
    total = sum(i['weight'] for i in data)
    summative = sum(i['weight'] for i in data if i['group'].lower() == 'summative')
    formative = sum(i['weight'] for i in data if i['group'].lower() == 'formative')

    ok = True
    if total != TOTAL_WEIGHT:
        print(f"  [WEIGHT ERROR] Total weight is {total}, must be {TOTAL_WEIGHT}.")
        ok = False
    if summative != SUMMATIVE_WEIGHT:
        print(f"  [WEIGHT ERROR] Summative weight is {summative}, must be {SUMMATIVE_WEIGHT}.")
        ok = False
    if formative != FORMATIVE_WEIGHT:
        print(f"  [WEIGHT ERROR] Formative weight is {formative}, must be {FORMATIVE_WEIGHT}.")
        ok = False
    return ok


def category_percentage(data, group):
    """Weighted percentage achieved within a single category."""
    items = [i for i in data if i['group'].lower() == group.lower()]
    weight_sum = sum(i['weight'] for i in items)
    if weight_sum == 0:
        return 0.0
    earned = sum(i['score'] * i['weight'] for i in items)
    return earned / weight_sum


def evaluate_grades(data):
    """
    Runs validation, computes GPA, decides Pass/Fail, and reports resubmission.
    """
    print("\n--- Processing Grades ---")

    scores_ok = validate_scores(data)
    weights_ok = validate_weights(data)

    if not (scores_ok and weights_ok):
        print("\nValidation failed. Please fix the errors above before grading.")
        return

    total_grade = sum(i['score'] * i['weight'] for i in data) / TOTAL_WEIGHT
    gpa = (total_grade / 100) * 5.0

    formative_pct = category_percentage(data, 'Formative')
    summative_pct = category_percentage(data, 'Summative')

    passed = formative_pct >= PASS_MARK and summative_pct >= PASS_MARK
    status = "PASSED" if passed else "FAILED"

    failed_formative = [i for i in data
                        if i['group'].lower() == 'formative' and i['score'] < PASS_MARK]
    resubmission = []
    if failed_formative:
        max_weight = max(i['weight'] for i in failed_formative)
        resubmission = [i for i in failed_formative if i['weight'] == max_weight]

    print("\n================ TRANSCRIPT ================")
    print(f"{'Assignment':<38}{'Group':<12}{'Score':>7}{'Weight':>8}")
    print("-" * 65)
    for i in data:
        print(f"{i['assignment']:<38}{i['group']:<12}{i['score']:>7.1f}{i['weight']:>8.1f}")
    print("-" * 65)
    print(f"Formative Score : {formative_pct:.2f}%  (Pass mark {PASS_MARK}%)")
    print(f"Summative Score : {summative_pct:.2f}%  (Pass mark {PASS_MARK}%)")
    print(f"Final Grade     : {total_grade:.2f}%")
    print(f"GPA             : {gpa:.2f} / 5.0")
    print(f"Final Status    : {status}")

    if not passed and resubmission:
        print("\n--- Resubmission Eligibility ---")
        for r in resubmission:
            print(f"  Eligible: {r['assignment']} "
                  f"(score {r['score']:.1f}, weight {r['weight']:.1f})")
    elif passed:
        print("\nNo resubmission required. Congratulations!")
    else:
        print("\nStudent failed but has no failed formative assignments to resubmit.")
    print("============================================")


if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
