# HTML DOM Search Engine – SPA with Semantic Chunk Search

A full-stack semantic search engine that fetches HTML content, chunks it intelligently, generates embeddings, and enables semantic search through a vector database.

## Features

- **HTML Processing**: Fetches and cleans HTML from any URL
- **Intelligent Chunking**: Splits content into 500-token chunks using BERT tokenizer
- **Semantic Search**: Uses sentence-transformers for semantic embeddings
- **Vector Database**: Milvus for fast similarity search
- **Modern UI**: React/Next.js SPA with Tailwind CSS
- **RESTful API**: FastAPI backend with CORS support

## Tech Stack

### Frontend
- Next.js 14
- React 18
- Tailwind CSS
- Axios for API calls

### Backend
- FastAPI
- Python 3.9+
- BeautifulSoup4 for HTML parsing
- Transformers + Sentence-Transformers for embeddings
- Milvus for vector database

## Project Structure

\`\`\`
.
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── header.tsx
│   │   ├── search-form.tsx
│   │   └── search-results.tsx
│   └── package.json
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── config.py
│   ├── milvus_client.py
│   ├── html_processor.py
│   ├── embeddings.py
│   └── search_engine.py
├── scripts/
│   ├── setup-milvus.sh
│   └── start-backend.sh
└── README.md
\`\`\`

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker (for Milvus)

### 1. Setup Milvus Vector Database

Using Docker (Recommended):

\`\`\`bash
docker run -d --name milvus \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:latest
\`\`\`

Or using the setup script:

\`\`\`bash
chmod +x scripts/setup-milvus.sh
./scripts/setup-milvus.sh
\`\`\`

### 2. Setup Backend

\`\`\`bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python main.py
\`\`\`

The backend will start on `http://localhost:8000`

API Documentation available at: `http://localhost:8000/docs`

### 3. Setup Frontend

\`\`\`bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
\`\`\`

The frontend will start on `http://localhost:3000`

## Usage

1. Open the frontend at `http://localhost:3000`
2. Enter a website URL (e.g., `https://example.com`)
3. Enter your search query
4. Click "Search"
5. View the top 10 matching HTML chunks sorted by semantic similarity

## API Endpoints

### POST /search

**Request:**
\`\`\`json
{
  "url": "https://example.com",
  "query": "search terms"
}
\`\`\`

**Response:**
\`\`\`json
[
  {
    "chunk_index": 0,
    "content": "HTML chunk content (max 500 tokens)...",
    "score": 0.25,
    "url": "https://example.com"
  }
]
\`\`\`

### GET /health

Returns API health status.

## How It Works

1. **HTML Fetching**: Requests the website URL
2. **HTML Cleaning**: Removes scripts, styles, and unwanted elements
3. **Tokenization**: Uses BERT tokenizer to count tokens
4. **Chunking**: Splits text into max 500-token chunks
5. **Embedding**: Converts chunks to 384-dimensional vectors
6. **Indexing**: Stores vectors in Milvus with metadata
7. **Search**: Encodes query, searches similar embeddings
8. **Ranking**: Returns top 10 results by similarity score

## Vector Database Details

**Collection Schema:**
- `id`: Auto-incremented primary key
- `chunk_index`: Position of chunk in document
- `content`: Text content (max 5000 characters)
- `embedding`: 384-dimensional vector (all-MiniLM-L6-v2)
- `url`: Source URL

**Index Configuration:**
- Metric Type: L2 (Euclidean distance)
- Index Type: IVF_FLAT
- Number of Lists: 128

## Models Used

- **Tokenizer**: `bert-base-uncased` (HuggingFace)
- **Embedding**: `all-MiniLM-L6-v2` (Sentence-Transformers)

## Performance Considerations

- First search on a URL triggers indexing (one-time cost)
- Subsequent searches are fast (vector DB lookup)
- Chunk size (500 tokens) balances context and performance
- IVF_FLAT index good for datasets < 1M vectors

## Troubleshooting

**"Failed to connect to Milvus"**
- Ensure Milvus is running: `docker ps | grep milvus`
- Check Milvus is on localhost:19530

**"Failed to fetch URL"**
- Verify the URL is valid and accessible
- Check network connectivity
- Some sites may block scraping

**"Embedding model not found"**
- First run downloads model from HuggingFace (~120MB)
- Requires internet connection
- Model is cached locally after first download

## Future Improvements

- Support for JavaScript-rendered content
- Incremental indexing (avoid re-indexing URLs)
- Advanced query parsing and filtering
- Full-text search hybrid approach
- Admin dashboard for indexed URLs
- User authentication and API keys
- Rate limiting and caching
- Support for PDF and other file types

## License

MIT

## Support

For issues or questions, please open an issue on GitHub or refer to the documentation.
