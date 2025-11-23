"""CSV loader implementation using pandas."""

from typing import List
from pathlib import Path
import pandas as pd

from .base_loader import AbstractDataLoader
from ..models.document import Document


class CSVLoader(AbstractDataLoader):
    """
    Loader for CSV files using pandas.
    
    Converts CSV rows into Document objects. Each row can be treated
    as a separate document, or the entire CSV can be converted to text.
    """
    
    def __init__(self, row_as_document: bool = True):
        """
        Initialize the CSV loader.
        
        Args:
            row_as_document: If True, each row becomes a separate Document.
                           If False, the entire CSV is converted to a single Document.
        """
        self.row_as_document = row_as_document
    
    def load(self, source_path: str) -> List[Document]:
        """
        Load and extract data from a CSV file.
        
        Args:
            source_path: Path to the CSV file
            
        Returns:
            List of Document objects. If row_as_document=True, one Document per row.
            If False, a single Document containing all CSV data.
            
        Raises:
            FileNotFoundError: If the CSV file doesn't exist
            ValueError: If the file cannot be parsed as CSV
        """
        if not self.validate_source(source_path):
            raise FileNotFoundError(f"CSV file not found: {source_path}")
        
        try:
            # Read CSV file
            df = pd.read_csv(source_path)
            
            if self.row_as_document:
                # Convert each row to a separate document
                documents = []
                for idx, row in df.iterrows():
                    # Convert row to text representation
                    row_text = "\n".join([f"{col}: {row[col]}" for col in df.columns])
                    
                    metadata = self.extract_metadata(
                        source_path,
                        row_index=idx,
                        columns=list(df.columns),
                        file_name=Path(source_path).name,
                        total_rows=len(df)
                    )
                    
                    documents.append(Document(
                        content=row_text,
                        source_uri=f"{source_path}#row_{idx}",
                        doc_type="csv",
                        metadata=metadata
                    ))
                
                return documents
            else:
                # Convert entire CSV to a single document
                # Convert DataFrame to a readable text format
                content = df.to_string(index=False)
                
                metadata = self.extract_metadata(
                    source_path,
                    columns=list(df.columns),
                    total_rows=len(df),
                    total_columns=len(df.columns),
                    file_name=Path(source_path).name,
                    file_size=Path(source_path).stat().st_size
                )
                
                return [Document(
                    content=content,
                    source_uri=str(Path(source_path).absolute()),
                    doc_type="csv",
                    metadata=metadata
                )]
                
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file is empty: {source_path}")
        except Exception as e:
            raise ValueError(f"Error loading CSV file {source_path}: {str(e)}")


