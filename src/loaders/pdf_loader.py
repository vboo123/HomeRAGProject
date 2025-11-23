"""PDF loader implementation using PyMuPDF."""

from typing import List
from pathlib import Path
import fitz  # PyMuPDF

from .base_loader import AbstractDataLoader
from ..models.document import Document


class PDFLoader(AbstractDataLoader):
    """
    Loader for PDF files using PyMuPDF (fitz).
    
    Extracts text content from PDF files and preserves page numbers
    in metadata for better context tracking.
    """
    
    def load(self, source_path: str) -> List[Document]:
        """
        Load and extract text from a PDF file.
        
        Args:
            source_path: Path to the PDF file
            
        Returns:
            List containing a single Document object with all PDF content,
            or multiple Documents if split by pages (configurable)
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file cannot be opened or is not a valid PDF
        """
        if not self.validate_source(source_path):
            raise FileNotFoundError(f"PDF file not found: {source_path}")
        
        try:
            # Open the PDF document
            pdf_doc = fitz.open(source_path)
            
            # Extract text from all pages
            full_text = []
            page_texts = []
            
            for page_num in range(len(pdf_doc)):
                page = pdf_doc[page_num]
                page_text = page.get_text()
                full_text.append(page_text)
                page_texts.append({
                    "page_number": page_num + 1,
                    "text": page_text
                })
            
            pdf_doc.close()
            
            # Combine all pages into a single document
            content = "\n\n".join(full_text)
            
            # Extract metadata
            metadata = self.extract_metadata(
                source_path,
                total_pages=len(pdf_doc),
                page_texts=page_texts,
                file_name=Path(source_path).name,
                file_size=Path(source_path).stat().st_size
            )
            
            return [Document(
                content=content,
                source_uri=str(Path(source_path).absolute()),
                doc_type="pdf",
                metadata=metadata
            )]
            
        except Exception as e:
            raise ValueError(f"Error loading PDF file {source_path}: {str(e)}")


