'''
importbuilder.importfinder.py

Utilities for finding python dependencies.
'''
import os
import importlib
import tomllib

def find_py_files(root_dir: str) -> list:
    '''
    Use os.walk() to locate files in a directory and subdirectories thereof with the extension .py

    :param root_dir: Directory to search for .py files
    '''
    pt_files = []
    if not os.path.isdir(root_dir):
        raise FileNotFoundError(f"{root_dir} could not be located...")

    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            split = os.path.splitext(file)
            if split[1] == ".py":
                pt_files.append(os.path.join(dirpath, file))
    return pt_files

def find_py_dependencies(pt_files: list) -> list:
    '''
    Search through a list of .py files, opening the files and finding imports.

    :param pt_files: List of python file paths in which to search for import statements
    '''
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

def find_versions_and_pip_name(imports: list) -> list:
    '''
    Search site-packages for pyproject files to determine pip version and install.

    :param imports: List of potentially importable python packages
    '''
    finished_imports = []
    for imp in imports:
        try:
            namespace = importlib.import_module(imp)
        except ModuleNotFoundError:
            print(
                f"{imp} is not installed in your environment.\n" +
                "If you are building a requirements.txt file for a project " +
                "you do not already have the dependencies for" +
                "try pipreqs"
            )
            return []

        try:
            version = namespace.__version__
        # std. library packages do not have __version__
        except AttributeError:
            continue

        # Force install_location to be a string incase it doesn't exist
        # (although this should never happen)
        install_location = str(namespace.__file__)

        # If the __file__ is not a reference to an __init__.py file,
        # then it is likely a std. library package.
        # Or the package is legacy. In either case, assume there is no pyproject.toml.
        if os.path.basename(install_location) == f"{imp}.py":
            finished_imports.append(f"{imp}=={version}")
            continue
        try:
            with open(
                    file = os.path.join(os.path.dirname(install_location), "pyproject.toml"),
                    mode ="rb"
            ) as f:
                pyprojecttoml = tomllib.load(f)

        # If we don't find a pyproject.toml, assume pip name = import name
        except FileNotFoundError:
            finished_imports.append(f"{imp}=={version}")
            continue

        try:
            imp = pyprojecttoml['project']['name']
        except KeyError:
            print(pyprojecttoml['project'])
            print(f"{imp} does not have a project name in the pyproject.toml file.\nContinuing...")
            continue

        finished_imports.append(f"{imp}=={version}")

    return finished_imports

def write_reqs(finished_imports: list, requirements_file = "requirements.txt") -> None:
    '''
    Create a pip compatible requirements.txt file
    '''
    with open(requirements_file, "w+", encoding = "utf-8") as f:
        for line in finished_imports:
            f.write(f"{line}\n")

class PythonFilesNotFound(Exception):
    '''
    PythonFilesNotFound is raised when a directory does not contain any .py files.
    '''
