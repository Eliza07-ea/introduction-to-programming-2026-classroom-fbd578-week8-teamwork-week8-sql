import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)

    language_count = {}
    for row in reader:
        language = row["language"].strip()
        if language in language_count:
            language_count[language] += 1
        else:
            language_count[language] = 1

with open("language_summary.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["language", "votes"])
    writer.writeheader()
    for language, votes in sorted(language_count.items(), key=lambda x: x[1], reverse=True):
        writer.writerow({"language": language, "votes": votes})

print("language_summary.csv created!")
