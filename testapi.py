import openai
import time
import os
from dotenv import load_dotenv
load_dotenv()

#openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

print(openai.api_key)
def call_openai_api(retry_count=5):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        return response
    except openai.error.RateLimitError as e:
        if retry_count > 0:
            print("Rate limit exceeded. Retrying...")
            time.sleep(10)  # Wait for a bit before retrying
            return call_openai_api(retry_count - 1)
    except Exception as e:
        print(f"An error occurred: {e}")

response = call_openai_api()
print(response)
