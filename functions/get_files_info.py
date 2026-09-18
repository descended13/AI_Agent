import os
from pathlib import Path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Do not use if request asks to use run_python_file, it does not run files, Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        print(f"Result for {directory} directory")
        if not valid_target_dir:
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            return(f'Error: "{directory}" is not a directory')
        else:
            returned_data = ""
            for item in Path(target_dir).iterdir():
                returned_data += (
                    "- "+str(item.name)+": file_size="+str(os.path.getsize(item))+
                    " bytes, is_dir="+str(os.path.isdir(item))+"\n"
                )
            return returned_data
    except:
        raise Exception("Error: The directories given do not work")


# def test(target_dir):
#     p = Path(target_dir)
#     returned_data = ""
#     for item in Path(target_dir).iterdir():
#         returned_data += (
#             "- "+str(item.name)+": file_size="+str(os.path.getsize(item))+
#             " bytes, is_dir="+str(os.path.isdir(item))+"\n"
#         )
#     return returned_data

# print(test("/home/des/workspace/bootdev/AI_Agent/calculator"))