import os
import sys
import pip

def find_py_files(root_dir: str) -> list:
    '''
    Use os.walk() to locate files in a directory and subdirectories thereof with the extension .py
    '''
    pt_files = []
    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            split = os.path.splitext(file)
            if split[1] == "py":
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
                        imports.append(imp.strip())

        except FileNotFoundError:
            print(
                f"{pt_file} was located by os.walk()," +
                " but could not be opened by the import searcher"
            )
    return list(set(imports))

class PythonFilesNotFound(Exception):
    '''
    PythonFilesNotFound is raised when a directory does not contain any .py files.
    '''

if __name__ == "__main__":
    search_dir = os.getcwd()
    if len(sys.argv) >= 2:
        search_dir = sys.argv[1]

    pt_files = find_py_files(search_dir)
    try:
        deps = find_py_dependencies(pt_files)
    except PythonFilesNotFound as e:
        raise PythonFilesNotFound(
            f"importbuilder was unable to locate any .py files in directory {search_dir}"
        ) from e

    print(deps)
