import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(working_directory, directory))

        if not target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        files = os.listdir(target_dir)
        files_info = []

        for file in files:
            file_path = os.path.join(target_dir, file)
            file_info = f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
            files_info.append(file_info)
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: {str(e)}"
