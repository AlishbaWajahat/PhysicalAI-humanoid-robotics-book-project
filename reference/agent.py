import os
import dotenv
from agents import Agent,Runner,function_tool,set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import asyncio
import requests


set_tracing_disabled(disabled=True)
dotenv.load_dotenv()
os.environ['GEMINI_API_KEY']=os.getenv('GEMINI_API_KEY')
model='gemini/gemini-2.0-flash'

@function_tool
def get_user_data(min_age:int)->list[dict]:
    'Retrieve user data based on minimum age'
    users = [
        {"name": "Muneeb", "age": 22},
        {"name": "Muhammad Ubaid Hussain", "age": 25},
        {"name": "Azan", "age": 19},

    ]
    return [user for user in users if user['age'] >= min_age]
    


@function_tool
def send_whatsapp(contact: str, message: str) -> str:
    instance_id = "instance133066"
    token = "uldzah8l1xnwzz9q"
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    payload = {
        "token": token,
        "to": contact,
        "body": message
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print('✅ Message sent via UlrtaMSG!')
        return "✅ Message sent via UlrtaMSG!"
    else:
        return f"❌ Failed: {response.text}"
    
    


Match_finder=Agent(
    name='Auntie',
    model=LitellmModel(model=model),
    instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches,Use the get_user_data tool to find users of minimum age 20 then use browser_search tools to fetch their details from linkedIn. Then format their details (name and age and profession) into a message and send it to +923311347822 using the send_whatsapp tool.",
    tools=[get_user_data,send_whatsapp])