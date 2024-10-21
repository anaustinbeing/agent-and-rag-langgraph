# RAG with LangGraph

This project uses LangGraph to manage RAG workflow.

The following is the working:

1. User input is validated to see if it is matching the pdf file content.
2. If it is matching, it finds the relevant results from the vector store using similarity search, passes the results to LLM to get response to send to user.
3. If it is not matching, it returns that it cannot answer questions outside the context of the topic.

## Nodes

query_agent (START node) - An agent which returns `ToolAgentAction` specifying the function calls. This information will be used to decide whether we move to the search or END node.

search - Performs similarity search and returns the matching documents.

error - If there is no match found by the start node.

rag_final_answer - the output of search node is fed to LLM to form reponse for user.

END node


![image](https://github.com/user-attachments/assets/641cd11d-4bb4-4178-acac-bfa3c84a8132)
