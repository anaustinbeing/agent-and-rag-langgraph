from langgraph.graph import StateGraph, END
from graph_utils.query_runner import run_query_tool, execute_search
from graph_utils.state import rag_final_answer, handle_error
from agent_state import AgentState
from dotenv import load_dotenv

load_dotenv()

def router_one(state: list):
    print('> router')
    try:
        tool_calls = state['query_tool_out'].additional_kwargs['tool_calls']
        return tool_calls[-1]["function"]["name"]
    except KeyError:
        return 'error'
    

def build_graph():
    graph = StateGraph(AgentState)

    # Define the nodes
    graph.add_node('tool_out', run_query_tool)
    graph.add_node('search', execute_search)
    graph.add_node('error', handle_error)
    graph.add_node('rag_final_answer', rag_final_answer)

    # Set entry point
    graph.set_entry_point('tool_out')

    # Add conditional edges
    graph.add_conditional_edges(
        start_key='tool_out',
        condition=router_one,
        conditional_edge_mapping={
            'search': 'search',
            'error': 'error'
        }
    )

    graph.add_edge('search', 'rag_final_answer')
    graph.add_edge('error', END)
    graph.add_edge('rag_final_answer', END)

    return graph.compile()
