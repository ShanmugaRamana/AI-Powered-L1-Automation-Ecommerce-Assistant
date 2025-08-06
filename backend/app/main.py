# /backend/app/main.py
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.chat_models import ChatRequest
from app.prompts.system_prompts import SYSTEM_PROMPT
from app.services.openrouter_service import get_llm_response
from app.services.ecommerce_service import check_order_status

app = FastAPI()

# Setup CORS middleware to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # The origin of our frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def handle_chat(request: ChatRequest):
    # 1. Construct the prompt with history and the new message
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + request.history + [{"role": "user", "content": request.message}]

    # 2. Get the initial response from the LLM
    llm_response_text = await get_llm_response(messages)

    # 3. Check if the LLM wants to use a tool
    try:
        # The LLM might return a JSON string wrapped in markdown, so we find it
        json_response = json.loads(llm_response_text[llm_response_text.find('{'):llm_response_text.rfind('}')+1])
        
        if json_response.get("tool_to_use") == "check_order_status":
            # 4. If so, execute the tool
            order_number = json_response["parameters"]["order_number"]
            tool_result = check_order_status(order_number)

            # 5. Send the tool's result back to the LLM to get a natural language response
            tool_messages = messages + [
                {"role": "assistant", "content": llm_response_text},
                {"role": "tool", "content": json.dumps(tool_result), "tool_call_id": "null"} # Role "tool" is a concept here
            ]
            final_response = await get_llm_response(tool_messages)
            return {"response": final_response}

    except (json.JSONDecodeError, KeyError):
        # 4b. If the response is not a valid JSON or tool call, it's a direct answer.
        pass

    # 5b. Return the direct answer
    return {"response": llm_response_text}