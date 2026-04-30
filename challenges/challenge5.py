import csv

issues = 0
cleaned = []

with open("messy_data.csv", "r") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames

    for i, row in enumerate(reader, start=2):
        row_issues = []

        # Fix leading/trailing whitespace in all fields
        row = {key: value.strip() for key, value in row.items()}

        # Check for empty fields
        for field, value in row.items():
            if value == "":
                row_issues.append(f"row {i}: missing '{field}'")
                row[field] = "N/A"

        # Check for duplicate rows
        if row in cleaned:
            row_issues.append(f"row {i}: duplicate row removed")
            issues += len(row_issues)
            continue

        # Normalize email to lowercase
        if "email" in row and row["email"] != "N/A":
            row["email"] = row["email"].lower()

        # Normalize name to title case
        if "name" in row and row["name"] != "N/A":
            row["name"] = row["name"].title()

        # Validate age is a number
        if "age" in row:
            try:
                age = int(row["age"])
                if age < 0 or age > 120:
                    row_issues.append(f"row {i}: age '{age}' out of range, set to N/A")
                    row["age"] = "N/A"
            except ValueError:
                row_issues.append(f"row {i}: age '{row['age']}' is not a number, set to N/A")
                row["age"] = "N/A"

        for msg in row_issues:
            print(f"ISSUE — {msg}")

        issues += len(row_issues)
        cleaned.append(row)

with open("cleaned_data.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned)

print(f"\n--- Report ---")
print(f"Cleaned rows written: {len(cleaned)}")
print(f"Total issues found:   {issues}")
print("Output saved to cleaned_data.csv")
