# This code is based on the official langchain documentation: https://python.langchain.com/docs/use_cases/question_answering/quickstart
import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import warnings
warnings.filterwarnings('ignore')

# Load, chunk and index the contents of the website on the multigrid documentation
loader = WebBaseLoader(
    web_paths=("https://julianroth.org/documentation/multigrid/basics.html",)
)
docs = loader.load()

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