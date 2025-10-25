import os
from os.path import abspath, exists, join
import shutil
from generate_page import extract_title, generate_page, generate_pages_recursive
def main():
    module_dir = os.path.dirname(__file__)
    project_root = abspath(join(module_dir, ".."))
    static_path = join(project_root, "static")
    public_path = join(project_root, "public")
    copy_directory_to_destination(static_path, public_path)
    
    content_path = join(project_root, "content")
    md_path = join(content_path, "index.md")
    t_path = join(project_root, "template.html")
    destination = join(public_path, "index.html")
    #generate_page(md_path, t_path, destination)
    
    generate_pages_recursive(content_path, t_path, public_path)

    
def copy_directory_to_destination(static_path, public_path):
    if exists(public_path):
        shutil.rmtree(public_path)
        os.mkdir(public_path)
    elif not exists(public_path) and os.path.isdir(static_path):
        os.mkdir(public_path)
    ls = os.listdir(static_path)

    for item in ls:
        new_path = abspath(join(static_path, item))
        new_destination = abspath(join(public_path, item))
        if os.path.isfile(new_path):
            shutil.copy(new_path, new_destination)
        if os.path.isdir(new_path):
            os.mkdir(new_destination)
            copy_directory_to_destination(new_path, new_destination)

if __name__ == "__main__":
    main()
