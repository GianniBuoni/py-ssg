import shutil
from os import path, mkdir, listdir

def copy_static(src: str, dest: str):
    if not path.exists(dest):
        mkdir(dest)

    for filename in listdir(src):
        from_path = path.join(src, filename)
        to_path = path.join(dest, filename)
        print(f"- Copying {from_path} {to_path}")

        if path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_static(from_path, to_path)
