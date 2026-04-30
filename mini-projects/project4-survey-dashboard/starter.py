import csv
import sqlite3

conn = sqlite3.connect("survey.db")
db   = conn.cursor()

db.execute('''CREATE TABLE IF NOT EXISTS responses (
    student_id TEXT,
    faculty TEXT,
    year INTEGER,
    satisfaction INTEGER,
    favourite_tool TEXT,
    comments TEXT
)''')

csv_files = [
    "faculty_science.csv",
    "faculty_arts.csv",
    "faculty_business.csv",
]

for filename in csv_files:
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.execute("INSERT INTO responses VALUES (?, ?, ?, ?, ?, ?)", (
                row["student_id"],
                row["faculty"],
                int(row["year"]),
                int(row["satisfaction"]),
                row["favourite_tool"],
                row["comments"]
            ))

conn.commit()
print("Database loaded successfully.\n")

print("=" * 30)
print("  UNIVERSITY SURVEY DASHBOARD")
print("=" * 30)

print("\n1. Total Responses by Faculty")
rows = db.execute("SELECT faculty, COUNT(*) AS n FROM responses GROUP BY faculty ORDER BY faculty").fetchall()
total = 0
for row in rows:
    print(f"   {row[0]:<10}: {row[1]}")
    total += row[1]
print(f"   {'TOTAL':<10}: {total}")

print("\n2. Average Satisfaction by Year of Study")
rows = db.execute("SELECT year, ROUND(AVG(satisfaction), 1) AS avg_sat FROM responses GROUP BY year ORDER BY year").fetchall()
for row in rows:
    print(f"   Year {row[0]} : {row[1]} / 5")

print("\n3. Favourite Tool Popularity")
rows = db.execute("SELECT favourite_tool, COUNT(*) AS n FROM responses GROUP BY favourite_tool ORDER BY n DESC").fetchall()
for row in rows:
    print(f"   {row[0]:<15}: {row[1]:>3}")

print("\n4. Faculty Comparison")
print(f"   {'Faculty':<12} | {'Avg Satisfaction':<18} | Most Popular Tool")
print("   " + "-" * 50)

faculties = ["Arts", "Business", "Science"]
for faculty in faculties:
    avg_row = db.execute(
        "SELECT ROUND(AVG(satisfaction), 1) AS avg FROM responses WHERE faculty = ?",
        (faculty,)
    ).fetchone()

    tool_row = db.execute(
        "SELECT favourite_tool FROM responses WHERE faculty = ? GROUP BY favourite_tool ORDER BY COUNT(*) DESC LIMIT 1",
        (faculty,)
    ).fetchone()

    print(f"   {faculty:<12} | {str(avg_row[0]):<18} | {tool_row[0]}")

print()
try:
    min_score = int(input("Enter minimum satisfaction score (1-5): "))
except ValueError:
    print("Invalid input. Defaulting to 4.")
    min_score = 4

rows = db.execute(
    "SELECT student_id, faculty, year, favourite_tool FROM responses WHERE satisfaction >= ? ORDER BY faculty, year",
    (min_score,)
).fetchall()

print(f"\nStudents with satisfaction >= {min_score}:")
if not rows:
    print("  No results found.")
for row in rows:
    print(f"  {row[0]} | {row[1]:<10} | Year {row[2]} | {row[3]}")

conn.close()
