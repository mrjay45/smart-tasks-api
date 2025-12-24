# Category (based on keywords):
from datetime import datetime, timedelta
import re

# Category classification [text is converted into lower case]
def category_classification(text: str) -> str:
    CATEGORY_KEYWORDS = {
        "scheduling": ['meeting', 'schedule', 'call', 'appointment', 'deadline'],
        "finance": ['payment', 'invoice', 'bill', 'budget', 'cost', 'expense'],
        "technical": ['bug', 'fix', 'error', 'install', 'repair', 'maintain'],
        "safety": ['safety', 'hazard', 'inspection', 'compliance', 'PPE']
    }
    # convert the text into lower case
    text = text.lower()
    
    # loop the dict and match the keywords to text
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
            
    return "general"


# Priority Detection [text is converted into lower case]
def priority_detection(text: str) -> str:
    PRIORITY_KEYWORDS = {
        "high": ['urgent', 'asap', 'immediately', 'today', 'critical', 'emergency'],
        "medium": ['soon', 'this week', 'important'],
    }
    text = text.lower()
    
    for key, values in PRIORITY_KEYWORDS.items():
        for value in values:
            if value in text:
                return key
            
    return "low"


# Entity Extraction [text is converted into lower case]
def entity_extraction(text: str) -> dict:
    entities = {}
    
    #? Date matching
    if "today" in text.lower():
        entities['date'] = datetime.now().date().isoformat()
    
    elif "tomorrow" in text.lower():
        entities['date'] = (datetime.now() + timedelta(days=1)).date().isoformat()
        
    elif "week" in text.lower():
        entities['date'] = "week"
    
    elif "year" in text.lower():
        entities['date'] = "year"

    # date matching like 21-12-2025 or 21/12/2025
    date_match = re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", text) 
    if date_match:
        entities['date'] = date_match.group(1)
        
    #? Time matching
    # 5pm, 02:15pm, 5 pm, 02:15 pm or am
    
    time_match = re.search(r"(\d{1,2}(:\d{1,2})?\s?(am|pm))", text, re.IGNORECASE)
    if time_match:
        entities['time'] = time_match.group(1)
        
    #? name matching (after "with", "by", "assign to")
    name_match = re.search(r"\s+(with|by|assign to)\s+([A-Za-z]+)", text, re.IGNORECASE)
    if name_match:
        entities['person'] = name_match.group(2)
        
    #? location matching
    location_matching = re.search(r"\s+(at|in)\s+(\w+)", text, re.IGNORECASE)
    if location_matching:
        entities['location'] = location_matching.group(2)
        
    #? ACtion verb matching
    ACTION_VERBS = ["schedule", "fix", "pay", "inspect", "call", "meet", "install", "repair", "review", "submit", "approve", "update", "notify", "follow-up","report"]
    for verb in ACTION_VERBS:
        if verb in text.lower():
            entities['action'] = verb
            break
        
    return entities
        

# Suggested actions based on category
def suggested_action(category: str) -> list:
    SUGGESTED_ACTIONS = {
        "scheduling": ["Block calendar", "Send invite", "Prepare agenda", "Set reminder"],
        "finance": ["Check budget", "Get approval", "Generate invoice", "Update records"],
        "technical": ["Diagnose issue", "Check resources", "Assign technician","Document fix"],
        "safety": ["Conduct inspection", "File report", "Notify supervisor","Update checklist"]
    }
    
    return SUGGESTED_ACTIONS.get(category, [])
        
        