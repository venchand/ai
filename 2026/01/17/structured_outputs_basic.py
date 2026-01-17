import os

import azure.identity
import openai
import rich
from dotenv import load_dotenv
from pydantic import BaseModel

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

client = openai.OpenAI(base_url="https://models.github.ai/inference", api_key=os.environ["GITHUB_TOKEN"])
MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o-mini")

class CalendarEvent(BaseModel):
    name: str
    description: str
    date: str
    participants: list[str]
    invitee: str
    guest: str

completion = client.beta.chat.completions.parse(
    model=MODEL_NAME,
    messages = [
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Ramesh and Suresh are going to meet over dinner on 16th of August 2024."}
    ],
    response_format=CalendarEvent,
)

message = completion.choices[0].message
if message.refusal:
    rich.print(message.refusal)
else:
    event = message.parsed
    rich.print(event)
