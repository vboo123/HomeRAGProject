# HomeRAGProject

RAG project to learn how to develop and scale RAG pipelines for creating a knowledge base for all of our home documents.

## Current Status

### ✅ Completed: Data Ingestion Layer

The data ingestion layer is fully implemented and functional. This layer handles the conversion of raw data sources (PDF, CSV, HTML) into standardized `Document` objects that are ready for the next stages of the RAG pipeline (chunking, embedding, vectorization).

**Implemented Features:**
- ✅ Hierarchical class structure with abstract base class (`AbstractDataLoader`)
- ✅ Factory pattern for extensible loader creation
- ✅ PDF loader using PyMuPDF
- ✅ CSV loader using pandas (supports row-as-document or single document modes)
- ✅ HTML loader with basic web crawler functionality
- ✅ Standardized `Document` model for consistent data representation
- ✅ Configuration system for crawler settings

**Next Steps:**
- ⏳ Chunking layer (split documents into smaller pieces)
- ⏳ Embedding layer (convert chunks to vectors)
- ⏳ Vector store integration
- ⏳ Retrieval logic
- ⏳ LLM integration (local DeepSeek/Llama)

## Project Structure

```
HomeRAGProject/
├── requirements.txt          # Python dependencies
├── config.py                 # Crawler configuration settings
├── example_usage.py          # Usage examples for all loaders
├── README.md                 # This file
└── src/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py
    │   └── document.py       # Standardized Document dataclass
    └── loaders/
        ├── __init__.py       # Factory pattern implementation
        ├── base_loader.py    # Abstract base class
        ├── pdf_loader.py     # PDF file loader
        ├── csv_loader.py     # CSV file loader
        └── html_loader.py    # HTML/web crawler loader
```

## How Data Ingestion Works

### Overview

The data ingestion layer follows a **factory pattern** with a **hierarchical class structure** to convert diverse data sources into a standardized format:

```
Raw Data Source → Loader → Standardized Document → Ready for Chunking
   (PDF/CSV/HTML)    ↓           (Document object)      (Next step)
```

### Document Creation Process

1. **Factory Pattern Selection**: Use `get_loader(file_type)` to get the appropriate loader
2. **Source Validation**: Loader validates the source exists/is accessible
3. **Data Extraction**: Loader-specific extraction (PDF text, CSV rows, HTML content)
4. **Metadata Collection**: Gather format-specific metadata (page numbers, row indices, URLs)
5. **Document Creation**: Convert to standardized `Document` object

### Document Model

All loaders return `Document` objects with this structure:

```python
@dataclass
class Document:
    content: str              # Extracted raw text content
    source_uri: str           # Original path/URL/identifier
    doc_type: str            # Type identifier ('pdf', 'csv', 'html')
    metadata: Dict[str, Any] # Format-specific metadata
```

**Document Validation:**
- `content` cannot be empty
- `source_uri` cannot be empty
- `doc_type` cannot be empty

### Loader Behavior

#### PDF Loader
- **Input**: PDF file path
- **Output**: 1 `Document` per PDF file (all pages combined)
- **Metadata**: Includes `total_pages`, `file_name`, `file_size`, `page_texts`

#### CSV Loader
- **Input**: CSV file path
- **Output**: 
  - **Default mode** (`row_as_document=True`): 1 `Document` per CSV row
  - **Single document mode** (`row_as_document=False`): 1 `Document` for entire CSV
- **Metadata**: Includes `row_index`, `columns`, `total_rows`, `file_name`

#### HTML Loader
- **Input**: Starting URL
- **Output**: 1 `Document` per crawled page
- **Features**: 
  - Domain restriction (stays within same domain)
  - Configurable max depth and link following
  - Extracts main content (removes navigation, scripts, etc.)
- **Metadata**: Includes `title`, `depth`, `content_length`, `source_path`

### Example Output

Loading **5 PDFs** and **2 CSVs** (with default CSV mode):

```python
# 5 PDFs → 5 Documents (1 per PDF)
# 2 CSVs (100 rows + 50 rows) → 150 Documents (1 per row)
# Total: 155 Documents
```

All returned as a list of `Document` objects, ready for chunking and embedding.

## Usage Examples

### Basic Usage

```python
from src.loaders import get_loader

# Get a loader using the factory pattern
loader = get_loader('pdf')

# Load documents
documents = loader.load('/path/to/file.pdf')

# Each document is a standardized Document object
for doc in documents:
    print(f"Type: {doc.doc_type}")
    print(f"Source: {doc.source_uri}")
    print(f"Content length: {len(doc.content)} characters")
    print(f"Metadata: {doc.metadata}")
```

### Processing Multiple Files

```python
from src.loaders import get_loader

files = [
    ('pdf', '/data/report1.pdf'),
    ('pdf', '/data/report2.pdf'),
    ('csv', '/data/customers.csv'),
    ('html', 'https://docs.example.com')
]

all_documents = []

for file_type, path in files:
    loader = get_loader(file_type)
    documents = loader.load(path)
    all_documents.extend(documents)

print(f"Total documents loaded: {len(all_documents)}")
```

### CSV Loader Configuration

```python
from src.loaders.csv_loader import CSVLoader

# Default: One document per row
loader = CSVLoader(row_as_document=True)
documents = loader.load('data.csv')  # Returns many Documents

# Alternative: One document for entire CSV
loader = CSVLoader(row_as_document=False)
documents = loader.load('data.csv')  # Returns 1 Document
```

### HTML Crawler Configuration

```python
from src.loaders.html_loader import HTMLLoader
from config import CrawlerConfig

# Custom crawler configuration
config = CrawlerConfig(
    stay_in_domain=True,
    max_depth=2,
    follow_links=True,
    max_links_per_page=10
)

loader = HTMLLoader(config=config)
documents = loader.load('https://example.com')
```

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run examples:**
   ```bash
   python example_usage.py
   ```

## Extensibility

### Adding New Loaders

The factory pattern makes it easy to add new data source types:

1. **Create a new loader class:**
   ```python
   from src.loaders.base_loader import AbstractDataLoader
   from src.models.document import Document
   
   class WordLoader(AbstractDataLoader):
       def load(self, source_path: str) -> List[Document]:
           # Your implementation
           return [Document(...)]
   ```

2. **Register it:**
   ```python
   from src.loaders import register_loader
   register_loader('word', WordLoader)
   ```

3. **Use it:**
   ```python
   loader = get_loader('word')  # Works automatically!
   ```

## Architecture Decisions

- **Factory Pattern**: Centralizes object creation, enables runtime registration, supports configuration-driven loading
- **Hierarchical Classes**: All loaders inherit from `AbstractDataLoader`, ensuring consistent interface
- **Standardized Documents**: All sources convert to same `Document` format, simplifying downstream processing
- **Metadata Preservation**: Format-specific metadata is preserved for advanced RAG features (filtering, reranking)

## Future Enhancements

- [ ] Word document loader (.docx)
- [ ] S3 object loader
- [ ] Database loaders (PostgreSQL, MongoDB)
- [ ] Advanced chunking strategies
- [ ] Embedding integration
- [ ] Vector store integration
- [ ] LLM integration (local DeepSeek/Llama)
