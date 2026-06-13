# Load the apis
import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
api_key=os.getenv("api_key")
GROQ_MODEL= "llama-3.3-70b-versatile"

# Load the tools
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
def generate_answer(system_message,user_message):
    client=Groq(api_key=api_key)
    response=client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role":"user","content":user_message},
            {"role":"system","content":system_message}
        ],
        temperature=0
    )

    return response.choices[0].message.content

def rag_answer(user_query, retriever):
    """End-to-end: retrieve → build messages → generate → return audit bundle."""
    retrieved = retrieve_chunks(user_query, retriever)
    user_message = build_user_message(user_query, retrieved)
    answer = generate_answer(SYSTEM_MESSAGE, user_message)
    return {"answer": answer, "retrieved_chunks": retrieved, "user_message": user_message}

def main():

    question = "What is the annual revenue in the year 2022?"
    print("Question:", question)

    result = rag_answer(question, retriever)

    print("\n--- Retrieved chunks ---")
    for chunk in result["retrieved_chunks"]:
        print(f"Chunk {chunk['Index']}: {chunk['Metadata']}")

    print("\n--- Generated answer ---")
    print(result["answer"])

    print("\n--- Grounding audit (you fill in) ---")
    print("List each fact in the answer and the chunk page that supports it.")


if __name__ == "__main__":
    main()