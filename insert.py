import sqlite3

# Connect to database
conn = sqlite3.connect("mydb.db")
a = conn.cursor()

# Insert 5 sample users
users_data = [
    ("Arun", 101, "Chennai"),
    ("Meena", 102, "Trichy"),
    ("Karthik", 103, "Madurai"),
    ("Priya", 104, "Coimbatore"),
    ("Suresh", 105, "Salem")
]

a.executemany("INSERT INTO users (name, roll, city) VALUES (?, ?, ?)", users_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Inserted 5 rows into users table successfully!")
