# pyrefly: ignore [missing-import]
import httpx
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq

def get_llm(temperature=0.0):
    """
    Returns a ChatGroq instance configured to use IPv4.
    This fixes APIConnectionError issues on cloud platforms like Railway 
    that default to IPv6 which sometimes fails to route to Groq API.
    """
    # Force IPv4 by binding to 0.0.0.0
    transport = httpx.HTTPTransport(local_address="0.0.0.0")
    client = httpx.Client(transport=transport, timeout=60.0)
    
    import os
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    
    return ChatGroq(
        model="llama-3.3-70b-versatile", 
        temperature=temperature,
        http_client=client,
        api_key=api_key
    )
