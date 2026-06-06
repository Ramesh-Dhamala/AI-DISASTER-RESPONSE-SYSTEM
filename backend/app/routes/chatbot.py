from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import re

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    context: Optional[Dict[str, Any]] = None

# Comprehensive disaster response database
DISASTER_RESPONSES = {
    # Flood related questions
    "flood_causes": "Floods are caused by: 🌊\n• Heavy rainfall lasting several days\n• Rapid snow/ice melt\n• River overflow or dam breaks\n• Storm surges from cyclones/hurricanes\n• Poor drainage systems in urban areas",
    
    "flood_prevention": "Flood prevention measures: 🛡️\n• Build on higher ground\n• Install proper drainage systems\n• Create retention ponds\n• Maintain rivers and canals\n• Plant trees to reduce runoff\n• Build flood barriers/levees\n• Use permeable pavements",
    
    "flood_safety": "During a flood: ⚠️\n• Move to higher ground IMMEDIATELY\n• Never walk or drive through flood water\n• Turn off gas and electricity\n• Listen to emergency broadcasts\n• Evacuate if authorities advise\n• Avoid bridges over fast-moving water",
    
    "flood_after": "After a flood: 🔧\n• Wait for authorities to say it's safe\n• Avoid floodwater (may be contaminated)\n• Check for structural damage\n• Don't use flooded appliances\n• Clean and disinfect everything\n• Watch for mold growth",
    
    "flood_kit": "Flood emergency kit: 🎒\n• 3+ days water and food\n• Battery-powered radio\n• Flashlight and extra batteries\n• First aid kit\n• Medications (7+ days supply)\n• Important documents (waterproof)\n• Cash and credit cards\n• Whistle to signal for help",
    
    # Earthquake related questions
    "earthquake_causes": "Earthquakes are caused by: 🌍\n• Movement of tectonic plates\n• Volcanic activity\n• Underground explosions\n• Collapse of underground mines\n• Fault line ruptures",
    
    "earthquake_safety": "During earthquake - DROP, COVER, HOLD ON! 🏠\n• DROP to the ground\n• Take COVER under sturdy furniture\n• HOLD ON until shaking stops\n• Stay away from windows\n• If outside, move to open area\n• If driving, pull over and stop\n• Don't use elevators",
    
    "earthquake_prepare": "Earthquake preparation: ✅\n• Secure heavy furniture to walls\n• Keep emergency supplies ready\n• Know how to turn off gas/water\n• Practice Drop, Cover, Hold On drills\n• Identify safe spots in each room\n• Keep shoes and flashlight by bed",
    
    "earthquake_after": "After earthquake: 🔍\n• Check for injuries and gas leaks\n• Expect aftershocks\n• Wear sturdy shoes\n• Listen to emergency broadcasts\n• Check for structural damage\n• Don't enter damaged buildings\n• Use text messages (phone lines busy)",
    
    # Landslide related questions
    "landslide_causes": "Landslides are triggered by: ⛰️\n• Heavy or prolonged rainfall\n• Earthquakes or vibrations\n• Steep slopes and erosion\n• Deforestation and construction\n• Snowmelt or glacier melting\n• Volcanic activity",
    
    "landslide_warning": "Warning signs of landslides: ⚠️\n• Cracking sounds in ground\n• Doors/windows stick or jam\n• New cracks in walls/floors\n• Leaning telephone poles/trees\n• Water breaking through ground\n• Rumbling sound increasing\n• Fences, walls tilting",
    
    "landslide_safety": "During a landslide: 🏃\n• Evacuate IMMEDIATELY if safe\n• Move to higher ground\n• Listen for unusual sounds\n• Stay alert and awake\n• If escape not possible, curl into a ball\n• Protect your head with hands",
    
    "landslide_after": "After landslide: 🔧\n• Stay away from slide area\n• Watch for flooding\n• Check for injured people\n• Report broken utilities\n• Listen for updates\n• Don't drive over debris\n• Help others if safe",
    
    # General safety
    "general_emergency": "General emergency steps: 🆘\n1. Stay calm and assess situation\n2. Call emergency services if needed\n3. Protect yourself first\n4. Help others if safe to do so\n5. Follow official instructions\n6. Keep communication devices charged\n7. Have emergency contacts ready",
    
    "emergency_numbers": "Emergency contacts: 📞\n• Police: 911 (USA) / 100 (India)\n• Fire: 911 / 101\n• Ambulance: 911 / 102\n• Disaster Management: 108\n• National Emergency: 112",
    
    "emergency_kit": "Basic emergency kit checklist: 🎒\n✓ Water (1 gallon/person/day for 3 days)\n✓ Food (non-perishable, 3-day supply)\n✓ Battery-powered radio\n✓ Flashlight and extra batteries\n✓ First aid kit\n✓ Whistle\n✓ Dust mask\n✓ Local maps\n✓ Cell phone with chargers\n✓ Prescription medications",
    
    "evacuation": "Evacuation tips: 🚗\n• Know multiple evacuation routes\n• Take emergency kit\n• Unplug appliances\n• Lock doors/windows\n• Inform family/friends\n• Follow official routes\n• Don't take shortcuts\n• Take pets with you",
    
    "preparation": "Disaster preparedness steps: 📋\n1. Create family emergency plan\n2. Build emergency kit\n3. Know community warning systems\n4. Learn first aid/CPR\n5. Identify safe places\n6. Practice drills\n7. Protect important documents\n8. Get insurance coverage",
    
    "shelter": "Finding shelter during disaster: 🏠\n• Go to designated evacuation centers\n• Stay with friends/family in safe areas\n• Community centers, schools (often shelters)\n• Churches, mosques, temples (may help)\n• Hotels in unaffected areas\n• Higher floors (for floods)\n• Lower floors (for tornadoes/hurricanes)",
    
    "first_aid": "Basic first aid for disasters: 🩺\n• CPR: 30 compressions, 2 breaths\n• Bleeding: Apply pressure with clean cloth\n• Burns: Cool with water (15-20 mins)\n• Fractures: Immobilize, don't move\n• Shock: Keep warm, elevate feet\n• Always call for professional help",
    
    "psychological": "Mental health after disaster: ❤️\n• Talk about your feelings\n• Spend time with family\n• Maintain normal routines\n• Limit news exposure\n• Get professional help if needed\n• Be patient with yourself\n• Help others in community",
    
    "children": "Helping children during disasters: 👶\n• Stay calm (children sense fear)\n• Explain simply what's happening\n• Keep them close\n• Maintain routines if possible\n• Reassure they're safe\n• Limit traumatic images\n• Let them express feelings",
    
    "pets": "Pet safety during disasters: 🐕\n• Take pets with you\n• Have pet emergency kit\n• Keep vaccinations updated\n• Microchip your pets\n• Know pet-friendly shelters\n• Never leave pets behind\n• Have carrier/leash ready",
    
    "pandemic": "During a pandemic/outbreak: 🦠\n• Follow health authority guidelines\n• Wear masks in public\n• Maintain social distance\n• Wash hands frequently\n• Stay home if sick\n• Get vaccinated when available\n• Clean surfaces regularly",
    
    "wildfire": "During wildfire: 🔥\n• Evacuate immediately when ordered\n• Keep windows/doors closed\n• Remove flammable items from yard\n• Use N95 mask for smoke\n• Stay low to ground if trapped\n• Look for clear areas (lakes, fields)\n• Cover yourself with wet blankets"
}

def get_disaster_type(user_message: str) -> str:
    """Detect what the user is asking about"""
    msg = user_message.lower()
    
    # Check for flood-related questions
    if any(word in msg for word in ['flood', 'water', 'river', 'rain', 'submerged', 'inundat']):
        if any(word in msg for word in ['why', 'cause', 'reason', 'happen']):
            return "flood_causes"
        elif any(word in msg for word in ['prevent', 'stop', 'control', 'avoid']):
            return "flood_prevention"
        elif any(word in msg for word in ['after', 'post', 'recover', 'clean']):
            return "flood_after"
        elif any(word in msg for word in ['kit', 'supply', 'prepare', 'emergency kit']):
            return "flood_kit"
        else:
            return "flood_safety"
    
    # Check for earthquake-related questions
    elif any(word in msg for word in ['earthquake', 'quake', 'tremor', 'seismic']):
        if any(word in msg for word in ['why', 'cause', 'reason', 'trigger']):
            return "earthquake_causes"
        elif any(word in msg for word in ['prepare', 'ready', 'preparation']):
            return "earthquake_prepare"
        elif any(word in msg for word in ['after', 'post', 'then']):
            return "earthquake_after"
        else:
            return "earthquake_safety"
    
    # Check for landslide-related questions
    elif any(word in msg for word in ['landslide', 'landslip', 'mudslide', 'debris', 'slope']):
        if any(word in msg for word in ['why', 'cause', 'reason', 'trigger']):
            return "landslide_causes"
        elif any(word in msg for word in ['sign', 'warning', 'indicator']):
            return "landslide_warning"
        elif any(word in msg for word in ['after', 'post']):
            return "landslide_after"
        else:
            return "landslide_safety"
    
    # Check for specific topics
    elif any(word in msg for word in ['emergency number', 'call', 'contact', 'phone']):
        return "emergency_numbers"
    
    elif any(word in msg for word in ['evacuation', 'evacuate', 'leave']):
        return "evacuation"
    
    elif any(word in msg for word in ['kit', 'supply', 'emergency kit', 'pack']):
        return "emergency_kit"
    
    elif any(word in msg for word in ['prepare', 'preparation', 'ready', 'plan']):
        return "preparation"
    
    elif any(word in msg for word in ['shelter', 'safe place', 'where to go']):
        return "shelter"
    
    elif any(word in msg for word in ['first aid', 'injury', 'wound', 'bleed']):
        return "first_aid"
    
    elif any(word in msg for word in ['mental', 'stress', 'anxiety', 'trauma', 'psychological']):
        return "psychological"
    
    elif any(word in msg for word in ['child', 'children', 'kid', 'young']):
        return "children"
    
    elif any(word in msg for word in ['pet', 'animal', 'dog', 'cat', 'puppy', 'kitten']):
        return "pets"
    
    elif any(word in msg for word in ['pandemic', 'virus', 'outbreak', 'disease', 'covid']):
        return "pandemic"
    
    elif any(word in msg for word in ['wildfire', 'forest fire', 'bushfire']):
        return "wildfire"
    
    # General questions
    elif any(word in msg for word in ['help', 'assist', 'support']):
        return "general_emergency"
    
    # Default
    else:
        return "general_emergency"

@router.post("/chat")
async def chat_with_assistant(message: ChatMessage):
    """
    AI Chat assistant for disaster response - gives different answers based on question
    """
    user_message = message.message.strip()
    
    if not user_message:
        return {
            "success": False,
            "response": "Please ask me a question about disaster safety!",
            "timestamp": datetime.now().isoformat()
        }
    
    # Detect what the user is asking about
    disaster_type = get_disaster_type(user_message)
    
    # Get the appropriate response
    response_text = DISASTER_RESPONSES.get(disaster_type, DISASTER_RESPONSES["general_emergency"])
    
    # Add a helpful greeting/intro for new conversations
    if len(user_message) < 10 or user_message.lower() in ["hi", "hello", "hey"]:
        response_text = "Hello! 👋 I'm your disaster response assistant. You can ask me about:\n\n• Floods 🌊\n• Earthquakes 🌍\n• Landslides ⛰️\n• Emergency kits 🎒\n• Evacuation 🚗\n• First aid 🩺\n• And much more!\n\nWhat would you like to know about?"
    
    # Add contextual follow-up suggestions
    suggestions = get_suggestions(disaster_type)
    
    return {
        "success": True,
        "response": response_text,
        "intent": disaster_type,
        "suggestions": suggestions,
        "timestamp": datetime.now().isoformat()
    }

def get_suggestions(intent: str) -> list:
    """Provide follow-up question suggestions"""
    suggestions_map = {
        "flood_safety": ["How to prevent floods?", "What to do after a flood?", "Flood emergency kit"],
        "flood_causes": ["How to stay safe during flood?", "Flood prevention tips", "After flood recovery"],
        "earthquake_safety": ["How to prepare for earthquake?", "What causes earthquakes?", "After earthquake safety"],
        "landslide_safety": ["Landslide warning signs?", "What causes landslides?", "After landslide safety"],
        "emergency_kit": ["What's in first aid kit?", "Food and water storage", "Essential documents"],
        "evacuation": ["Emergency kit checklist", "Family emergency plan", "Safe shelter locations"],
        "first_aid": ["CPR steps", "Treating burns", "Emergency kit items"]
    }
    
    return suggestions_map.get(intent, ["Flood safety tips", "Earthquake preparation", "Emergency kit checklist", "Evacuation planning"])

@router.get("/chat/health")
async def chat_health():
    """Check if chatbot service is healthy"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "topics_available": list(DISASTER_RESPONSES.keys()),
        "message": "Chatbot now gives different responses for different questions!"
    }