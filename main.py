import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
    ]
)

if len(sys.argv) == 1:
    print("Error: No prompt provided")
    sys.exit(1)

prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

is_verbose = False

if "--verbose" in sys.argv:
    is_verbose = True

if response.function_calls:
    for function_call in response.function_calls:
        result = call_function(function_call, is_verbose)
        if result.parts[0].function_response.response:
            if is_verbose:
                print(f"-> {result.parts[0].function_response.response}")
        else:
            raise Exception("Fatal Error")
else:
    print(response.text)

# if "--verbose" in sys.argv:
#     print(f"User prompt: {prompt}\n")
#     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n")
#     print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

