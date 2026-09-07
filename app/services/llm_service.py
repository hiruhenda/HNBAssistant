import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not found in your .env file!")

# 2. Configure Gemini 3.5 Flash-Lite
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key
)

# 3. Bank Assistant Persona Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an intelligent internal assistant for Hatton National Bank (HNB). You assist bank employees courteously, clearly, and concisely."),
    ("human", "{question}")
])

# 4. LangChain LCEL pipeline
chain = prompt | llm | StrOutputParser()

async def get_llm_response(question: str) -> str:
    """Asynchronously passes the question to Gemini."""
    response = await chain.ainvoke({"question": question})
    return response