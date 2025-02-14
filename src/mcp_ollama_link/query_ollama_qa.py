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
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Quick health check without logging
            try:
                await client.get("http://localhost:11434/api/version")
            except httpx.ConnectError:
                print("Failed to connect to Ollama server")
                return None
            except httpx.TimeoutException:
                print("Timeout while checking Ollama server")
                return None

            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            try:
                response = await client.post(
                    "http://localhost:11434/api/generate",
                    json=payload,
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "No response content")
                else:
                    print(f"Ollama returned status code: {response.status_code}")
                    return None
                    
            except httpx.ConnectError:
                print("Lost connection to Ollama server during query")
                return None
            except httpx.TimeoutException:
                print("Timeout while waiting for Ollama response")
                return None
                
    except Exception as e:
        print(f"Unexpected error while querying Ollama: {str(e)}")
        return None

if __name__ == "__main__":
    prompt = """ 
    User: "How many letters in the english alphabet?"

    Assistant: (return a concise answer to the user's question)
    """
    
    result = query_ollama(prompt)
    print(result)