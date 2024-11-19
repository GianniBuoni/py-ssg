import shutil
from os import path, mkdir, listdir

from lib.extract_markdown import generate_page

def copy_static(src: str, dest: str):
    if not path.exists(dest):
        mkdir(dest)

    for filename in listdir(src):
        from_path = path.join(src, filename)
        to_path = path.join(dest, filename)
        print(f"- Copying {from_path} to {to_path}")

        if path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_static(from_path, to_path)

def generate_pages_recursive(src: str, template_path: str, dest:str):
    print(template_path)
    if not path.exists(dest):
        mkdir(dest)

    for filename in listdir(src):
        from_path = path.join(src, filename)
        to_path = path.join(dest, filename)

        if from_path == template_path:
            continue
        elif path.isfile(from_path):
            generate_page(from_path, template_path, dest)
        else: generate_pages_recursive(from_path, template_path, to_path)
