import os, shutil, sys
from block import markdown_to_html_node


# yes, i wasted hour of my time just to visualize
# graph tree instead of task completion 

def copy_from_static_to_public(source, destination, graph="╠═══"):
    contents = os.listdir(source)
    if len(contents) == 0:
        return 
    for item in contents:
        if item == contents[-1]:
            tree_graph = graph[:-4] + "    " + graph[-4:]
            graph = graph[:-4] + "╚" + graph[-3:]
        else:
            tree_graph = graph[:-4] + "║   " + graph[-4:]
        current_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(destination, item)
        if os.path.isfile(current_item_path):
            shutil.copy(current_item_path, destination_item_path)
            print(f"{graph}Source file: {current_item_path} was copied to: {destination_item_path}")
        else:
            os.mkdir(destination_item_path)
            print(f"{graph}Source directory: {current_item_path} was copied to: {destination_item_path}")
            copy_from_static_to_public(current_item_path, destination_item_path, tree_graph)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no title is found in the text")

def write_to_dest_path(dest_path, page):
    pathdir = os.path.dirname(dest_path)
    if not os.path.exists(pathdir):
        try:
            os.makedirs(pathdir)
        except PermissionError:
            print("Cannot make/delete folder. Check permissions")
            sys.exit(1)
    with open(dest_path, "w") as f:
        f.write(page)
         

def generate_page(path_from, template_path, dest_path):
    print(f"Generating page from {path_from} to {dest_path} using {template_path}")
    with open(path_from) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)
    write_to_dest_path(dest_path, page)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    if len(contents) == 0:
        return 
    for item in contents:
        current_item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(current_item_path) and current_item_path.endswith(".md"):
            filename = os.path.splitext(item)[0] + ".html"
            to_file = os.path.join(dest_dir_path, filename)
            generate_page(current_item_path, template_path, to_file)
        elif os.path.isdir(current_item_path):
            destination_item_path = os.path.join(dest_dir_path, item)
            if not os.path.exists(destination_item_path):
                os.mkdir(destination_item_path)
            print(f"Source directory: {current_item_path} was replicated in: {destination_item_path}")
            generate_pages_recursively(current_item_path, template_path, destination_item_path)
