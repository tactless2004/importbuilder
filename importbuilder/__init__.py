'''
ImportBuilder searches for the locally installed modules associated with import statements.
Creating a pip compatible requirements.txt file.  
'''
import os
from importbuilder.importfinder import (
    find_py_files,
    find_py_dependencies,
    write_reqs,
    find_versions_and_pip_name,
    PythonFilesNotFound
)

__all__ = ['find']

def find(search_dir: str, requirements_file: str) -> None:
    '''
    Find python dependencies in a project and make a pip compatible.
    '''
    if not search_dir:
        search_dir = os.getcwd()

    try:
        pt_files = find_py_files(search_dir)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"{search_dir} cannot be found. If {search_dir} " +
             "is a relative path ensure you are in the correct directory"
        ) from e

    try:
        deps = find_py_dependencies(pt_files)
    except PythonFilesNotFound as e:
        raise PythonFilesNotFound(
            f"importbuilder was unable to locate any .py files in directory {search_dir}"
        ) from e

    requirements = find_versions_and_pip_name(deps)
    write_reqs(
        finished_imports = requirements,
        requirements_file =requirements_file
    )
