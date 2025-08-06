# /backend/app/services/openrouter_service.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Recommended model, but you can use others like "openai/gpt-4o"
MODEL_NAME = "meta-llama/llama-3.3-70b-instruct" 

async def get_llm_response(prompt_messages: list) -> str:
    """
    Calls the OpenRouter API to get a response from the specified model.
    """
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY is not set."

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
                },
                json={
                    "model": MODEL_NAME,
                    "messages": prompt_messages
                }
            )
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            return data['choices'][0]['message']['content']
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return f"Error communicating with AI service: {e.response.text}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred while contacting the AI service."