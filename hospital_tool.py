import json
from typing import Optional
from langchain.tools import Tool

# It's assumed your 'data' folder is in the same root directory as app.py
# If running this file directly, the path might need adjustment.
METADATA_FILE_PATH = 'data/hospital_directory/hospital_directory_metadata.json'

try:
    with open(METADATA_FILE_PATH, 'r') as f:
        hospital_metadata = json.load(f)
except FileNotFoundError:
    print(f"WARNING: Metadata file not found at {METADATA_FILE_PATH}. The hospital tool will not work.")
    hospital_metadata = {}

def find_hospitals(state: str, pincode: Optional[str] = None) -> str:
    """Finds hospitals in a state, with an optional pincode filter."""
    file_path = hospital_metadata.get(state)
    if not file_path:
        return f"Sorry, I do not have hospital information for the state: {state}."
    
    try:
        with open(file_path, 'r') as f:
            loaded_json = json.load(f)
        
        if isinstance(loaded_json, dict):
            data = loaded_json.get("hospitals", [])
        elif isinstance(loaded_json, list):
            data = loaded_json
        else:
            return "Error: Unsupported JSON format in the data file."
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return f"Error reading hospital data file for {state}: {e}"
    
    if pincode:
        # Ensure we are using "Pincode" with a capital P to match the JSON data.
        filtered_hospitals = [h for h in data if str(h.get("Pincode", "")) == str(pincode)]
        
        if not filtered_hospitals:
            return f"No hospitals found in {state} with the pincode {pincode}."
        else:
            return json.dumps(filtered_hospitals, indent=2)
    else:
        hospital_count = len(data)
        return (f"I found {hospital_count} hospitals in {state}. "
                "For a more specific list, please provide a pincode.")

def hospital_tool_wrapper(query) -> str:
    """
    Wrapper that robustly handles dict or string input for the find_hospitals function.
    """
    if isinstance(query, str):
        try:
            query_dict = json.loads(query)
        except json.JSONDecodeError:
            query_dict = {"state": query}
    elif isinstance(query, dict):
        query_dict = query
    else:
        return "Error: Invalid input format for the hospital tool."

    return find_hospitals(state=query_dict.get("state"), pincode=query_dict.get("pincode"))

hospital_tool = Tool(
    name="hospital_directory_tool",
    func=hospital_tool_wrapper,
    description="""
    Use this tool to find hospitals in a specific Indian state. The input can be a dictionary OR a plain string for the state name.
    For multi-argument searches, the input MUST be a dictionary with a "state" key and an optional "pincode" key.
    Example: {"state": "Uttar Pradesh", "pincode": "208001"}.
    If the tool's output asks for a pincode, you MUST ask the user for it.
    """
)
