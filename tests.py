from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file


def run_tests(working_directory, directory, content):
    if directory == ".":
        print(f"Result for current directory:")
    else:
        print(f"Result for '{directory}':")
    # print (get_files_info(working_directory, directory))
    print (write_file(working_directory, directory, content))


run_tests("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
run_tests("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
run_tests("calculator", "/tmp/temp.txt", "this should not be allowed")