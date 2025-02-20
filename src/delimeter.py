from textnode import *

def split_nodes_delimeter(old_nodes, delimiter, text_type):
    node_result = []
    for node in old_nodes:
        node_parts = []
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            node_result.append(node)
        else:
            node_segments = node.text.split(delimiter)
            length = len(node_segments)
            if length % 2 == 0:
                raise Exception("closing delimeter is not found")
            i = 0
            while i < length:
                if i % 2 == 0:
                    node_parts.append(TextNode(node_segments[i], TextType.TEXT))
                else:
                    node_parts.append(TextNode(node_segments[i], text_type))
                i += 1
        node_result.extend(node_parts)
    return node_result