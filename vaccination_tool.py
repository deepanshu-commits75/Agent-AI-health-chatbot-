import json
from langchain.tools import Tool

VACCINE_FILE_PATH = 'data/vaccination_schedule.json'

def get_vaccination_schedule(category: str) -> str:
    """Provides the vaccination schedule for a specific category (e.g., Infants, Pregnant Women)."""
    try:
        with open(VACCINE_FILE_PATH, 'r') as f:
            schedule_data = json.load(f)
    except FileNotFoundError:
        return f"Error: The vaccination schedule data file ({VACCINE_FILE_PATH}) is missing."

    schedule = schedule_data.get(category)
    if not schedule:
        return f"I do not have a vaccination schedule for the category '{category}'. Please try 'Infants' or 'Pregnant Women'."
    else:
        report = f"Here is the vaccination schedule for {category}:\n"
        for item in schedule:
            report += f"- Vaccine: {item.get('Vaccine', 'N/A')}, When: {item.get('When', 'N/A')}\n"
        return report

vaccination_tool = Tool(
    name="vaccination_schedule_tool",
    func=get_vaccination_schedule,
    description="""
    Use this for any questions related to vaccination schedules.
    It takes one argument: the category of the person, which must be one of ['Infants', 'Pregnant Women'].
    This tool returns a pre-formatted schedule. The agent's job is to present this to the user in a friendly way.
    """
)
