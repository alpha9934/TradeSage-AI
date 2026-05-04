from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager

from data_ingestion.ingestion_pipeline import DataIngestion
from agent.agent import GraphBuilder
from data_models.models import QuestionRequest

# 1. Use Lifespan to initialize the Graph once on startup
services = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Graph once
    print("Building Agentic Graph...")
    builder = GraphBuilder()
    builder.build()
    services["graph"] = builder.get_graph()
    services["ingestion"] = DataIngestion()
    yield
    services.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Agentic Stock Market Bot API is running"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        # Use the pre-initialized ingestion service
        services["ingestion"].run_pipeline(files)
        return {"message": "Files successfully processed and stored."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/query")
async def query_chatbot(request: QuestionRequest):
    try:
        # Use the pre-built graph
        graph = services["graph"]
        
        # Format for LangGraph
        input_data = {"messages": [("user", request.question)]}
        
        # Invoke the graph
        result = graph.invoke(input_data)
        
        # Extract the last message content
        if "messages" in result and len(result["messages"]) > 0:
            final_output = result["messages"][-1].content
        else:
            final_output = "I'm sorry, I couldn't process that request."
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})