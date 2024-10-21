from langgraph.graph import StateGraph, END
from graph_utils.query_runner import run_query_agent, execute_search
from graph_utils.state import rag_final_answer, handle_error
from agent_state import AgentState
import os
from dotenv import load_dotenv

load_dotenv()

def router_one(state: list):
    print('> router')
    if isinstance(state['agent_out'], list):
        return state['agent_out'][-1].tool
    else:
        return 'error'
    

def build_graph():
    graph = StateGraph(AgentState)

    # Define the nodes
    graph.add_node('query_agent', run_query_agent)
    graph.add_node('search', execute_search)
    graph.add_node('error', handle_error)
    graph.add_node('rag_final_answer', rag_final_answer)

    # Set entry point
    graph.set_entry_point('query_agent')

    # Add conditional edges
    graph.add_conditional_edges(
        start_key='query_agent',
        condition=router_one,
        conditional_edge_mapping={
            'search': 'search',
            'error': 'error',
            'final_output': END
        }
    )

    graph.add_edge('search', 'rag_final_answer')
    graph.add_edge('error', END)
    graph.add_edge('rag_final_answer', END)

    return graph.compile()
