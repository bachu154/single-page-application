from milvus_client import get_collection
from embeddings import EmbeddingService
from html_processor import fetch_html, clean_html, chunk_text
from config import COLLECTION_NAME
import logging

logger = logging.getLogger(__name__)

class SearchEngine:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.collection = get_collection()
    
    def process_and_index_url(self, url: str) -> int:
        """Process URL, create chunks, generate embeddings, and index in Milvus."""
        try:
            # Fetch and clean HTML
            html_content = fetch_html(url)
            cleaned_text = clean_html(html_content)
            
            # Create chunks
            chunks = chunk_text(cleaned_text)
            
            # Generate embeddings
            embeddings = self.embedding_service.embed_texts(chunks)
            
            # Prepare data for insertion
            chunk_indices = list(range(len(chunks)))
            urls = [url] * len(chunks)
            
            data = [
                chunk_indices,
                chunks,
                embeddings,
                urls,
            ]
            
            # Insert into Milvus
            result = self.collection.insert(data)
            self.collection.flush()
            
            logger.info(f"Indexed {len(chunks)} chunks from {url}")
            return len(chunks)
        except Exception as e:
            logger.error(f"Failed to process and index URL {url}: {e}")
            raise
    
    def search(self, query: str, top_k: int = 10) -> list:
        """Search for relevant chunks based on query."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.embed_text(query)
            
            # Search in Milvus
            search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
            results = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["chunk_index", "content", "url"]
            )
            
            # Format results
            formatted_results = []
            for hits in results:
                for hit in hits:
                    formatted_results.append({
                        "chunk_index": hit.entity.get("chunk_index"),
                        "content": hit.entity.get("content"),
                        "score": float(hit.distance),
                        "url": hit.entity.get("url")
                    })
            
            logger.info(f"Found {len(formatted_results)} results for query: {query}")
            return formatted_results
        except Exception as e:
            logger.error(f"Search failed for query '{query}': {e}")
            raise
