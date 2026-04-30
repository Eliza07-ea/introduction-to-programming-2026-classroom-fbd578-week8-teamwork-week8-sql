import csv

scores = []
grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

highest = {"name": "", "score": -1}
lowest  = {"name": "", "score": 101}

with open("grades.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name  = row["name"]
        score = int(row["score"])

        scores.append(score)

        if score > highest["score"]:
            highest["name"] = name
            highest["score"] = score

        if score < lowest["score"]:
            lowest["name"] = name
            lowest["score"] = score

        if score >= 90:
            letter = "A"
        elif score >= 80:
            letter = "B"
        elif score >= 70:
            letter = "C"
        elif score >= 60:
            letter = "D"
        else:
            letter = "F"

        grade_counts[letter] += 1

average = round(sum(scores) / len(scores), 1)

print("=== Quiz Grade Summary ===")
print(f"{'Average score:':<20} {average}")
print(f"{'Highest score:':<20} {highest['score']} ({highest['name']})")
print(f"{'Lowest score:':<20} {lowest['score']} ({lowest['name']})")
print("\nGrade distribution:")
for letter, count in grade_counts.items():
    print(f"  {letter}: {count}")
