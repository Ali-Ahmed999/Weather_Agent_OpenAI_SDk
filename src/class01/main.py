from agents.tool import function_tool
from agents import Agent,Runner
import asyncio
from connection import config,model
import requests
from dotenv import load_dotenv
import os



load_dotenv()

@function_tool("get_weather_info")
def get_weather(location: str) -> str:
    """
    Get the weather for a given location using Visual Crossing Weather API.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        raise ValueError("WEATHER_API_KEY is not set. Please ensure it is defined in your .env file.")
    
    WEATHER_API_KEY = api_key
    
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"    
    params = {
        "key": WEATHER_API_KEY,
        "unitGroup": "metric",  
        "contentType": "json"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        current_conditions = data.get("currentConditions", {})
        temperature = current_conditions.get("temp", "N/A")
        description = current_conditions.get("conditions", "No description available")
        return f"The weather in {location} is {description} with a temperature of {temperature}°C."
    else:
        return f"Could not retrieve weather data for {location}. Please check the location name."


weather_Agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You can answer questions about the weather.",
    model=model,
    tools=[get_weather],
)


async def main():
    try:        
        result = await Runner.run(weather_Agent, input="What is the weather like in Karachi?")
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")
        
    
asyncio.run(main())
