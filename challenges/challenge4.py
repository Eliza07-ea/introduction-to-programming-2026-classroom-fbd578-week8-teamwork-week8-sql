import sqlite3

conn = sqlite3.connect("favorites.db")
db = conn.cursor()

while True:
    print("\n--- SQL Explorer ---")
    print("1. Count all responses")
    print("2. Show all languages")
    print("3. Most popular language")
    print("4. Most popular problem")
    print("5. Count by language")
    print("6. Count by problem")
    print("7. Search by language")
    print("8. Exit")

    choice = input("\nChoose an option (1-8): ").strip()

    if choice == "1":
        db.execute("SELECT COUNT(*) FROM favorites")
        print(f"Total responses: {db.fetchone()[0]}")

    elif choice == "2":
        db.execute("SELECT DISTINCT language FROM favorites ORDER BY language")
        for row in db.fetchall():
            print(row[0])

    elif choice == "3":
        db.execute("SELECT language, COUNT(*) AS n FROM favorites GROUP BY language ORDER BY n DESC LIMIT 1")
        row = db.fetchone()
        print(f"Most popular language: {row[0]} ({row[1]} votes)")

    elif choice == "4":
        db.execute("SELECT problem, COUNT(*) AS n FROM favorites GROUP BY problem ORDER BY n DESC LIMIT 1")
        row = db.fetchone()
        print(f"Most popular problem: {row[0]} ({row[1]} votes)")

    elif choice == "5":
        db.execute("SELECT language, COUNT(*) AS n FROM favorites GROUP BY language ORDER BY n DESC")
        for row in db.fetchall():
            print(f"{row[0]}: {row[1]}")

    elif choice == "6":
        db.execute("SELECT problem, COUNT(*) AS n FROM favorites GROUP BY problem ORDER BY n DESC")
        for row in db.fetchall():
            print(f"{row[0]}: {row[1]}")

    elif choice == "7":
        lang = input("Enter language: ").strip()
        db.execute("SELECT problem, COUNT(*) AS n FROM favorites WHERE language = ? GROUP BY problem ORDER BY n DESC", (lang,))
        rows = db.fetchall()
        if rows:
            for row in rows:
                print(f"{row[0]}: {row[1]}")
        else:
            print("No results found.")

    elif choice == "8":
        print("Goodbye!")
        break

    else:
        print("Invalid choice, try again.")

conn.close()
