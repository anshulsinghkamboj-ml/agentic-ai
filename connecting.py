from dotenv import load_dotenv
import os
from openai import OpenAI
import ollama
import time
from ollama import Client
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')

def stream_chatollama(user_message,max_retries=5,base_delay=2.0):
    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message},]
    
    attempt=0

    while attempt <=max_retries:
        try:
            for part in client.chat(model="gpt-oss:120b",messages=messages,stream=True) :
                msg=part.get("message",{})
                chunk = msg.get("content")
                if chunk:
                    yield chunk
            return 


        except Exception as e:
            attempt +=1
            if attempt > max_retries:raise RuntimeError( f"stream_chatollama failed after {max_retries} retries") from e
            delay = base_delay * (2 ** (attempt - 1))
            time.sleep(delay)
        
    


def ask_chatgpt(user_message):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",  # gpt-4 turbo or a model of your preference
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": user_message}],
        temperature=0.7,
        )       
    return response.choices[0].message.content

user = "What is the capital of France?"
response = ask_chatgpt(user)
print(response)
print('-'*10)
for chunk in stream_chatollama("Tell me something wise."):
    print(chunk, end="", flush=True)