from langgraph.graph import StateGraph, START
from langchain_aws import ChatBedrock
from langchain_core.messages import SystemMessage, HumanMessage
from typing_extensions import TypedDict

llm = ChatBedrock(
    credentials_profile_name="default", model_id="anthropic.claude-3-5-sonnet-20240620-v1:0"
)

# Define the Graph State
class SQLState(TypedDict):
    user_input: str
    response: str


def fix_sql_code(state: SQLState) -> SQLState:
    """Get the SQL code from the user."""
    system_message = SystemMessage("You are an expert at SQL. IF the user input is a SQL code, THEN fix the syntax errors. If not, respond with 'Please provide SQL code.'")
    messages = [system_message, HumanMessage(state["user_input"])]
    return {"response": llm.invoke(messages)}

# Create a LangGraph
workflow = StateGraph(SQLState).add_sequence([fix_sql_code])
workflow.add_edge(START, 'fix_sql_code')

# Compile the Graph
syntax_fix_graph = workflow.compile()

# print(syntax_fix_graph.invoke({"user_input": "select * from table column=value"})['response'].content)
# print(syntax_fix_graph.invoke({"user_input": "fix the following sql select * from table column=value"})['response'].content)