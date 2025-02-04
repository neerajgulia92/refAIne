import streamlit as st
import boto3
import json

# Initialize the Bedrock Runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

# Function to call Claude AI via AWS Bedrock
def call_claude_api(user_prompt):
    kwargs = {
        "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
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
                    "content": [
                        {"type": "text", "text": user_prompt}
                    ]
                }
            ]
        })
    }

    try:
        response = bedrock_runtime.invoke_model(**kwargs)
        body = json.loads(response['body'].read())
        return body  # Adjust as per Claude's response structure
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
st.title("ref[AI]ne: SQL Code Quality Improvement Tool")

# Text area for SQL code input
user_sql_code = st.text_area("Paste your SQL code here:", height=300)

# Button to process code with Claude
if st.button("Improve Code"):
    if user_sql_code.strip():
        response = call_claude_api(user_sql_code)
        if "error" in response:
            st.error(f"Error: {response['error']}")
        else:
            st.subheader("Optimized SQL Code:")
            st.code(response.get("output", "No response received"), language="sql")  # Adjust based on Claude's response structure
    else:
        st.warning("Please enter some SQL code.")
