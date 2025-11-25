import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer
import logging

logger = logging.getLogger(__name__)

def fetch_html(url: str) -> str:
    """Fetch HTML content from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        raise

def clean_html(html_content: str) -> str:
    """Clean HTML by removing scripts, styles, and other unwanted elements."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove script and style elements
    for script in soup(["script", "style", "meta", "link"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = " ".join(chunk for chunk in chunks if chunk)
    
    return text

def tokenize_text(text: str, tokenizer_model: str = "bert-base-uncased"):
    """Tokenize text using HuggingFace tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model)
    tokens = tokenizer.tokenize(text)
    return tokens

def chunk_text(text: str, max_tokens: int = 500, tokenizer_model: str = "bert-base-uncased") -> list:
    """Split text into chunks with max token limit."""
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model)
    tokens = tokenizer.tokenize(text)
    
    chunks = []
    current_chunk = []
    
    for token in tokens:
        current_chunk.append(token)
        if len(current_chunk) >= max_tokens:
            chunk_text = tokenizer.convert_tokens_to_string(current_chunk)
            chunks.append(chunk_text)
            current_chunk = []
    
    # Add remaining tokens
    if current_chunk:
        chunk_text = tokenizer.convert_tokens_to_string(current_chunk)
        chunks.append(chunk_text)
    
    logger.info(f"Created {len(chunks)} chunks from text")
    return chunks
