from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def create_rag_tool(llm, vector_db_path: str):
    """Creates a RAG tool from an existing ChromaDB vector store."""
    
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
    vector_db = Chroma(
        persist_directory=vector_db_path,
        embedding_function=embedding_function
    )
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    rag_prompt_template = "Answer the user's question based only on the following context:\n\nContext:\n{context}\n\nQuestion:\n{question}"
    rag_prompt = PromptTemplate.from_template(rag_prompt_template)
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    
    return Tool(
        name="symptom_and_health_knowledge_base",
        func=rag_chain.invoke,
        description="""
        Use this tool for any general health-related questions, including symptoms, diseases, and treatments.
        It is your primary source of knowledge. Use it as a fallback if no other specific tool is suitable.
        The input to this tool should be a simple question string.
        """
    )
