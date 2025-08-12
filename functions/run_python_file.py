import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_dir.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_dir):
            return f'Error: File "{file_path}" not found.'
        if not target_dir.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        command = ["python", file_path] + args

        result = subprocess.run(command, timeout=30, capture_output=True, text=True, cwd=working_directory)

        if result.stdout.strip() == "" and result.stderr.strip() == "":
            return "No output produced."
        
        output = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
        
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)