"""The purpose of this module is to provide a simple interface for querying Ollama."""

import httpx
import json

async def query_ollama(prompt: str, model: str) -> str | None:
    """
    Query the Ollama model with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the model
        model (str): The name of the Ollama model to use
        
    Returns:
        str | None: The model's response or None if the query fails
    """
    try:
        print(f"[DEBUG] Starting Ollama query...")
        print(f"[DEBUG] Model: {model}")
        print(f"[DEBUG] Prompt: {prompt}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                health_check = await client.get("http://localhost:11434/api/version")
                print(f"[DEBUG] Ollama server status: {health_check.status_code}")
            except Exception as e:
                print(f"[DEBUG] Ollama server not responding: {e}")
                return json.dumps({"error": "Ollama server not responding"})

            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            print(f"[DEBUG] Sending request to Ollama...")
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=payload,
            )
            
            print(f"[DEBUG] Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response content")
            else:
                error_msg = f"Error from Ollama API: {response.status_code}"
                print(f"[DEBUG] {error_msg}")
                return json.dumps({"error": error_msg})
                
    except Exception as e:
        error_msg = f"Error querying Ollama: {str(e)}"
        print(f"[DEBUG] {error_msg}")
        return json.dumps({"error": error_msg})

if __name__ == "__main__":
    prompt = """ 
    User: "How many letters in the english alphabet?"

    Assistant: (return a concise answer to the user's question)
    """
    
    result = query_ollama(prompt)
    print(result)