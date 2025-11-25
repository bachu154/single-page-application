from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, EMBEDDING_DIMENSION
import logging

logger = logging.getLogger(__name__)

def connect_milvus():
    """Connect to Milvus vector database."""
    try:
        connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
        logger.info(f"Connected to Milvus at {MILVUS_HOST}:{MILVUS_PORT}")
    except Exception as e:
        logger.error(f"Failed to connect to Milvus: {e}")
        raise

def create_collection():
    """Create Milvus collection for HTML chunks."""
    try:
        # Define schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="chunk_index", dtype=DataType.INT32),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIMENSION),
            FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500),
        ]
        
        schema = CollectionSchema(fields=fields, description="HTML chunks with embeddings")
        
        # Create collection if it doesn't exist
        if COLLECTION_NAME in [c.name for c in Collection.list()]:
            logger.info(f"Collection {COLLECTION_NAME} already exists")
            return Collection(COLLECTION_NAME)
        
        collection = Collection(name=COLLECTION_NAME, schema=schema)
        logger.info(f"Created collection {COLLECTION_NAME}")
        
        # Create index
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        logger.info("Created index on embedding field")
        
        return collection
    except Exception as e:
        logger.error(f"Failed to create collection: {e}")
        raise

def get_collection():
    """Get existing collection."""
    try:
        return Collection(COLLECTION_NAME)
    except Exception as e:
        logger.error(f"Failed to get collection: {e}")
        raise
