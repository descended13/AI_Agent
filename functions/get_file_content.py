import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the file up to a maximum of 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Specifies what directory to search from the current directory which may contain the file to be read",
            },  "file_path": {
                    "type": "string",
                    "description": "Specifies what file to read which would be contained in the working_directory",
            },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_path:
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_dir):
            return (f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_dir) as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except:
        return("Error: Iunno what to put here")
        