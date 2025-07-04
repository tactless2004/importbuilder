'''
__main__.py method for importbuilder.
'''
import sys
import os
from importbuilder.importfinder import (
    find_py_files,
    find_py_dependencies,
    find_versions_and_pip_name,
    write_reqs,
    PythonFilesNotFound
)

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

    requirements = find_versions_and_pip_name(deps)
    write_reqs(requirements)
