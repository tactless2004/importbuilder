import os
import sys
import pip

def find_py_files(root_dir: str) -> list:
    pt_files = []
    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            if file.split(".")[1] == "py":
                pt_files.append(os.path.join(dirpath, file))
    return pt_files

def find_py_dependencies(pt_files: list) -> list:
    imports = []
    if not pt_files:
        raise PythonFilesNotFound("importfinder was unable to locate any Python files")
    for pt_file in pt_files:
        try:
            with open(pt_file, "r", encoding = "utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    # Remove white space
                    line = line.strip("")
                    if len(line) > 7 and line[0:7] == "import ":
                        imp = line.split(" ")[1]
                        imports.append(imp)

        except FileNotFoundError:
            print(f"{pt_file} was located by os.walk(), but could not be opened by the import searcher")

class PythonFilesNotFound(Exception):
    pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        root_dir = os.getcwd()
    elif len(sys.argv) >= 2:
        root_dir = sys.argv[1]

    pt_files = find_py_files(root_dir)
    find_py_dependencies(pt_files)
    