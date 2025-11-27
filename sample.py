import streamlit as st
import sqlite3
import requests

st.title("Text-to-SQL Query App")

user_input = st.text_input("Enter your query in natural language:")

if st.button("Run Query"):
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()

    payload = {
        "model": "mistral:7b",
        "prompt": f"""
        You are an SQL generator.
        Convert natural language to valid SQLite SQL.
        Rules:
        - Output only the SQL query.
        - No explanations or markdown formatting.
        - Use correct SQLite syntax.
        - Always end the query with a semicolon.
        Question: {user_input}
        """,
        "stream": False
    }

    resp = requests.post("http://localhost:11434/api/generate", json=payload)
    sql_query = resp.json()["response"].strip()

    st.code(sql_query, language="sql")

    try:
        if sql_query.lower().startswith("select"):
            rows = cursor.execute(sql_query).fetchall()
            st.write("### Results")
            if rows:
                for r in rows:
                    st.write(r)
            else:
                st.info("No rows found.")
        else:
            cursor.execute(sql_query)
            conn.commit()
            st.success("✅ Query executed successfully.")
    except Exception as e:
        st.error(f"Error: {e}")

    conn.close()
