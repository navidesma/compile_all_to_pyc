from os import path, name as os_name
from os.path import isdir, isfile, join
from os import listdir, remove, rename, replace
import re
import subprocess

python_file_regex = re.compile("^.*\.py$")

virtual_environment_names = [
    ".env",
    ".venv",
    "env",
    "venv",
    "ENV",
    "env.bak",
    "venv.bak",
]

base_dir = "."


cpython_version = ".cpython-311"

python_version = input(
    "\nEnter your python version, 9 for python 3.9, 10 for python 3.10 and so on, or just press Enter, the default is python 3.11.\nYour python version or just press Enter: "
)

if python_version != "":
    if not python_version.isdigit():
        print("\nEnter a valid python version or leave empty")
        raise Exception("\nEnter a valid python version or leave empty")

    cpython_version.replace("11", python_version)


relative_or_absolute = input(
    "\nI'm going to ask you for your project path, will it be relative to this directory or absolute?\nEnter R for relative or A for absolute R/A: "
)

if relative_or_absolute != "R" and relative_or_absolute != "A":
    raise Exception("\nEnter R or A")

entered_path = input(
    "\nEnter your relative or absolute path based on your previous answer,\nYOU ARE DOING THIS BY YOUR OWN RISK, so please enter the correct path for your python project directory:\n"
)

final_path = (
    entered_path if relative_or_absolute == "A" else join(base_dir, entered_path)
)

remove_py_or_not_input = input(
    "\nDo you want your .py files to be removed?\npress Y if you want to remove your .py files or N if you want to keep them Y/N: "
)

if remove_py_or_not_input != "Y" and remove_py_or_not_input != "N":
    raise Exception("Enter Y or N")

remove_py = remove_py_or_not_input == "Y"

is_windows = os_name == "nt"

command = subprocess.Popen(
        cwd=final_path,
        args=f"python{'' if is_windows else '3'} -m compileall .",
        stdout=subprocess.PIPE,
        shell=True,
    )

(output, err) = command.communicate()

p_status = command.wait()

if p_status != 0:
    raise Exception("\nsomething went wrong when generating pyc files")


def move_pyc_file(current_path: path):
    for item in listdir(current_path):
        item_path = join(current_path, item)
        if isdir(item_path) and item == "__pycache__":
            for compiled_file in listdir(item_path):
                compiled_file_path = join(item_path, compiled_file)

                new_name: str = str(compiled_file).replace(cpython_version, "")
                new_name_path = join(item_path, new_name)

                rename(compiled_file_path, new_name_path)

                previous_dir_path = join(item_path, "..")
                replace(new_name_path, join(previous_dir_path, new_name))

                if remove_py:
                    for item_to_be_removed in listdir(previous_dir_path):
                        if isfile(
                            join(previous_dir_path, item_to_be_removed)
                        ) and re.fullmatch(python_file_regex, item_to_be_removed):
                            remove(join(previous_dir_path, item_to_be_removed))

        if isdir(item_path) and not item in virtual_environment_names:
            move_pyc_file(item_path)


move_pyc_file(final_path)
