import json
import boto3
import uvicorn
from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_aws import ChatBedroc
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Optional, Annotated

# Initialize FastAPI App
app = FastAPI()

from langchain_aws import ChatBedrock

# Initialize AWS Bedrock Client
# bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

llm = ChatBedrock(
    credentials_profile_name="default", model_id="anthropic.claude-3-5-sonnet-20240620-v1:0"
)

# Define the Graph State
class SQLState:
    messages: Annotated[list, add_messages]
    sql_code: str
    response: Optional[str]

# Define a function to call Claude for SQL tasks
# def call_claude_api(sql_code, task_type):
#     prompt = f"Task: {task_type}\n\nSQL Code:\n{sql_code}\n\nProvide the response accordingly."
    
#     kwargs = {
#         "modelId": "anthropic.claude-3-5-sonnet-20240620-v1:0",
#         "contentType": "application/json",
#         "accept": "application/json",
#         "body": json.dumps({
#             "anthropic_version": "bedrock-2023-05-31",
#             "max_tokens": 200,
#             "top_k": 250,
#             "stop_sequences": [],
#             "temperature": 1,
#             "top_p": 0.999,
#             "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
#         })
#     }

#     try:
#         response = bedrock_runtime.invoke_model(**kwargs)
#         body = json.loads(response['body'].read())
#         return body["content"][0]["text"]
#     except Exception as e:
#         return f"Error: {str(e)}"

# Define LangGraph Tools
@tool
def fix_syntax(state: SQLState) -> SQLState:
    """Fix SQL syntax errors."""
    state["response"] = llm_with_tools.invoke(state["sql_code"])
    return state

@tool
def standardize_code(state: SQLState) -> SQLState:
    """Standardize SQL formatting."""
    state["response"] = llm_with_tools.invoke(state["sql_code"], "standardize_code")
    return state

@tool
def optimize_sql(state: SQLState) -> SQLState:
    """Optimize SQL queries."""
    state["response"] = llm_with_tools.invoke(state["sql_code"], "optimize_sql")
    return state

@tool
def generate_documentation(state: SQLState) -> SQLState:
    """Generate documentation for SQL code."""
    state["response"] = llm_with_tools.invoke(state["sql_code"], "generate_documentation")
    return state

def call_model(state:SQLState) -> SQLState:
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": messages+response, "sql_code": response}

# binding tools to node
tools = [fix_syntax, standardize_code, optimize_sql, generate_documentation]
sql_tools = ToolNode(tools=tools)
llm_with_tools = llm.bind_tools(tools)
# Create a LangGraph
workflow = StateGraph(SQLState)
workflow.add_node('agent', call_model)
workflow.add_node('sql_tools', sql_tools)
workflow.add_edge(START, 'agent')
workflow.add_conditional_edges('agent', tools_condition)
workflow.add_edge('sql_tools','agent')

# Define the Entry Point for Graph
workflow.set_entry_point("agent")

# Compile the Graph
graph = workflow.compile()

# FastAPI Endpoints to Trigger the Agent
# @app.post("/fix_syntax/")
# async def fix_syntax_endpoint(data: dict):
#     sql_code = data.get("sql_code", "")
#     if not sql_code:
#         raise HTTPException(status_code=400, detail="SQL code is required")
#     return graph.invoke({"sql_code": sql_code})

# @app.post("/standardize/")
# async def standardize_endpoint(data: dict):
#     sql_code = data.get("sql_code", "")
#     if not sql_code:
#         raise HTTPException(status_code=400, detail="SQL code is required")
#     return graph.invoke({"sql_code": sql_code})

# @app.post("/optimize/")
# async def optimize_endpoint(data: dict):
#     sql_code = data.get("sql_code", "")
#     if not sql_code:
#         raise HTTPException(status_code=400, detail="SQL code is required")
#     return graph.invoke({"sql_code": sql_code})

# @app.post("/document/")
# async def document_endpoint(data: dict):
#     sql_code = data.get("sql_code", "")
#     if not sql_code:
#         raise HTTPException(status_code=400, detail="SQL code is required")
#     return graph.invoke({"sql_code": sql_code})