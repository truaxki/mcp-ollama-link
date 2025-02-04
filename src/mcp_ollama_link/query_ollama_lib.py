from ollama import Client
from typing import List, Dict

# Create a single client instance
client = Client(host='http://localhost:11434')

def query_ollama_stream(messages: List[Dict[str, str]]):
    try:
        response_content = ""
        # Stream the response
        for chunk in client.chat(
            model='llama2',
            messages=messages,
            stream=True
        ):
            if 'content' in chunk['message']:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                response_content += content
        # Return only the latest response
        return response_content
    except Exception as e:
        print(f"Error in streaming: {e}")
        return None

if __name__ == "__main__":
    # Initialize conversation history
    messages = []
    
    print("Start chatting! (type 'quit' to exit)")
    while True:
        # Get user input
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        # Add user message to history
        messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get and print assistant's response
        print("\nAssistant: ", end='')
        assistant_response = query_ollama_stream(messages)
        
        # Add assistant's response to history
        if assistant_response:
            messages.append({
                'role': 'assistant',
                'content': assistant_response
            })