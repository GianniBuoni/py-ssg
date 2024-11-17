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

    page_content = generate_page_content(from_path)
    html = replace_template_html(page_content, template_path)
    write_html(html, dest_path)

def generate_page_content(from_path) -> tuple[str, str]:
    f = open(from_path)
    file_contents = f.read()
    f.close()

    title = extract_title(file_contents)
    body = ""
    blocks = markdown_to_htmlnode(file_contents)
    for block in blocks:
        body += block.to_html()

    return title, body

def replace_template_html(html: tuple[str, str], template_path: str) -> str:
    f = open(template_path)
    file_contents = f.read()
    f.close()
    
    file_contents = file_contents.replace("{{ Title }}", html[0])
    file_contents = file_contents.replace("{{ Content }}", html[1])

    return file_contents

def write_html(html: str, dest_path: str) -> None:
    file_path = dest_path + "/index.html"
    
    with open(file_path, "w") as file:
        file.write(html)

    print(f"\nWrote: {file_path}")
