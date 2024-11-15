import re


def extract_title(markdown: str) -> str:
    delimiter = r"^#\s(.*)"
    match = re.findall(delimiter, markdown)
    if not match:
        raise Exception("Invalid markdown: No h1 present.")
    if len(match) > 1:
        raise Exception("Invalid markdown: More than one h1 present.")
    return match[0].strip()
