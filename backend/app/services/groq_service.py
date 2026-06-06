"""
GROQ Service for AI Chatbot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mock function for disaster chat (since we might not have GROQ API key)
def disaster_chat(user_message: str, context: dict = None):
    """
    Process disaster-related chat messages
    """
    try:
        # Try to import groq if available
        try:
            from groq import Groq
            
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                client = Groq(api_key=api_key)
                # Make API call here if needed
                pass
        except ImportError:
            pass
        
        # Simple response logic for now
        response = generate_disaster_response(user_message)
        
        return {
            "success": True,
            "response": response,
            "source": "AI Assistant"
        }
        
    except Exception as e:
        return {
            "success": False,
            "response": f"Error: {str(e)}",
            "source": "Error Handler"
        }

def generate_disaster_response(message: str) -> str:
    """Generate a response for disaster-related queries"""
    message_lower = message.lower()
    
    if "flood" in message_lower:
        return "Floods are caused by heavy rainfall or river overflow. Stay tuned to weather alerts, move to higher ground, and avoid walking or driving through floodwaters."
    elif "earthquake" in message_lower:
        return "During an earthquake: Drop, Cover, and Hold On. Stay away from windows, and after shaking stops, check for injuries and gas leaks."
    elif "landslide" in message_lower:
        return "Landslides often occur in hilly areas after heavy rain. Watch for signs like cracking sounds or falling debris, and evacuate immediately if detected."
    elif "cyclone" in message_lower or "hurricane" in message_lower:
        return "Cyclones bring strong winds and heavy rain. Secure your home, stock emergency supplies, and follow evacuation orders if given."
    elif "safety" in message_lower:
        return "For any disaster: Always have an emergency kit ready, know evacuation routes, keep important documents safe, and follow local authorities' instructions."
    elif "alert" in message_lower or "warning" in message_lower:
        return "Monitor official weather channels and disaster management authorities for real-time alerts and warnings in your area."
    else:
        return "I'm your AI disaster response assistant. You can ask me about floods, earthquakes, landslides, cyclones, safety measures, or emergency preparedness."