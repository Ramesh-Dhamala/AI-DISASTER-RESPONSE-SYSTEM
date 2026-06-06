from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ FIX: correct environment variable name
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are DisasterGuard AI - Emergency Response Assistant for Nepal.

Your responsibilities:
- Flood safety and warnings
- Landslide prevention and safety
- Earthquake safety and aftershock guidance
- Forest fire safety and evacuation
- Emergency first aid guidance
- Evacuation routes
- Disaster recovery advice

Nepal Emergency Numbers:
- Police: 100
- Ambulance: 102
- Fire Brigade: 101
- Nepal Red Cross: 4270650
- NDRRMA: 1149

Rules:
1. Only answer disaster, safety, or emergency-related questions
2. If question is NOT related to disaster → reply:
   "I can only assist with disaster and emergency-related questions."
3. Always prioritize human safety
4. Give clear step-by-step instructions
5. If emergency → say CALL 100 IMMEDIATELY
6. Keep answers simple and calm
"""

def disaster_chat(message: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content