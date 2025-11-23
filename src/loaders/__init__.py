"""Factory pattern for data loaders in the RAG pipeline."""

from typing import Dict, Type
from .base_loader import AbstractDataLoader
from .pdf_loader import PDFLoader
from .csv_loader import CSVLoader
from .html_loader import HTMLLoader

# Registry of available loaders
_LOADER_REGISTRY: Dict[str, Type[AbstractDataLoader]] = {
    'pdf': PDFLoader,
    'csv': CSVLoader,
    'html': HTMLLoader,
}


def get_loader(file_type: str) -> AbstractDataLoader:
    """
    Factory function to create a loader instance based on file type.
    
    Args:
        file_type: Type of data source ('pdf', 'csv', 'html', etc.)
        
    Returns:
        An instance of the appropriate loader class
        
    Raises:
        ValueError: If the file type is not supported
        
    Example:
        >>> loader = get_loader('pdf')
        >>> documents = loader.load('/path/to/file.pdf')
    """
    file_type_lower = file_type.lower()
    
    if file_type_lower not in _LOADER_REGISTRY:
        available_types = ', '.join(_LOADER_REGISTRY.keys())
        raise ValueError(
            f"Unsupported file type: {file_type}. "
            f"Available types: {available_types}"
        )
    
    loader_class = _LOADER_REGISTRY[file_type_lower]
    return loader_class()


def register_loader(file_type: str, loader_class: Type[AbstractDataLoader]):
    """
    Register a new loader type for extensibility.
    
    Args:
        file_type: Type identifier (e.g., 'word', 's3', 'db')
        loader_class: Class that inherits from AbstractDataLoader
        
    Example:
        >>> from .word_loader import WordLoader
        >>> register_loader('word', WordLoader)
    """
    if not issubclass(loader_class, AbstractDataLoader):
        raise TypeError(
            f"Loader class must inherit from AbstractDataLoader, "
            f"got {loader_class.__name__}"
        )
    
    _LOADER_REGISTRY[file_type.lower()] = loader_class


# Export all loader classes and factory function
__all__ = [
    'AbstractDataLoader',
    'PDFLoader',
    'CSVLoader',
    'HTMLLoader',
    'get_loader',
    'register_loader',
]


