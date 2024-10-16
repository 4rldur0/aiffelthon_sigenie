from models.validation_check.rag_model import app

def validate_compliance(question: str):
    """
    Function to validate shipping instruction data against compliance.
    Args:
        question (str): The question or query to check for compliance.
    
    Returns:
        str: Generated compliance report or validation result.
    """
    try:
        response = app.invoke(question)
        return response
    except Exception as e:
        raise RuntimeError(f"Error during compliance validation: {e}")