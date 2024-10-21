from custom_tools.agent_tools import output_tool
import os
from dotenv import load_dotenv
from graph_utils.query_runner import llm

load_dotenv()


final_answer_llm = llm.bind_tools([output_tool], tool_choice='final_output')

def rag_final_answer(state: list):
    print('> final_answer')
    query = state['input']
    context = state['intermediate_steps'][-1]

    prompt = f'''You are a helpful assistant that writes a 2-3 sentences to answer the user's question using the 'ANSWER' provided.
    Strictly refer to the 'ANSWER' when providing answer.
    QUESTION: {query}
    ANSWER: {context['search']}
    '''
    out = final_answer_llm.invoke(prompt)
    function_call = out.additional_kwargs['tool_calls'][-1]['function']['arguments']
    return {'agent_out': function_call}

def handle_error(state: list):
    print('> handle_error')
    query = state['input']
    prompt = f'''You are a helpful assistant. You could not find answer to this question.
    Politely reply that you do not have information outside the topic: {state['topic']}.
    QUESTION: {query}
    '''
    out = final_answer_llm.invoke(prompt)
    function_call = out.additional_kwargs['tool_calls'][-1]['function']['arguments']
    return {'agent_out': function_call}
