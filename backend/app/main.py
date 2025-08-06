# /backend/app/main.py
import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.chat_models import ChatRequest
from app.prompts.system_prompts import SYSTEM_PROMPT
from app.services.ecommerce_service import check_order_status, process_return_request, request_human_agent

# ... (FastAPI app and middleware setup remains the same) ...
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


async def detect_language_with_llm(text: str) -> str:
    prompt = f"Detect the language of the following text. Respond with only the language name in English, such as 'Tamil', 'English', or 'Hindi'. Do not add any other words or punctuation. Text: '{text}'"
    detection_response = await get_llm_response([{"role": "user", "content": prompt}])
    detected_language = detection_response.strip().capitalize()
    if ' ' in detected_language or len(detected_language) > 15: return "English"
    return detected_language

@app.post("/chat")
async def handle_chat(request: ChatRequest):
    if request.language and request.language in ["English", "Tamil", "Hindi"]:
        language_name = request.language
    else:
        language_name = await detect_language_with_llm(request.message)

    dynamic_system_prompt = f"{SYSTEM_PROMPT}\n\nLanguage for response: {language_name}."
    messages = [{"role": "system", "content": dynamic_system_prompt}] + request.history + [{"role": "user", "content": request.message}]
    llm_response_text = await get_llm_response(messages)

    tool_call_match = re.search(r'\{.*\}', llm_response_text, re.DOTALL)
    if tool_call_match:
        json_str = tool_call_match.group(0)
        try:
            json_response = json.loads(json_str)
            tool_to_use = json_response.get("tool_to_use")
            tool_result = None
            if tool_to_use:
                if tool_to_use == "check_order_status":
                    tool_result = check_order_status(order_number=json_response["parameters"]["order_number"])
                elif tool_to_use == "process_return_request":
                    tool_result = process_return_request(order_number=json_response["parameters"]["order_number"], reason=json_response["parameters"]["reason"])
                elif tool_to_use == "request_human_agent":
                    tool_result = request_human_agent(issue=json_response["parameters"]["issue"])
            
            if tool_result:
                tool_messages = [
                    {"role": "system", "content": dynamic_system_prompt},
                    {"role": "assistant", "content": llm_response_text},
                    {"role": "tool", "content": json.dumps(tool_result)},
                    # --- THIS IS THE CRITICAL FIX ---
                    # Add a final, explicit command to ensure the response is in the correct language.
                    {"role": "user", "content": f"Based on the tool's output, formulate a response to the user in {language_name}."}
                ]
                final_response = await get_llm_response(tool_messages)
                return {"response": final_response, "task_complete": True, "language": language_name}
        except json.JSONDecodeError:
            pass
    
    return {"response": llm_response_text, "task_complete": False, "language": language_name}