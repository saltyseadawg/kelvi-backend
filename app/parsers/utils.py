from pathlib import Path
import shutil
import re


def remove_trailing_brackets(text: str) -> str:
    """Used ChatGPT"""
    pattern = r"(?:\s*\([^)]*\))*\s*$"
    processed = re.sub(pattern, "", text)
    return processed


def list_files(folder_path: str) -> tuple:
    return tuple(str(x) for x in Path(folder_path).iterdir() if x.is_file())


def combine_files(folder_path: str, out_file: str):
    filenames = list_files(folder_path)
    with open(out_file, "wb") as outfile:
        for filename in filenames:
            with open(filename, "rb") as infile:
                shutil.copyfileobj(infile, outfile)
