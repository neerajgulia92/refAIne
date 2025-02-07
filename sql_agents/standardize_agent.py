from langgraph.graph import StateGraph, START
from langchain_aws import ChatBedrock
from langchain_core.messages import SystemMessage, HumanMessage
from typing_extensions import TypedDict

llm = ChatBedrock(
    credentials_profile_name="default", model_id="anthropic.claude-3-5-sonnet-20240620-v1:0"
)

# Define the Graph State
class SQLState(TypedDict):
    standard_documents: str
    user_input: str
    response: str

def get_standardization_docs(state: SQLState) -> SQLState:
    """Get the SQL code from the user."""
    standardization_docs = "SQL Commands need to be capitalized" # Add/get the standardization docs here
    return {"standard_documents": standardization_docs}


def standardize_sql_code(state: SQLState) -> SQLState:
    """Get the SQL code from the user."""
    system_message = SystemMessage("You are an expert at SQL. IF the user input is SQL code, THEN update the SQL code so that it complies with STANDARDS. If not, respond with 'Please provide SQL code.'")
    standardization_message = SystemMessage(f"\n\nSTANDARDS\n---\n{state['standard_documents']}")
    messages = [system_message, standardization_message, HumanMessage(state["user_input"])]
    return {"response": llm.invoke(messages)}

# Create a LangGraph
workflow = StateGraph(SQLState).add_sequence([get_standardization_docs, standardize_sql_code])
workflow.add_edge(START, 'get_standardization_docs')

# Compile the Graph
standardize_graph = workflow.compile()


# print(standardize_graph.invoke({"user_input": "select * from table"})['response'].content)
# print(standardize_graph.invoke({"user_input": "fix the following sql select * from table"})['response'].content)
