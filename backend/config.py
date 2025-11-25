import os
from dotenv import load_dotenv

load_dotenv()

# Milvus Configuration
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
COLLECTION_NAME = "html_chunks"

# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOKENIZER_MODEL = "bert-base-uncased"

# Chunk Configuration
MAX_TOKENS_PER_CHUNK = 500
EMBEDDING_DIMENSION = 384
