# import streamlit as st
# import sqlite3
# import requests

# st.title("Text-to-SQL Query App")

# user_input = st.text_input("Enter your query in natural language:")

# if st.button("Run Query"):
#     conn = sqlite3.connect("mydb.db")
#     cursor = conn.cursor()

#     # Call Ollama
#     payload = {
#         "model": "mistral:7b",
#         "prompt": f"""You are an SQL generator.
#         Convert natural language to SQL for SQLite.
#         Rules: Only output SQL query, no explanation, no backticks.
#         Question: {user_input}""",
#         "stream": False
#     }
#     resp = requests.post("http://localhost:11434/api/generate", json=payload)
#     sql_query = resp.json()["response"].strip()

#     st.code(sql_query, language="sql")

#     try:
#         if sql_query.lower().startswith("select"):
#             rows = cursor.execute(sql_query).fetchall()
#             st.write("### Results")
#             if rows:
#                 for r in rows:
#                     st.write(r)
#             else:
#                 st.info("No rows found.")
#         else:
#             cursor.execute(sql_query)
#             conn.commit()
#             st.success("✅ Query executed successfully.")
#     except Exception as e:
#         st.error(f"Error: {e}")

#     conn.close()

import sqlite3
import requests

def main():
    print("=== Text-to-SQL Query App (Terminal Version) ===")

    while True:
        user_input = input("\nEnter your query in natural language (or type 'exit' to quit): ")

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break

        conn = sqlite3.connect("mydb.db")
        cursor = conn.cursor()

        # Call Ollama (local Mistral model)
        payload = {
            "model": "mistral:7b",
            "prompt": f"""
            You are an SQL generator.
            Convert natural language to valid SQLite SQL.
            Rules:
            - Output only the SQL query, no explanations, no markdown, no backticks.
            - Use correct SQLite syntax.
            - Avoid invalid commands like DELETE DISTINCT.
            - Always end with a semicolon.
            Question: {user_input}
            """,
            "stream": False
        }

        try:
            # Call local Ollama API
            resp = requests.post("http://localhost:11434/api/generate", json=payload)
            sql_query = resp.json()["response"].strip()

            print("\nGenerated SQL Query:")
            print("------------------------------------------------")
            print(sql_query)
            print("------------------------------------------------")

            # Execute query
            command = sql_query.lower().split()[0]

            if command == "select":
                rows = cursor.execute(sql_query).fetchall()
                if rows:
                    print("\nResults:")
                    for r in rows:
                        print(r)
                else:
                    print("\nNo rows found.")
            else:
                cursor.execute(sql_query)
                conn.commit()
                print("\n✅ Query executed successfully.")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        finally:
            conn.close()

if __name__ == "__main__":
    main()
