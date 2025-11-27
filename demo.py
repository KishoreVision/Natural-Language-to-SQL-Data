import sqlite3
import requests

conn = sqlite3.connect("mydb.db")
a = conn.cursor()

jsons = {
    "model": "mistral:7b",
    "prompt": "You are an SQL generator. Convert natural language to SQL queries for SQLite. Rules: - Output only the SQL query, no backticks, no code fences, no explanations. Question: Select all names from users table.",
    "stream": False
}

req = requests.post("http://localhost:11434/api/generate", json=jsons)

query = req.json()["response"].strip()
print("Generated Query:", query)

a.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        roll INTEGER,
        city TEXT
    )
""")

for row in a.execute(query):
    print(row)

conn.commit()
conn.close()
