import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)

    frequency = {}
    for row in reader:
        title = row["title"].strip()
        if title in frequency:
            frequency[title] += 1
        else:
            frequency[title] = 1

minimum = int(input("Minimum votes: "))

print(f"\nTitles with at least {minimum} vote(s):")
for title, count in sorted(frequency.items(), key=lambda x: x[1], reverse=True):
    if count >= minimum:
        print(f"{title}: {count}")
