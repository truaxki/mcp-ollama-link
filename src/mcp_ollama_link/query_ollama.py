"""The purpose of this module is to provide a simple interface for querying Ollama."""

import requests

def query_ollama(prompt, model="deepseek-r1:32b"):
    response = requests.post('http://localhost:11434/api/generate',
        json={
            "model": model,

            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()['response']
# Read the JSON file and create a focused prompt
with open('2025-01-28-meta-memory.json', 'r') as file:
    content = file.read()



prompt = """ 
  User: "How many letters in the english alphabet?"

  Assistant: (return a consise answe to the user's question)
"""
result = query_ollama(prompt)
print(result)