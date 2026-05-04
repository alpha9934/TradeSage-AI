import os
import tempfile
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from utils.model_loaders import ModelLoader
from utils.config_loader import load_config
from pinecone import ServerlessSpec, Pinecone
from uuid import uuid4
import sys
from exceptions.exceptions import TradingBotException


class DataIngestion:
    """
    Class to handle document loading, transformation and ingestion into Pinecone vector store.
    """

    def __init__(self):
        try:
            print("Initializing DataIngestion pipeline...")
            self.model_loader = ModelLoader()
            self._load_env_variables()
            self.config = load_config()
        except Exception as e:
            raise TradingBotException(e, sys)

    def _load_env_variables(self):
        try:
            load_dotenv()

            required_vars = [
                "GOOGLE_API_KEY",
                "PINECONE_API_KEY"
            ]

            missing_vars = [var for var in required_vars if os.getenv(var) is None]
            if missing_vars:
                raise EnvironmentError(f"Missing environment variables: {missing_vars}")

            self.google_api_key = os.getenv("GOOGLE_API_KEY")
            self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        except Exception as e:
            raise TradingBotException(e, sys)

    def load_documents(self, uploaded_files) -> List[Document]:
        try:
            documents = []
            for uploaded_file in uploaded_files:
                file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
                suffix = file_ext if file_ext in [".pdf", ".docx"] else ".tmp"

                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(uploaded_file.file.read())
                    temp_path = temp_file.name

                if file_ext == ".pdf":
                    loader = PyPDFLoader(temp_path)
                    documents.extend(loader.load())
                elif file_ext == ".docx":
                    loader = Docx2txtLoader(temp_path)
                    documents.extend(loader.load())
                else:
                    print(f"Unsupported file type: {uploaded_file.filename}")
            return documents
        except Exception as e:
            raise TradingBotException(e, sys)

    def store_in_vector_db(self, documents: List[Document]):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,    # was 1000
            chunk_overlap=100  # was 200
            )
            documents = text_splitter.split_documents(documents)

            pinecone_client = Pinecone(api_key=self.pinecone_api_key)
            index_name = self.config["vector_db"]["index_name"]

            # Read dimension from config (must match embedding model output)
            dimension = self.config["embedding_model"].get("dimension", 3072)

            existing_indexes = [i.name for i in pinecone_client.list_indexes()]

            if index_name in existing_indexes:
                # Check if existing index has wrong dimension and delete if so
                index_info = pinecone_client.describe_index(index_name)
                if index_info.dimension != dimension:
                    print(f"Dimension mismatch: index has {index_info.dimension}, model needs {dimension}. Recreating index...")
                    pinecone_client.delete_index(index_name)
                    existing_indexes = []  # force recreation below

            if index_name not in existing_indexes:
                print(f"Creating Pinecone index '{index_name}' with dimension {dimension}...")
                pinecone_client.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )

            index = pinecone_client.Index(index_name)
            vector_store = PineconeVectorStore(index=index, embedding=self.model_loader.load_embeddings())
            uuids = [str(uuid4()) for _ in range(len(documents))]

            vector_store.add_documents(documents=documents, ids=uuids)
            print(f"Successfully stored {len(documents)} chunks in Pinecone.")
        except Exception as e:
            raise TradingBotException(e, sys)

    def run_pipeline(self, uploaded_files):
        try:
            documents = self.load_documents(uploaded_files)
            if not documents:
                print("No valid documents found.")
                return
            self.store_in_vector_db(documents)
        except Exception as e:
            raise TradingBotException(e, sys)


if __name__ == '__main__':
    pass