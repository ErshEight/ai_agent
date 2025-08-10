import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) == 1:
    print("Error: No prompt provided")
    sys.exit(1)

prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)

print(response.text)

if "--verbose" in sys.argv:
    print(f"User prompt: {prompt}\n")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

