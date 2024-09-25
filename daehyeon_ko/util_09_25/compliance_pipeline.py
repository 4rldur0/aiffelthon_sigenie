# Import libraries
from rag_model import RAGModel  # Import the RAGModel class
import logging

# Set up logging for error tracking
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize the RAGModel instance with document sources
sources = [
              # Replace with your URLs
              "company_policy.pdf"  # Replace with the actual PDF file path
]

app = RAGModel(sources=sources)

def validate_compliance(question: str):
    """
    Validate compliance for the given question or query.
    Args:
        question (str): The question or query to check for compliance.
    
    Returns:
        str: Generated compliance report or validation result.
    """
    try:
        response = app.invoke(question)
        return response
    except RuntimeError as e:
        logging.error(f"RuntimeError in validate_compliance: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in validate_compliance: {e}")
        raise RuntimeError(f"Error during compliance validation: {e}")
