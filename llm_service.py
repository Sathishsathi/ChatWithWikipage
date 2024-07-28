from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings import OllamaEmbeddings
from langchain.globals import set_llm_cache
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.cache import SQLiteCache
from flask import session

#caching the response for faster retrival of same questions
set_llm_cache(SQLiteCache(database_path="/Users/sathish.kumar/Documents/personal/pytorch_learning/langchain_try/langchain.db"))

#defining the llm model
llm = Ollama(model="llama3")


#defining the embedding model which will be used for retrival
ollama_emb = OllamaEmbeddings(
    model="llama3",
)


store = {}

contextualize_q_system_prompt = (
		    "Given a chat history and the latest user question "
		    "which might reference context in the chat history, "
		    "Answer the following question from the context below"
		)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\
    {context}"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

chat_history = []

def get_session_history(session_id) -> BaseChatMessageHistory:
    # if session_id not in store:
    #     store[session_id] = x()
    # return store[session_id]
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

def get_response(question, content, session_id):
	global chat_history
	text_splitter = RecursiveCharacterTextSplitter()
	documents = text_splitter.split_text(content)
	vector = FAISS.from_texts(documents, ollama_emb)
	retriever = vector.as_retriever()
	# response = document_chain.invoke({
	#      "input": question,
	#      "context": [Document(page_content=content)]
	#  })
	history_aware_retriever = create_history_aware_retriever(
		    llm, retriever, contextualize_q_prompt
		)
	question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
	rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


	conversational_rag_chain = RunnableWithMessageHistory(
	    rag_chain,
	    get_session_history,
	    input_messages_key="input",
	    history_messages_key="chat_history",
	    output_messages_key="answer",
	)
	
	ai_msg_1 = conversational_rag_chain.invoke({"input": query, "chat_history": chat_history}, config={
    "configurable": {"session_id": session_id}
	})

	chat_history.extend(
	    [
	        HumanMessage(content=query),
	        AIMessage(content=ai_msg_1["answer"]),
	    ]
	)
	print(ai_msg_1['answer'])
	return ai_msg_1['answer']

# wiki_content = get_page_content('Viluppuram')
# resp = get_response(query, wiki_content)
