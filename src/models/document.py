"""Standardized document model for RAG pipeline."""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Document:
    """
    Standardized document representation for the RAG pipeline.
    
    This model ensures all data sources (PDF, CSV, HTML, etc.) are converted
    to a consistent format before chunking and embedding.
    
    Attributes:
        content: The extracted raw text content from the source
        source_uri: The original path, URL, or identifier of the source
        doc_type: Type identifier (e.g., 'pdf', 'csv', 'html', 's3', 'db')
        metadata: Flexible dictionary for additional context (page numbers,
                  headers, creation dates, etc.)
    """
    
    content: str
    source_uri: str
    doc_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate document fields after initialization."""
        if not self.content:
            raise ValueError("Document content cannot be empty")
        if not self.source_uri:
            raise ValueError("Document source_uri cannot be empty")
        if not self.doc_type:
            raise ValueError("Document doc_type cannot be empty")


