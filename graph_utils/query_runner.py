from langchain_core.agents import AgentFinish
import json
from custom_tools.agent_tools import search_tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from custom_tools.agent_tools import output_tool, search_tool

import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), temperature=0)

prompt = hub.pull('hwchase17/openai-functions-agent')


# Create the agent runnable with the tools and prompt


def run_query_agent(state: list):
    print('> run_query_agent')
    search_tool.description = search_tool.description.format(topic=state['topic'])
    query_agent_runnable = create_openai_tools_agent(
        llm=llm,
        tools=[search_tool, output_tool],
        prompt=prompt
    )
    agent_out = query_agent_runnable.invoke(state)  # Using query_agent_runnable here
    return {'agent_out': agent_out}

# def run_query_agent(state: list, query_agent_runnable):
#     print('> run_query_agent')
#     agent_out = query_agent_runnable.invoke(state)
#     return {'agent_out': agent_out}

def execute_search(state: list):
    print('> execute_search')
    action = state['agent_out']
    search_tool.description = search_tool.description.format(topic=state['topic'])
    tool_call = action[-1].message_log[-1].additional_kwargs['tool_calls'][-1]
    out = search_tool.invoke(
        json.loads(tool_call['function']['arguments'])
    )
    return {'intermediate_steps': [{'search': str(out)}]}
