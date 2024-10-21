from langchain_core.tools import tool

import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 

load_dotenv()

doc_reader = PdfReader('content/pdf_file.pdf')

raw_text = ''
for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts, embeddings)


# Define search tool for querying similar records
@tool('search')
def search_tool(query: str):
    '''This tool only gives details about {topic}.
    Call this tool only when asked about {topic}.'''
    return docsearch.similarity_search(query)
