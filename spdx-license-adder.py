import os
import argparse

# Function to determine the programming language based on the file extension
def get_language(file_path):
    language_extensions = {
        '.py': 'Python',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.go': 'Go',
        '.p4': 'P4'
    }

    _, ext = os.path.splitext(file_path)
    return language_extensions.get(ext, 'Unknown')

def modify_file(file_path, license_identifier):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()

        language = get_language(file_path)
        comment_prefix = ""

        if language == "Python":
            comment_prefix = "#"
        elif language in ["P4", "C++", "C", "Java", "Go"]:
            comment_prefix = "//"

        spdx_line = f"SPDX-License-Identifier: {license_identifier}"

        content.insert(0, comment_prefix + " " + spdx_line + "\n")

        with open(file_path, 'w') as file:
            file.writelines(content)

        print(f"Comment added to the beginning of {file_path}")
    except Exception as e:
        print(f"Error while modifying {file_path}: {e}")


def read_paths_from_file(file_name):
    try:
        with open(file_name, 'r') as f:
            paths = [line.strip() for line in f.readlines() if line.strip()]
        return paths
    except Exception as e:
        print(f"Error reading from {file_name}: {e}")
        return []


def main():

    parser = argparse.ArgumentParser(description="SPDX License Adder: Add an SPDX license header to the beginning of source code files.")

    parser.add_argument('file_paths', nargs='*', help="List of file paths to modify (space separated)")
    parser.add_argument('--file', help="A file containing paths to modify (one per line)")
    parser.add_argument('--license', required=True, help="The SPDX license identifier to add (e.g., MIT, Apache-2.0)")

    args = parser.parse_args()

    if args.file and args.file_paths:
        print("Error: Please provide either a file with paths (--file) or explicit file paths, but not both.")
        return

    file_paths = args.file_paths

    if args.file:
        file_paths.extend(read_paths_from_file(args.file))

    if not file_paths:
        print("Error: No file paths provided. Please specify file paths directly or in a file.")
        return

    for file_path in file_paths:
        if os.path.exists(file_path):
            modify_file(file_path, args.license)
        else:
            print(f"File {file_path} does not exist.")

if __name__ == '__main__':
    main()
