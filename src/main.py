import shutil
from os import path, mkdir
from lib.copy_static import copy_static, generate_pages_recursive

def main():
    # paths
    public = path.join("public")
    static = path.join("static")
    content = path.join("content")
    template = path.join("content", "template.html")

    # delete public if already exists
    if path.exists(public):
        print("Deleting existing public directory.")
        shutil.rmtree(public)

    # make new puclic directory
    print("\nCreating new public directory.")
    mkdir(public)
    copy_static(static, public)

    print("\nGenerating pages.")
    generate_pages_recursive(content, template, public)

if __name__ == "__main__":
    main()
