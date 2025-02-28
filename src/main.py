import sys, os, shutil
from recursivecopy import copy_from_static_to_public

def main():
    if len(sys.argv) < 3:
        print("usage: python3 main.py <source_path> <destination_path>")
        sys.exit(1)
    source = sys.argv[1]
    destination = sys.argv[2]
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

main()