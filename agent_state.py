# from pydantic import BaseModel, Field
# from typing import List, Union, Tuple
# from langchain_core.agents import AgentAction, AgentFinish


# class AgentState(BaseModel):
#     input: str
#     agent_out: Union[AgentAction, AgentFinish, None] = None
#     intermediate_steps: List[Tuple[AgentAction, str]] = Field(default_factory=list)

#     def add_step(self, action: AgentAction, result: str):
#         """Add an intermediate step to the state."""
#         self.intermediate_steps.append((action, result))


from typing import TypedDict, Annotated, List, Union
from langchain_core.agents import AgentAction, AgentFinish
import operator


class AgentState(TypedDict):
    topic: str
    input: str
    agent_out: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]