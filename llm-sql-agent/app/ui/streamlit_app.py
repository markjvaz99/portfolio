import streamlit as st
import requests
import pandas as pd

# 🔧 Config
API_URL = "http://api:8000/query"

st.set_page_config(page_title="LLM SQL Agent", layout="wide")

st.title("🧠 LLM SQL Agent")
st.write("Ask questions about your database")

# 📝 Input
query = st.text_input("Enter your query:", placeholder="e.g. Show all users")

if st.button("Run Query"):
    if not query.strip():
        st.warning("Please enter a query")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                data = response.json()

                # 🔍 Show SQL (debug/optional)
                with st.expander("Generated SQL"):
                    st.code(data.get("sql", ""), language="sql")

                result = data.get("data", {})

                # 🚨 Error handling
                if result.get("type") == "error":
                    st.error(result.get("message"))
                
                # 📊 Table rendering
                elif result.get("type") == "table":
                    columns = result.get("columns", [])
                    rows = result.get("rows", [])

                    if not rows:
                        st.info("No data found")
                    else:
                        df = pd.DataFrame(rows, columns=columns)
                        st.dataframe(df, use_container_width=True)

                        st.success(f"{result.get('row_count', 0)} rows returned")

                else:
                    st.warning("Unknown response type")

            except Exception as e:
                st.error(f"API Error: {str(e)}")