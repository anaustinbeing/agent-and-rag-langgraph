from langchain_core.agents import AgentFinish
import json
from custom_tools.agent_tools import search_tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain_core.utils.function_calling import convert_to_openai_function
from custom_tools.agent_tools import search_tool

import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), streaming=True)

# prompt = hub.pull('hwchase17/openai-functions-agent')


# functions = [convert_to_openai_function(search_tool())]

def run_query_tool(state: list):
    print('> run_query_tool')
    search_tool.description = search_tool.description.format(topic=state['topic'])
    print(search_tool.description)
    query_tool = llm.bind_tools([search_tool])


    # query_agent_runnable = create_openai_tools_agent(
    #     llm=llm,
    #     tools=[search_tool],
    #     prompt=prompt
    # )
    query_tool_out = query_tool.invoke(state['input'])
    return {'query_tool_out': query_tool_out}


def execute_search(state: list):
    print('> execute_search')
    action = state['query_tool_out']
    search_tool.description = search_tool.description.format(topic=state['topic'])
    tool_call = action.additional_kwargs['tool_calls'][-1]
    print('arguments: ', json.loads(tool_call['function']['arguments']))
    out = search_tool.invoke(
        json.loads(tool_call['function']['arguments'])
    )
    return {'intermediate_steps': [{'search': str(out)}]}
