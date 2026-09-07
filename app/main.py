from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import get_llm_response

app = FastAPI(
    title="HNB AI Assistant API",
    description="Internal assistant powered by LangChain and Google Gemini",
)

# Enable CORS for network and mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Whitelist of authorized staff
ALLOWED_USERS = {"hiruka", "shenali", "lakshitha"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "HNB AI Service"}

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_bot(payload: ChatRequest):
    # 1. Check if user is on the allowed list
    cleaned_name = payload.user_name.strip().lower()
    if cleaned_name not in ALLOWED_USERS:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You are not authorized to use this assistant."
        )

    # 2. Check message content
    cleaned_message = payload.message.strip()
    if not cleaned_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # 3. Generate response from Gemini
    try:
        ai_reply = await get_llm_response(cleaned_message)
        return ChatResponse(
            user_name=payload.user_name,
            reply=ai_reply,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")