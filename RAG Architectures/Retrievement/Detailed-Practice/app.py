# Load the apis
import os
from dotenv import load_dotenv
load_dotenv()
# Load the tools
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

Embendding_Model_Name= "sentence-transformers/all-MiniLM-L6-v2" 
Chroma_Path=r"C:\Users\Lenovo\GenAI-Agentic-Systems\RAG Architectures\Retrievement\Detailed-Practice\tesla_db"
Top_k=5
tesla_collection="tesla-10k-2019-to-2023"
embeddings=HuggingFaceEmbeddings(model_name=Embendding_Model_Name)


vectore_Store=Chroma(
    collection_name=tesla_collection,
    persist_directory=Chroma_Path,
    embedding_function=Embendding_Model_Name
)

retreiver=vectore_Store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":Top_k}
)

def retreive_chunks(user_query,retreiver):
    docs=retreiver.invoke(user_query)
    retreived=[]
    for i,doc in enumerate(docs):
        retreived.append({
            "Index":i,
            "Text":doc.page_content,
            "Metadata":doc.metadata
        })
    return retreived

