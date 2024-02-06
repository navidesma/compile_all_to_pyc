from os import path, name as os_name
from os.path import isdir, isfile, join
from os import listdir, remove, rename, replace
import re
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Convert all yo pyc')
parser.add_argument('-v', '--python_version', type=int, required=True, help='Enter the version of your python, 11 for python 3.11, 9 for python 3.9 and so on')
parser.add_argument('-p', '--path', type=str, required=True, help='Path to your python project, for example: /home/user/project/')
parser.add_argument('-r', '--remove', required=False, action="store_true", help='if you define this argument all of the .py files will be removed')

args = parser.parse_args()

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

python_version = args.python_version

cpython_version = cpython_version.replace("11", str(python_version))

final_path = args.path

remove_py = args.remove

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
                            
        if isfile(item_path) and cpython_version in item:
            new_name: str = str(item).replace(cpython_version, "")
            new_name_path = join(current_path, new_name)

            rename(item_path, new_name_path)

        if isdir(item_path) and not item in virtual_environment_names:
            move_pyc_file(item_path)


move_pyc_file(final_path)
