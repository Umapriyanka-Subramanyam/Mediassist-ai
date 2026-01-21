import json
import os
import difflib
from typing import Dict, Any

# Load medicines data once
MEDICINES_DB = []
try:
    with open("backend/medicines.json", "r") as f:
        MEDICINES_DB = json.load(f)
except FileNotFoundError:
    # Fallback/Empty if file setup is wrong, but it should exist
    print("ERROR: backend/medicines.json not found.")

def get_medicine_info_from_llm(medicine_name: str, language: str) -> Dict[str, Any]:
    """
    Searches for medicine information in the local JSON database using fuzzy matching.
    Function name kept as 'get_medicine_info_from_llm' for compatibility with main.py,
    even though it no longer uses an LLM.
    """
    
    if not MEDICINES_DB:
        return {
            "medicine": medicine_name,
            "usage": "Database Error: medicines.json not found.",
            "dos_donts": "Please check backend setup.",
            "side_effects": "Unknown",
            "disclaimer": "System Error."
        }

    # Normalize input
    query = medicine_name.lower().strip()
    
    # Create a map of lower-case names to original data objects
    # and a list of names for matching
    name_map = {m["name"].lower(): m for m in MEDICINES_DB}
    all_names = list(name_map.keys())
    
    # 1. Exact Match
    if query in name_map:
        data = name_map[query]
        return _format_response(data, medicine_name)

    # 2. Fuzzy Match (find closest)
    # cutoff=0.6 means 60% similarity required
    matches = difflib.get_close_matches(query, all_names, n=1, cutoff=0.5)
    
    if matches:
        best_match_name = matches[0]
        data = name_map[best_match_name]
        return _format_response(data, best_match_name.title())
    
    # 3. No match found
    return {
        "medicine": medicine_name,
        "usage": "Medicine not found in our database.",
        "dos_donts": "We are constantly adding new medicines.",
        "side_effects": "Data unavailable.",
        "disclaimer": "Please consult a doctor or check the spelling."
    }

def _format_response(data: Dict[str, str], display_name: str) -> Dict[str, Any]:
    """Helper to format the successful response."""
    # We could eventually support language translation here if needed.
    # For now, we return the stored English data.
    return {
        "medicine": data["name"], # Use the official name from DB
        "usage": data["usage"],
        "dos_donts": data["dos_donts"],
        "side_effects": data["side_effects"],
        "disclaimer": data["disclaimer"]
    }
