<img width="1440" height="1384" alt="image" src="https://github.com/user-attachments/assets/2c803d33-934f-40ca-bdcc-fcda8b03ef00" /># 📈 Agentic Investment & Finance Assistant

> An AI-powered investment research assistant trained on the world's most influential finance and trading literature. Ask questions, get insights, and make informed investment decisions — all through a conversational interface.


<img width="1440" height="1384" alt="image" src="https://github.com/user-attachments/assets/acacf4c8-dff3-4577-a9cf-ed432c1955ea" />


---

## 🧠 What Is This?

The **Agentic Investment & Finance Assistant** is a Retrieval-Augmented Generation (RAG) chatbot built on a curated knowledge base of classic investment and trading books. It combines a powerful agentic reasoning loop with real-time web search to answer questions about markets, trading strategies, technical analysis, derivatives, and investor psychology.

Whether you're a beginner trying to understand NIFTY 50 or an experienced trader looking for insights on options pricing, this assistant has you covered.

---

## 📚 Knowledge Base — Trained On

The assistant's knowledge base is built from the following landmark books in finance and investing:

| Book | Author | Topic |
|------|--------|-------|
| **Technical Analysis of the Financial Markets** | John J. Murphy | Technical Analysis |
| **Security Analysis** (6th Edition) | Benjamin Graham & David Dodd | Fundamental Analysis |
| **Stock Market Wizards** | Jack D. Schwager | Trading Psychology & Strategy |
| **Options, Futures, and Other Derivatives** (5th Edition) | John C. Hull | Derivatives & Quantitative Finance |
| **Trading In The Zone** | Mark Douglas | Trading Psychology |
| **Reminiscences of a Stock Operator** | Edwin Lefèvre | Market Wisdom & Speculation |

These books represent decades of proven investment wisdom, quantitative methods, and market psychology — all queryable through natural language.

---

## 🏗️ Project Structure

```
Agentic_Stock_market_bot/
├── agent/                  # LangGraph agentic reasoning loop
├── config/
│   └── config.yaml         # Model, vector DB, and retriever settings
├── custom_logging/         # Logging utilities
├── data_ingestion/
│   └── ingestion_pipeline.py  # Document loading & Pinecone ingestion
├── data_models/            # Pydantic request/response models
├── exceptions/             # Custom exception handling
├── fallback_data/          # Fallback responses
├── notebook/               # Experimentation notebooks
├── prompt_library/         # System and RAG prompts
├── toolkit/                # Agent tools (Tavily search, retriever)
├── utils/
│   ├── model_loaders.py    # Embedding & LLM loader
│   └── config_loader.py    # YAML config loader
├── main.py                 # FastAPI backend
├── streamlit.py            # Streamlit frontend
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **Agentic Framework** | LangGraph |
| **Embedding Model** | Google `gemini-embedding-001` (3072 dims) |
| **LLM** | Groq — `llama-3.3-70b-versatile` |
| **Vector Database** | Pinecone (Serverless, cosine similarity) |
| **Web Search Tool** | Tavily Search API |
| **Document Loaders** | LangChain (PyPDF, Docx2txt) |

---

## 🤖 Models Used

### Embedding Model
- **Model:** `gemini-embedding-001`
- **Provider:** Google Generative AI (`google-genai` SDK)
- **Dimensions:** 3072
- **Task Types:** `RETRIEVAL_DOCUMENT` for indexing, `RETRIEVAL_QUERY` for search

### LLM
- **Model:** `llama-3.3-70b-versatile`
- **Provider:** Groq (ultra-low latency inference)
- **Use:** Agentic reasoning, RAG answer generation, tool calling

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Agentic_Stock_market_bot.git
cd Agentic_Stock_market_bot
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

| Variable | Where to Get |
|----------|-------------|
| `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `GROQ_API_KEY` | [Groq Console](https://console.groq.com/) |
| `PINECONE_API_KEY` | [Pinecone Console](https://app.pinecone.io/) |
| `TAVILY_API_KEY` | [Tavily](https://app.tavily.com/) |

### 5. Configure Settings

Review `config/config.yaml`:

```yaml
vector_db:
  index_name: "trading-bot"

embedding_model:
  model_name: "gemini-embedding-001"
  dimension: 3072

llm:
  groq:
    provider: "groq"
    model_name: "llama-3.3-70b-versatile"

retriever:
  top_k: 3
  score_threshold: 0.5

tools:
  tavily:
    max_results: 5
```

### 6. Run the Backend

```bash
uvicorn main:app --reload --port 8000
```

### 7. Run the Frontend

In a new terminal:

```bash
streamlit run streamlit.py
```

Open your browser at `http://localhost:8501`

---

## 📄 How to Upload Documents

1. Open the app in your browser
2. Use the **Upload Documents** panel in the sidebar
3. Upload PDF or DOCX files (stock reports, research papers, etc.)
4. Click **Upload and Ingest**
5. The documents are chunked, embedded, and stored in Pinecone automatically

---

## 💬 Example Questions

- *"What does John Murphy say about moving average crossovers?"*
- *"Explain the concept of implied volatility from Hull's perspective"*
- *"What is the psychological mindset of a successful trader according to Mark Douglas?"*
- *"How did Jesse Livermore approach market speculation?"*
- *"What is Benjamin Graham's margin of safety principle?"*
- *"Summarize the latest NIFTY 50 trends"* *(uses live web search)*

---

## 🔒 Security Notes

- Never commit your `.env` file — it's listed in `.gitignore`
- API keys are loaded at runtime via `python-dotenv`
- All file uploads are processed in temporary storage and not persisted on disk

---

## 📋 Requirements

- Python 3.11+
- Active Pinecone account (Serverless tier works)
- Google AI Studio API key with Generative Language API enabled
- Groq API key (free tier available)

---

## 📜 License

This project is for educational and research purposes. The knowledge base books are copyrighted by their respective authors and publishers. This tool does not redistribute any book content — it only stores vector embeddings.
