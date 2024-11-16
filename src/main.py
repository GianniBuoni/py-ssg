import shutil
from os import path, mkdir
from lib.copy_static import copy_static
from lib.extract_markdown import generate_page

def main():
    # paths
    public = path.join("public")
    static = path.join("static")
    markdown = path.join("content", "index.md")
    template = path.join("content", "template.html")

    # delete public if already exists
    if path.exists(public):
        print("Deleting existing public directory.")
        shutil.rmtree(public)

    # make new puclic directory
    print("\nCreating new public directory.")
    mkdir(public)

    copy_static(static, public)
    generate_page(markdown, template, public)

if __name__ == "__main__":
    main()
