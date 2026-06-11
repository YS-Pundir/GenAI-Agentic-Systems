# load the  vectore store and create the retreiver
import os 
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

Embed_Model_Name= "sentence-transformers/all-MiniLM-L6-v2"
embeddings=HuggingFaceEmbeddings(model_name=Embed_Model_Name)
Chroma_Path="./tesla_db"
Top_K=5


Vectore_Store=Chroma(
    persist_directory=Chroma_Path,
    embedding_function=embeddings
)
retreiver=Vectore_Store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":Top_K}
)
