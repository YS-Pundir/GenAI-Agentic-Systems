# Load the apis
import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
api_key=os.getenv("api_key")
GROQ_MODEL= "llama-3.3-70b-versatile"
client=Groq(api_key=api_key)

# Load the tools
import json
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Declaring some important variable 
Embendding_Model_Name= "sentence-transformers/all-MiniLM-L6-v2" 
Chroma_Path=r"C:\Users\Lenovo\GenAI-Agentic-Systems\RAG Architectures\Retrievement\Detailed-Practice\tesla_db"
Top_k=5
tesla_collection="tesla-10k-2019-to-2023"
embeddings=HuggingFaceEmbeddings(model_name=Embendding_Model_Name)

# getting the ChromaStore , which was persisted during the experiment in lab
vectore_Store=Chroma(
    collection_name=tesla_collection,
    persist_directory=Chroma_Path,
    embedding_function=embeddings
)
# declaring the retreiver
retriever=vectore_Store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":Top_k}
)

# function for retreiving the chunks and returing it in the format of list of dictionaries
def retrieve_chunks(user_query,retriever):
    docs=retriever.invoke(user_query)
    retreived=[]
    for i,doc in enumerate(docs):
        retreived.append({
            "Index":i,
            "Text":doc.page_content,
            "Metadata":doc.metadata
        })
    return retreived




# Building the system Prompt
SYSTEM_MESSAGE = """
You are an assistant for a financial services firm that answers user queries on annual reports.
User input will contain the context required to answer the question.
The context will begin with the token #context and contains portions of the source document.
The question will begin with the token #question.
Answer ONLY using the provided context.
If the answer is not found in the context, then do not make things up , just refuse to answers that friendly .
""".strip()
# building the context text from the retreived chunks
def build_context_block(retrieve_chunks):
    parts=[]
    for chunk in retrieve_chunks:
        parts.append(chunk["Text"])

    return "\n\n".join(parts)
# building the user query from the by atatching the context 
def build_user_message(user_query,retrieve_chunks):
    context_text=build_context_block(retrieve_chunks)

    return f"#context\n{context_text}\n#question\n{user_query}"


# Generating the answers:
def generate_answer(conversational_history):
    response = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=conversational_history,
                    temperature=0
                )

    return response.choices[0].message.content.strip()

# will use this function in case want to see the metadata for inquiry
def rag_answer(user_query, retriever):
    """End-to-end: retrieve → build messages → generate → return audit bundle."""
    retrieved = retrieve_chunks(user_query, retriever)
    user_message = build_user_message(user_query, retrieved)
    answer = generate_answer(SYSTEM_MESSAGE, user_message)
    return {"answer": answer, "retrieved_chunks": retrieved, "user_message": user_message}






# --- Configuration ---
HISTORY_FILE = "conversation_history.json"
MAX_STEPS = 5
STOP_WORDS = ["exit", "quit", "stop"]

# --- Helper functions for managing conversation history ---
def load_conversation_history():
    """Loads conversation history from a JSON file, or initializes it with the system message."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
        # Ensure system message is always at the beginning if not present
        if not history or history[0]['role'] != 'system':
            history.insert(0, {'role': 'system', 'content': SYSTEM_MESSAGE})
        print(f"Loaded conversation history from {HISTORY_FILE}. Current turns: {len(history)-1}")
    else:
        history = [{'role': 'system', 'content': SYSTEM_MESSAGE}]
        print(f"No conversation history found at {HISTORY_FILE}. Starting a new conversation.")
    return history

def save_conversation_history(history):
    """Saves the current conversation history to a JSON file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
    print(f"Conversation history saved to {HISTORY_FILE}.")

# --- Multi-turn RAG interaction loop ---
def multi_turn_rag_chat():
    conversation_history = load_conversation_history()
    turn_count = 0

    print("\n--- Starting Multi-Turn RAG Chat ---")
    print("Type 'exit', 'quit', or 'stop' to end the conversation.")
    print(f"Maximum {MAX_STEPS} turns allowed per session (excluding system message and previous turns).")

    # Display initial system message if it's a new conversation
    if len(conversation_history) == 1 and conversation_history[0]['role'] == 'system':
         print(f"[SYSTEM] - {conversation_history[0]['content'][:100]}...")

    while turn_count < MAX_STEPS:
        user_input = input(f"\n[{turn_count + 1}/{MAX_STEPS}] You: ")

        if user_input.lower() in STOP_WORDS:
            print("Exiting chat. Goodbye!")
            break

        # 1. Retrieve relevant documents from Vector DB
        print("--> Retrieving documents for context...")
        context =retrieve_chunks(user_input, retriever)
        user_message_content = build_user_message(user_input, context).format(context=context, question=user_input)

        # 2. Append the user's message (with context) to history
        conversation_history.append({'role': 'user', 'content': user_message_content})

        # 3. Call the LLM with the entire history
        try:
            print("--> Calling LLM...")

            assistant_response = generate_answer(conversation_history)

        except Exception as e:
            assistant_response = f'Sorry, I encountered the following error: \n {e}'
            print(f"LLM Error: {e}")

        # 4. Append the LLM's response to history
        conversation_history.append({'role': 'assistant', 'content': assistant_response})

        # 5. Save the updated history
        save_conversation_history(conversation_history)

        print(f"Assistant: {assistant_response}")
        turn_count += 1

    if turn_count == MAX_STEPS:
        print(f"\nMaximum turns ({MAX_STEPS}) reached. Chat session ended.")

# --- Run the chat ---
multi_turn_rag_chat()
