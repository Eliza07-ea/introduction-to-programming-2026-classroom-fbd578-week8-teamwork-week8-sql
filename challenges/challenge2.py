import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)

    data = {}
    for row in reader:
        language = row["language"].strip()
        problem = row["problem"].strip()

        if language not in data:
            data[language] = {}

        if problem in data[language]:
            data[language][problem] += 1
        else:
            data[language][problem] = 1

print(f"{'Language':<20} {'Most Common Problem':<30} {'Votes'}")
print("-" * 55)

for language, problems in sorted(data.items()):
    top_problem = max(problems, key=problems.get)
    top_count = problems[top_problem]
    print(f"{language:<20} {top_problem:<30} {top_count}")
