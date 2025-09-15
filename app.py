import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory

# Import your tools from the 'tools' directory
from tools.hospital_tool import hospital_tool
from tools.vaccine_tool import vaccination_tool
from tools.rag_tool import create_rag_tool

def main():
    # --- LLM and API Key Setup ---
    try:
        # Best practice: set GROQ_API_KEY as an environment variable
        GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
        if not GROQ_API_KEY:
            raise KeyError
    except KeyError:
        print("🔴 GROQ_API_KEY environment variable not set. Please set your API key.")
        return

    llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)

    # --- Vector DB Path ---
    # IMPORTANT: Update this to the correct path of your ChromaDB
    CHROMA_DB_PATH = "/path/to/your/chroma_db"
    
    # --- Initialize Tools ---
    rag_tool = create_rag_tool(llm, CHROMA_DB_PATH)
    tools = [hospital_tool, vaccination_tool, rag_tool]

    # --- Agent Prompt ---
    template = """
    You are a friendly and empathetic AI health assistant. Your goal is to help users by providing accurate information from your tools.

    TOOLS:
    ------
    You have access to the following tools. Here are their names:
    {tool_names}

    Here are the details for each tool:
    {tools}

    CONVERSATION HISTORY:
    ---------------------
    {chat_history}

    INSTRUCTIONS & EXAMPLES:
    ------------------------
    - Your primary job is to be a helpful, conversational assistant.
    - When you receive a result from a tool, NEVER just show the raw output. ALWAYS rephrase it in a friendly, easy-to-understand way.
    - If the hospital_directory_tool asks for a pincode, you MUST ask the user for it.
    - For hospital_directory_tool, the input MUST be a dictionary like: {{"state": "Uttar Pradesh", "pincode": "208001"}}

    Begin!

    Question: {input}
    {agent_scratchpad}
    """
    
    custom_prompt = PromptTemplate.from_template(template)
    
    # --- Memory ---
    memory = ConversationBufferWindowMemory(k=5, memory_key='chat_history', return_messages=True)

    # --- Agent and Executor ---
    agent = create_react_agent(llm, tools, custom_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    # --- Chat Loop ---
    print("🚀 Health Chatbot is ready! Type 'exit' to end.")
    print("-" * 50)
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("AI Assistant: Goodbye!")
            break
        if user_input.strip():
            response = agent_executor.invoke({"input": user_input})
            print(f"\nAI Assistant: {response['output']}\n")

if __name__ == "__main__":
    main()
