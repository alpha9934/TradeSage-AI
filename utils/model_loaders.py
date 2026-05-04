import os
from typing import List
from dotenv import load_dotenv
from pydantic import SecretStr
from google import genai
from google.genai import types
from langchain_core.embeddings import Embeddings
from langchain_groq import ChatGroq
from utils.config_loader import load_config


# ──────────────────────────────────────────────
# Custom Embeddings — uses new google.genai SDK
# (google.generativeai is deprecated)
# ──────────────────────────────────────────────
class GeminiEmbeddings(Embeddings):
    """
    Embeddings using the new google-genai SDK.
    Supports models: gemini-embedding-001, gemini-embedding-2
    """

    def __init__(self, api_key: str, model: str = "gemini-embedding-001"):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        print(f"GeminiEmbeddings initialized with model: {self.model}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents for storage/indexing."""
        embeddings = []
        for text in texts:
            result = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
            )
            embeddings.append(result.embeddings[0].values)
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string for retrieval."""
        result = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        return result.embeddings[0].values


# ──────────────────────────────────────────────
# Main ModelLoader class
# ──────────────────────────────────────────────
class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """

    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()

    def _validate_env(self):
        """Validate necessary environment variables."""
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_embeddings(self) -> GeminiEmbeddings:
        """
        Load and return a GeminiEmbeddings instance.
        Uses new google-genai SDK directly.
        """
        print("Initializing Google Embedding model...")
        model_name = self.config["embedding_model"]["model_name"]
        print(f"Using embedding model: {model_name}")
        return GeminiEmbeddings(api_key=self.google_api_key, model=model_name)

    def load_llm(self) -> ChatGroq:
        """Load and return the Groq LLM model."""
        print("Initializing Groq LLM...")
        model_name = self.config["llm"]["groq"]["model_name"]
        groq_model = ChatGroq(
            model=model_name,
            api_key=SecretStr(self.groq_api_key) if self.groq_api_key else None
        )
        print(f"Groq LLM loaded: {model_name}")
        return groq_model