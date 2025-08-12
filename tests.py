from functions.run_python_file import run_python_file


def run_tests(working_directory, directory, content=None):
    if content is None:
        content = []
    if directory == ".":
        print(f"Result for current directory:")
    else:
        print(f"Result for '{directory}':")
    print (run_python_file(working_directory, directory, content))


run_tests("calculator", "main.py")
run_tests("calculator", "main.py", ["3 + 5"])
run_tests("calculator", "tests.py")
run_tests("calculator", "../main.py")
run_tests("calculator", "nonexistent.py")