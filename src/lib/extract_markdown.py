import re

from lib.block_markdown import markdown_to_htmlnode


def extract_title(markdown: str) -> str:
    delimiter = r"^#\s(.*)"
    match = re.findall(delimiter, markdown)
    if not match:
        raise Exception("Invalid markdown: No h1 present.")
    if len(match) > 1:
        raise Exception("Invalid markdown: More than one h1 present.")
    return match[0].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"\nGenerating page from {from_path} to {dest_path} via {template_path}")

    f = open(from_path)
    file_contents = f.read()

    title = extract_title(file_contents)
    body = ""
    blocks = markdown_to_htmlnode(file_contents)
    for block in blocks:
        body += block.to_html()

    return title, body
