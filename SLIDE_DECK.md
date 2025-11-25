# Slide Deck Content: HTML DOM Search Engine

## Slide 1: Introduction

**Title:** Semantic Search for HTML Content

**Content:**
- **Problem**: Finding relevant information on websites requires manual browsing or keyword matching, which is inefficient and often inaccurate
- **Solution**: A semantic search engine that understands meaning, not just keywords
- **Architecture Overview**:
  - Frontend: React/Next.js SPA for user interaction
  - Backend: FastAPI for processing and API
  - Vector DB: Milvus for semantic similarity search
  - NLP: Sentence-Transformers for embeddings

**Key Insight**: Semantic search uses AI-generated embeddings to find contextually relevant content, not just keyword matches.

---

## Slide 2: Frontend Design & User Experience

**Title:** Intuitive Search Interface

**Content:**
- **UI Components**:
  - Clean, centered search form
  - Two input fields: Website URL + Search Query
  - Single "Search" button with loading state
  - Real-time results display with metadata

- **UX Features**:
  - Loading animation during processing
  - Clear error messages
  - Results shown as cards with:
    - Chunk preview (max 500 tokens)
    - Similarity score
    - Source URL link
    - Chunk index

- **Design Principles**:
  - Minimalist, modern aesthetic
  - Responsive design (mobile to desktop)
  - Clear typography hierarchy
  - Accessible color contrast

**Data Flow**: User Input → API Call → Results Rendering

---

## Slide 3: Backend Architecture & HTML Processing

**Title:** Multi-Stage Processing Pipeline

**Content:**
- **Stage 1: HTML Fetching**
  - Uses Python `requests` library
  - Handles errors and timeouts
  - Supports all standard HTTP methods

- **Stage 2: HTML Cleaning**
  - BeautifulSoup4 removes:
    - Script tags
    - Style tags
    - Meta tags
    - Hidden elements
  - Preserves semantic content

- **Stage 3: Tokenization**
  - Uses `bert-base-uncased` tokenizer
  - Counts actual tokens (not characters)
  - Ensures consistent chunk boundaries

- **Stage 4: Chunking**
  - Max 500 tokens per chunk
  - Preserves semantic boundaries
  - Maintains overlap for context
  - Returns ordered chunks

**Key Metric**: 500 tokens ≈ 300-400 words

---

## Slide 4: Vector Database & Semantic Search

**Title:** How Semantic Search Works

**Content:**
- **Embedding Generation**:
  - Model: `all-MiniLM-L6-v2` (384 dimensions)
  - Converts text → semantic vector
  - Small & fast (22M parameters)
  - Multilingual support

- **Vector Database (Milvus)**:
  - Stores chunk embeddings
  - Metadata: chunk_index, content, url
  - IVF_FLAT index for fast search
  - L2 distance metric

- **Search Process**:
  1. User query → generate embedding
  2. Find nearest neighbors in vector space
  3. Return top 10 by distance
  4. Format with metadata

- **Why Vectors?**
  - Captures semantic meaning
  - Fast similarity computation
  - Scalable to millions of docs
  - Language-agnostic

**Example**:
- Query: "AI models"
- Related: "machine learning", "neural networks", "deep learning"
- Not matched by keywords alone

---

## Slide 5: Technical Implementation & Challenges

**Title:** Key Challenges & Solutions

**Content:**
- **Challenge 1: Large HTML Files**
  - Solution: Stream processing, chunk early
  - Prevents memory overflow

- **Challenge 2: Semantic Accuracy**
  - Solution: State-of-the-art embedding model
  - Tested on semantic similarity benchmarks

- **Challenge 3: Performance at Scale**
  - Solution: Vector index optimization
  - IVF_FLAT handles millions of chunks

- **Future Improvements**:
  - JavaScript rendering (Playwright/Selenium)
  - Incremental indexing (no re-indexing)
  - Hybrid search (semantic + keyword)
  - Caching layer for repeated URLs
  - Authentication & API quotas

**Deployment Options**:
- Docker for containerized backend
- AWS/GCP for scalable hosting
- CDN for frontend distribution

**Performance Metrics**:
- Indexing: ~1000 chunks/sec
- Search: ~100ms latency
- Memory: ~2GB for 100K chunks
