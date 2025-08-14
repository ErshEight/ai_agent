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

args = []
for arg in sys.argv[1:]:
    if not arg.startswith("--"):
        args.append(arg)

prompt = " ".join(args)
is_verbose = "--verbose" in sys.argv

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]
for i in range(20):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if not response.function_calls and response.text:
            print(f"Final response:\n{response.text}")
            break
        elif i == 19:
            print(f"Maximum iterations reached.")
            break

        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                result = call_function(function_call, is_verbose)
                if result.parts[0].function_response.response:
                    if is_verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                else:
                    raise Exception("Fatal Error")
                function_responses.append(result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))
                
        continue

    except Exception as e:
        print(f"Error: {str(e)}")
        break
