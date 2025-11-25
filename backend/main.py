from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search_engine import SearchEngine
from milvus_client import connect_milvus, create_collection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="HTML Search Engine API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine
search_engine = None

class SearchRequest(BaseModel):
    url: str
    query: str

class SearchResponse(BaseModel):
    chunk_index: int
    content: str
    score: float
    url: str

@app.on_event("startup")
async def startup_event():
    """Initialize Milvus connection and collection on startup."""
    global search_engine
    try:
        connect_milvus()
        create_collection()
        search_engine = SearchEngine()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.post("/search", response_model=list[SearchResponse])
async def search(request: SearchRequest):
    """
    Search for relevant HTML chunks based on query.
    
    - **url**: Website URL to fetch and search
    - **query**: Search query
    
    Returns top 10 matched chunks with similarity scores.
    """
    try:
        if not request.url or not request.query:
            raise HTTPException(status_code=400, detail="URL and query are required")
        
        # Process and index the URL
        logger.info(f"Processing URL: {request.url}")
        chunks_indexed = search_engine.process_and_index_url(request.url)
        logger.info(f"Indexed {chunks_indexed} chunks")
        
        # Search for relevant chunks
        results = search_engine.search(request.query, top_k=10)
        
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search request failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
