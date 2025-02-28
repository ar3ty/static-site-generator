import os, shutil

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