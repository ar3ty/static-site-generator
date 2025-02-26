from textnode import *

import re 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_result = []
    for node in old_nodes:
        node_parts = []
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            node_parts.append(node)
        else:
            node_segments = node.text.split(delimiter)
            length = len(node_segments)
            if length % 2 == 0:
                raise Exception("closing delimeter is not found")
            i = 0
            while i < length:
                if node_segments[i] == "":
                    i += 1
                    continue
                if i % 2 == 0:
                    node_parts.append(TextNode(node_segments[i], TextType.TEXT))
                else:
                    node_parts.append(TextNode(node_segments[i], text_type))
                i += 1
        node_result.extend(node_parts)
    return node_result

def extract_markdown_images(text):
     return re.findall(r'(?<=!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def split_nodes_images(old_nodes):
    node_result = []
    for node in old_nodes:
        node_parts = []
        list_of_images = extract_markdown_images(node.text)
        if node.text_type != TextType.TEXT or list_of_images == []:
            node_parts.append(node)
        else:
            length = len(list_of_images)
            i = 0
            text_edited = node.text
            while i < length:
                alt_image = list_of_images[i][0]
                link_image = list_of_images[i][1]
                node_segments = text_edited.split(f"![{alt_image}]({link_image})", 1)
                if node_segments[0] == "":
                    node_parts.append(TextNode(alt_image, TextType.IMAGE, link_image))
                else:
                    node_parts.append(TextNode(node_segments[0], TextType.TEXT))
                    node_parts.append(TextNode(alt_image, TextType.IMAGE, link_image))
                text_edited = node_segments[1]
                i += 1
            if text_edited != "":
                node_parts.append(TextNode(text_edited, TextType.TEXT))
        node_result.extend(node_parts)
    return node_result

def split_nodes_links(old_nodes):
    node_result = []
    for node in old_nodes:
        node_parts = []
        list_of_links = extract_markdown_links(node.text)
        if node.text_type != TextType.TEXT or list_of_links == []:
            node_parts.append(node)
        else:
            length = len(list_of_links)
            i = 0
            text_edited = node.text
            while i < length:
                alt_image = list_of_links[i][0]
                link_image = list_of_links[i][1]
                node_segments = text_edited.split(f"[{alt_image}]({link_image})", 1)
                if node_segments[0] == "":
                    node_parts.append(TextNode(alt_image, TextType.LINK, link_image))
                else:
                    node_parts.append(TextNode(node_segments[0], TextType.TEXT))
                    node_parts.append(TextNode(alt_image, TextType.LINK, link_image))
                text_edited = node_segments[1]
                i += 1
            if text_edited != "":
                node_parts.append(TextNode(text_edited, TextType.TEXT))
        node_result.extend(node_parts)
    return node_result

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes