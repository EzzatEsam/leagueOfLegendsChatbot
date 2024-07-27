from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from lol_chatter_backend.LolDataFetcher import latest_patch , get_items , get_champions
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from lol_chatter_backend.LolDataFetcher.post_processor import dict2str 


version_file = r"lol_chatter_backend/cache/version.txt"
db_path = r"lol_chatter_backend/cache/chroma_db"
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")



if  os.path.exists(version_file):
    with open(version_file, "r") as file:
        version = file.read()
else:
    os.makedirs(os.path.dirname(version_file),
                exist_ok=True)
    version = None
    
    
if version != latest_patch:
    print("Updating data")
    items = get_items()
    champions = get_champions()
    
    
    print("Creating documents")
    docs = [Document(page_content=dict2str(item), metadata={"source":f"Item data : {item["name"]}" }) for item in items.values()]

    docs += [Document(page_content=dict2str(champion), metadata={"source": f"Champion data : {champion['name']}" }) for champion in champions.values()]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print("Creating embeddings db")
    
    vectorstore = Chroma.from_documents(
    documents=splits,  # Data
    embedding=gemini_embeddings,  # Embedding model
    persist_directory=db_path,  # Directory to save data
        )

    
    with open(version_file, "w") as file:
        file.write(latest_patch)
        

print("Reading db")
vectorstore_disk = Chroma(
    persist_directory=db_path,  # Directory of db
    embedding_function=gemini_embeddings,  # Embedding model
)


def get_retriever():
    return vectorstore_disk.as_retriever(search_kwargs={"k": 4})

