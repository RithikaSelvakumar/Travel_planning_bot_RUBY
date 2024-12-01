#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.messages import HumanMessage
from flask import Flask, render_template, request, jsonify
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama

import os

import time
app = Flask(__name__)
load_dotenv()
os.environ.get("USER_AGENT")
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get("PERSIST_DIRECTORY")
model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

from constants import CHROMA_SETTINGS
qa=None
llm=None
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
retriever = db.as_retriever(search_kwargs={"k": 5})

def main(query,chat_history):

    
    
    
  
    # Prepare the LLM
    llm= Ollama(model="llama3.2")

    contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
     )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )


### Answer question ###
    qa_system_prompt = """You are an intelligent meeting assistant called RUBY for helping employees clarify their queries about the meeting .
        Use the following pieces of retrieved context to answer the question in detail:{context}.\
        Greet if the user greets you. \
        If you don't know the answer, just say that you don't know 
        Only answer relevant content and Not anything extra.\
        Dont return the prompt in the answer. \
        Don't respond irrelevant or anything outside the context. \
    
    """
    qa_prompt= ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain
'''
if __name__ == "__main__":
    chat_history=[]
        
    while True:
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue

        # Get the answer from the chain
        start = time.time()
        rag_chain=main(query,chat_history)
        ai_msg_1=rag_chain.invoke({"input":query,"chat_history":chat_history})
        
        
        end = time.time()

       
        print("Query-->",query,"\nresult-->",ai_msg_1["answer"])
        print(f"\n> Answer (took {round(end - start, 2)} s.):")
        chat_history.extend([HumanMessage(content=query), ai_msg_1["answer"]])

        print(" the Final answer is :", ai_msg_1['answer'])

        # Print the relevant sources used for the answer
        # if "context" in ai_msg_1:
        #     for document in ai_msg_1["context"]:
        #         print("\n> " + document.metadata["source"] + ":")
        #     print(document.page_content)

'''
