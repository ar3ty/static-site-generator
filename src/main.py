import sys, os, shutil
from fillespages import copy_from_static_to_public, generate_pages_recursively

def main():
    source = "./static"
    destination = "./public"
    dir_path_content = "./content"
    template_path = "./template.html"
    try:
        if os.path.exists(destination):
            shutil.rmtree(destination)
        os.mkdir(destination)
        print("Deleting contents of public directory...")
    except PermissionError:
        print("Cannot make/delete folder. Check permissions")
        sys.exit(1)
    if not os.path.exists(source):
        raise Exception("Source folder does not exist")
    print("Copying contents of static files to public directory:")
    copy_from_static_to_public(source, destination)
    generate_pages_recursively(dir_path_content, template_path, destination)

main()