import os
import argparse
from macho_parser import MachoParser


def parse_file(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError("The provided file does not exist")
    
    parser = MachoParser(file_path)
    parser.decrypt_strings()


def parse_directory(dir_path: str):
    if not os.path.isdir(dir_path):
        raise FileNotFoundError("The provided directory does not exist")
    
    for file in os.listdir(dir_path):
        full_file_path = os.path.join(dir_path, file)
        print(f"----- File: {file} -----")
        parser = MachoParser(full_file_path)
        parser.decrypt_strings()


def init_args_setup():
    parser = argparse.ArgumentParser(description='GO Deobfuscator')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type = str, help = 'File path')
    group.add_argument('--dir', type = str, help = 'Directory path')

    return parser.parse_args()


def main():
    args = init_args_setup()
    
    if args.file:
        parse_file(args.file)
    elif args.dir:
        parse_directory(args.dir)
    else:
        raise Exception("You can either provide a single file or a directory containing multiple files")
    

if __name__ == "__main__":
    main()
