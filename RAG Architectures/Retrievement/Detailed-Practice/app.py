# Load the apis
import os
from dotenv import load_dotenv
load_dotenv()
# Load the tools
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

Embendding_Model_Name= "sentence-transformers/all-MiniLM-L6-v2" 
Chroma_Path="./tesla_db"
Top_k=5

embeddings=HuggingFaceEmbeddings(model_name=Embendding_Model_Name)

vectore_Store=Chroma(
    persist_directory=Chroma_Path,
    embedding_function=embeddings
)

retreiver=vectore_Store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":Top_k}
)

