"""Abstract base class for all data loaders in the RAG pipeline."""

from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from ..models.document import Document


class AbstractDataLoader(ABC):
    """
    Abstract base class defining the interface for all data loaders.
    
    All concrete loaders (PDFLoader, CSVLoader, HTMLLoader, etc.) must
    inherit from this class and implement the load() method.
    """
    
    @abstractmethod
    def load(self, source_path: str) -> List[Document]:
        """
        Load data from the source and convert it to standardized Document objects.
        
        Args:
            source_path: Path to the data source (file path, URL, etc.)
            
        Returns:
            List of Document objects containing the extracted content and metadata
            
        Raises:
            FileNotFoundError: If the source file doesn't exist (for file-based loaders)
            ValueError: If the source is invalid or cannot be processed
        """
        pass
    
    def validate_source(self, source_path: str) -> bool:
        """
        Validate that the source exists and is accessible.
        
        Args:
            source_path: Path to validate
            
        Returns:
            True if source is valid, False otherwise
        """
        if not source_path:
            return False
        
        # For file-based loaders, check if file exists
        if not source_path.startswith(('http://', 'https://')):
            return Path(source_path).exists()
        
        # For URL-based loaders, assume valid (actual validation in loader)
        return True
    
    def extract_metadata(self, source_path: str, **kwargs) -> dict:
        """
        Extract metadata from the source.
        
        Args:
            source_path: Path to the source
            **kwargs: Additional keyword arguments for metadata extraction
            
        Returns:
            Dictionary containing extracted metadata
        """
        return {
            "source_path": source_path,
            **kwargs
        }


