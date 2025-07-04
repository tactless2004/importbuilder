'''
__main__.py method for importbuilder.
'''
import argparse
from importbuilder import find
import os

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
        output_file = "requirements.txt"

    find(root_dir, output_file)