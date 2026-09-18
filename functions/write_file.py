import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Allows the writing to specific files if allowed",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Specifies what directory to write the file to from the current directory",
                },
                        "file_path": {
                            "type": "string",
                            "description": "Specifies what file to write to which would be contained in the working_directory",
                        },
                                "content": {
                                    "type": "string",
                                    "description": "The content of the information that will be written",
                                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_path):
            return(f'Error: "{file_path}" is not a directory')

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
    