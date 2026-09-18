import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python files from a given working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Specifies what directory to search from the current directory which may contain the file to be ran",
                },
                "file_path": {
                    "type": "string",
                    "description": "Specifies what .py file to run which would be contained in the working_directory",
                },
                "args": {
                    "type": "string",
                    "description": "Any arguments for the running of the file",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    if not valid_target_path:
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(target_path):
        return(f'Error: "{file_path}" does not exist or is not a regular file')
    if not file_path.endswith('py'):
        return(f'Error: "{file_path}" is not a Python file')

    command = ["python", target_path]
    if args:
        command.extend(args)

    result_output = []
    result = subprocess.run(
        command,capture_output=True,text=True,timeout=30,check=True)

    if result.returncode != 0:
        result_output.append(f"Process exited with code {result.returncode}")
    stdout_content = result.stdout.strip() if result.stdout else "None"
    stderr_content = result.stderr.strip() if result.stderr else "None"

    result_output.append(f"STDOUT: {stdout_content}")
    result_output.append(f"STDERR: {stderr_content}")
    return(result_output)