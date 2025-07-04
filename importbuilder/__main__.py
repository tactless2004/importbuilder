'''
importbuilder.__main__.py

__main__ method to make importbuilder callable in a `python -m module` manner.
'''
import os
import argparse
from importbuilder import find

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='ImportBuilder',
                    description='Builds a pip compatible requirements.txt file' +
                                'by finding imports in a python project and' +
                                'cross referencing with site-packages' 
    )
    parser.add_argument("-f", "--folder")
    parser.add_argument("-o", "--outputfile")
    args = parser.parse_args()

    root_dir = args.folder
    output_file = args.outputfile
    if not root_dir:
        root_dir = os.getcwd()
    if not output_file:
        output_file = "requirements.txt" #pylint: disable=invalid-name

    find(root_dir, output_file)
