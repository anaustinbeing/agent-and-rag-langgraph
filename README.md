# RAG with LangGraph

This project uses LangGraph to manage RAG workflow.

The following is the working:

1. User input is validated to see if it is matching the pdf file content.
2. If it is matching, it finds the relevant results from the vector store using similarity search, passes the results to LLM to get response to send to user.
3. If it is not matching, it returns that it cannot answer questions outside the context of the topic.

## Nodes

tool_out (START node) - This node performs tool calling and identifies the tool (function) that needs to be called and the arguments based on the user query. This information will be used to decide whether we move to the search or error node.

search - Performs similarity search and returns the matching documents.

error - If there is no tool calling identified by the start node, error node will run.

rag_final_answer - the output of search node is fed to LLM to form reponse for user.

END node


![image](https://github.com/user-attachments/assets/641cd11d-4bb4-4178-acac-bfa3c84a8132)
