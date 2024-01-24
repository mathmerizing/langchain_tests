# This code is based on the official langchain documentation: https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf
import os
import bs4
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


import warnings
warnings.filterwarnings('ignore')

# download PDF from https://raw.githubusercontent.com/mathmerizing/MultigridPython/master/BPX%26HB%20Ausarbeitung.pdf
if not os.path.exists("BPX_and_HB.pdf"):
    with open("BPX_and_HB.pdf", 'wb') as f:
        f.write(requests.get("https://raw.githubusercontent.com/mathmerizing/MultigridPython/master/BPX%26HB%20Ausarbeitung.pdf").content)

# load PDF and split into pages
loader = PyPDFLoader("BPX_and_HB.pdf")
#pages = loader.load_and_split()
docs = loader.load()

# faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
# docs = faiss_index.similarity_search("What does HB stand for?", k=1)
# for doc in docs:
#     print(str(doc.metadata["page"]) + ":", doc.page_content[:300])

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the multigrid documentation.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
# print("Prompt: ", prompt)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

format_docs = lambda docs: "\n\n".join(doc.page_content for doc in docs)

# retrieval and generation (RAG) chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

more_questions = input("Do you have any questions? (y/n): ")
while more_questions == "y":
    question = input("Question: ")
    print(f"Answer:   {rag_chain.invoke(question)}")
    more_questions = input("Do you have any more questions? (y/n): ")

# cleanup
vectorstore.delete_collection()


