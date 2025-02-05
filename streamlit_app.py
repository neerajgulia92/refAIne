import streamlit as st
from PIL import Image
import os
import boto3
import json
import uvicorn
from fastapi import FastAPI, HTTPException
import threading
import requests

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="ref[AI]ne - SQL Code Quality Tool", layout="wide")

# Path for logo
image_path = "logo.png"

# Check if the logo exists
if os.path.exists(image_path):
    logo = Image.open(image_path)
    st.image(logo, use_container_width=True)
else:
    st.warning(f"Logo image not found at {image_path}. Please ensure the file exists.")

# Initialize AWS Bedrock Client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

# FastAPI App
app = FastAPI()

# Function to Call AWS Claude Model
def call_claude_api(sql_code, task_type):
    prompt = f"Task: {task_type}\n\nSQL Code:\n{sql_code}\n\nProvide the response accordingly."
    kwargs = {
        "modelId": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "top_k": 250,
            "stop_sequences": [],
            "temperature": 1,
            "top_p": 0.999,
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        })
    }
    try:
        response = bedrock_runtime.invoke_model(**kwargs)
        body = json.loads(response['body'].read())
        return {"output": body["content"][0]["text"]}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}

# FastAPI Endpoints
@app.post("/fix_syntax/")
async def fix_syntax(data: dict):
    sql_code = data.get("sql_code", "")
    if not sql_code:
        raise HTTPException(status_code=400, detail="SQL code is required")
    return call_claude_api(sql_code, "fix_syntax")

@app.post("/standardize/")
async def standardize(data: dict):
    sql_code = data.get("sql_code", "")
    if not sql_code:
        raise HTTPException(status_code=400, detail="SQL code is required")
    return call_claude_api(sql_code, "standardize_code")

@app.post("/optimize/")
async def optimize(data: dict):
    sql_code = data.get("sql_code", "")
    if not sql_code:
        raise HTTPException(status_code=400, detail="SQL code is required")
    return call_claude_api(sql_code, "optimize_sql")

@app.post("/document/")
async def document(data: dict):
    sql_code = data.get("sql_code", "")
    if not sql_code:
        raise HTTPException(status_code=400, detail="SQL code is required")
    return call_claude_api(sql_code, "generate_documentation")

# Start FastAPI Server in a Separate Thread
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8502)  # Run on port 8502

threading.Thread(target=run_fastapi, daemon=True).start()

# Streamlit UI
st.title("SQL Code Quality Improvement Tool")
st.subheader("Paste your SQL code here:")
user_sql_code = st.text_area("", height=300)

# Function to Call FastAPI from Streamlit
def fetch_from_api(endpoint, sql_code):
    try:
        response = requests.post(f"http://127.0.0.1:8502/{endpoint}/", json={"sql_code": sql_code})
        return response.json().get("output", "Error processing request")
    except Exception as e:
        return f"Error: {str(e)}"

# Buttons for Actions
if st.button("Fix Syntax Errors"):
    st.subheader("Fixed SQL Code:")
    st.code(fetch_from_api("fix_syntax", user_sql_code), language="sql", line_numbers=True)

if st.button("Standardize Code"):
    st.subheader("Standardized SQL Code:")
    st.code(fetch_from_api("standardize", user_sql_code), language="sql", line_numbers=True)

if st.button("Generate Documentation"):
    st.subheader("Generated Documentation:")
    st.markdown(fetch_from_api("document", user_sql_code))

if st.button("Optimize SQL Code"):
    st.subheader("Optimized SQL Code:")
    st.code(fetch_from_api("optimize", user_sql_code), language="sql", line_numbers=True)
