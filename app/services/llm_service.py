import requests
from app.config import Config

def generate_from_llm(prompt: str):
    response = requests.post(
        f"{Config.BASE_URL}/llm/chat",
        json={
            "token": Config.LLM_TOKEN,
            "chat": prompt
        }
    )
    
    # Debug Output dari API LLM
    # print("STATUS:", response.status_code)
    # print("RESPONSE:", response.text)

    if response.status_code != 200:
        raise Exception("LLM request failed")

    return response.json()