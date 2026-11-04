import os
import shutil
from generate_page import generate_pages_recursive

def copy_content(source_dir: str, dest_dir:str)->None:

    if not os.path.exists(source_dir):
        raise ValueError("Origin directory doesn`t exist")
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    sub_dir = os.listdir(source_dir)
    for dir in sub_dir:
        sub_dir_path = os.path.join(source_dir, dir)
        sub_dir_dest = os.path.join(dest_dir, dir)
        if os.path.isfile(sub_dir_path):
            shutil.copy(sub_dir_path, sub_dir_dest)
            print(f"Copied: {sub_dir_path} -> {sub_dir_dest}")
        else:
             copy_content(sub_dir_path, sub_dir_dest)

    


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_content("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
