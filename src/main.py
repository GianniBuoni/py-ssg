import shutil
from os import path, mkdir
from lib.copy_static import copy_static

def main():
    public = path.join("public")
    static = path.join("static")

    # delete public if already exists
    if path.exists(public):
        print("Deleting existing public directory.")
        shutil.rmtree(public)

    # make new puclic directory
    print("Creating new public directory.")
    mkdir(public)

    copy_static(static, public)

if __name__ == "__main__":
    main()
