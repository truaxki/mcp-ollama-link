"""The purpose of this module is to provide a simple interface for querying Ollama."""

import requests
from typing import Optional

def query_ollama(prompt: str, model: str = "deepseek-r1:32b") -> Optional[str]:
    """
    Send a single query to Ollama model and get a response.
    
    Args:
        prompt: The input text to send to the model
        model: Name of the Ollama model to use
    
    Returns:
        str: The model's response or None if there's an error
    """
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()['response']
    except Exception as e:
        print(f"Error in query: {e}")
        return None

if __name__ == "__main__":
    prompt = """ 
    User: "How many letters in the english alphabet?"

    Assistant: (return a concise answer to the user's question)
    """
    
    result = query_ollama(prompt)
    print(result)