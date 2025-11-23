"""Example usage of the RAG data ingestion loaders."""

from src.loaders import get_loader
from config import CrawlerConfig


def example_pdf_loader():
    """Example of loading a PDF file."""
    print("=" * 60)
    print("Example: PDF Loader")
    print("=" * 60)
    
    # Get PDF loader using factory pattern
    loader = get_loader('pdf')
    
    # Load PDF file (replace with your actual PDF path)
    pdf_path = "example.pdf"  # Update this path
    try:
        documents = loader.load(pdf_path)
        
        print(f"Loaded {len(documents)} document(s) from PDF")
        for i, doc in enumerate(documents):
            print(f"\nDocument {i+1}:")
            print(f"  Source: {doc.source_uri}")
            print(f"  Type: {doc.doc_type}")
            print(f"  Content length: {len(doc.content)} characters")
            print(f"  Metadata: {doc.metadata}")
            print(f"  Content preview: {doc.content[:200]}...")
            
    except FileNotFoundError:
        print(f"PDF file not found: {pdf_path}")
        print("Please update the path to a valid PDF file.")
    except Exception as e:
        print(f"Error: {e}")


def example_csv_loader():
    """Example of loading a CSV file."""
    print("\n" + "=" * 60)
    print("Example: CSV Loader")
    print("=" * 60)
    
    # Get CSV loader using factory pattern
    loader = get_loader('csv')
    
    # Load CSV file (replace with your actual CSV path)
    csv_path = "example.csv"  # Update this path
    try:
        documents = loader.load(csv_path)
        
        print(f"Loaded {len(documents)} document(s) from CSV")
        for i, doc in enumerate(documents[:3]):  # Show first 3
            print(f"\nDocument {i+1}:")
            print(f"  Source: {doc.source_uri}")
            print(f"  Type: {doc.doc_type}")
            print(f"  Content: {doc.content}")
            print(f"  Metadata: {doc.metadata}")
            
        if len(documents) > 3:
            print(f"\n... and {len(documents) - 3} more documents")
            
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
        print("Please update the path to a valid CSV file.")
    except Exception as e:
        print(f"Error: {e}")


def example_html_loader():
    """Example of loading HTML content via web crawler."""
    print("\n" + "=" * 60)
    print("Example: HTML Loader (Web Crawler)")
    print("=" * 60)
    
    # Configure crawler
    config = CrawlerConfig(
        stay_in_domain=True,
        max_depth=1,  # Only crawl the starting page and one level deep
        follow_links=True,
        max_links_per_page=5
    )
    
    # Get HTML loader with custom config
    from src.loaders.html_loader import HTMLLoader
    loader = HTMLLoader(config=config)
    
    # Or use factory pattern (will use default config)
    # loader = get_loader('html')
    
    # Load HTML from URL (replace with your actual URL)
    url = "https://example.com"  # Update this URL
    try:
        documents = loader.load(url)
        
        print(f"Loaded {len(documents)} document(s) from HTML crawl")
        for i, doc in enumerate(documents):
            print(f"\nDocument {i+1}:")
            print(f"  Source: {doc.source_uri}")
            print(f"  Type: {doc.doc_type}")
            print(f"  Content length: {len(doc.content)} characters")
            print(f"  Metadata: {doc.metadata}")
            print(f"  Content preview: {doc.content[:200]}...")
            
    except Exception as e:
        print(f"Error: {e}")


def example_factory_pattern():
    """Example demonstrating the factory pattern extensibility."""
    print("\n" + "=" * 60)
    print("Example: Factory Pattern Usage")
    print("=" * 60)
    
    # Factory pattern allows easy switching between loader types
    file_types = ['pdf', 'csv', 'html']
    
    for file_type in file_types:
        try:
            loader = get_loader(file_type)
            print(f"✓ Successfully created {file_type.upper()} loader: {type(loader).__name__}")
        except ValueError as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    print("RAG Pipeline - Data Ingestion Examples")
    print("=" * 60)
    
    # Run examples
    example_factory_pattern()
    example_pdf_loader()
    example_csv_loader()
    example_html_loader()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nNote: Update the file paths/URLs in the examples to use your own data.")


