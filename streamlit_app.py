import streamlit as st
import boto3
import json

# Initialize Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

# Function to call Claude AI via AWS Bedrock
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
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        })
    }

    try:
        response = bedrock_runtime.invoke_model(**kwargs)
        body = json.loads(response['body'].read())
        return {"output": body["content"][0]["text"]}
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return {"output": "Error processing request"}

# Streamlit UI
st.title("ref[AI]ne: SQL Code Quality Improvement Tool")
st.subheader("Paste your SQL code here:")

# SQL Code Input
user_sql_code = st.text_area("", height=300)

# Buttons for actions
if st.button("Fix Syntax Errors"):
    response = call_claude_api(user_sql_code, "fix_syntax")
    st.subheader("Fixed SQL Code:")
    st.code(response.get("output", "Error processing request"), language="sql", line_numbers=True)

if st.button("Standardize Code"):
    response = call_claude_api(user_sql_code, "standardize_code")
    st.subheader("Standardized SQL Code:")
    st.code(response.get("output", "Error processing request"), language="sql", line_numbers=True)

if st.button("Generate Documentation"):
    response = call_claude_api(user_sql_code, "generate_documentation")
    st.subheader("Generated Documentation:")
    st.markdown(response.get("output", "Error processing request"))

if st.button("Optimize SQL Code"):
    response = call_claude_api(user_sql_code, "optimize_sql")
    st.subheader("Optimized SQL Code:")
    st.code(response.get("output", "Error processing request"), language="sql", line_numbers=True)