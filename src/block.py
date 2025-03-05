from enum import Enum
from htmlnode import *
from inline import text_to_textnodes, textnode_to_htmlnode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block == "":
            continue
        new_blocks.append(new_block)
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    match block[0]:
        case "#":
            check_heading = re.match(r'(?<!#)#{1,6}\s', block)
            if check_heading == None:
                return BlockType.PARAGRAPH
            return BlockType.HEADING
        case "`":
            if block[:3] == "```" and block[-3:] == "```":
                return BlockType.CODE
            return BlockType.PARAGRAPH
        case ">":
            for line in lines:
                if line[0] != ">":
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        case "-":
            for line in lines:
                if line[:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case "1":
            for i in range(len(lines)):
                if lines[i][:3] != f"{i+1}. ":
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

def code_to_htmlnode(block):
    text = block[3:-3].lstrip("\n")
    child = LeafNode("code", text)
    return ParentNode("pre", [child])

def quote_to_htmlnode(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        redacted_line = line[2:]
        new_lines.append(redacted_line.strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def heading_to_htmlnode(block):
    check_heading = re.match(r'(#{1,6})', block).group(0)
    rank = len(check_heading)
    text = block[rank+1:]
    formatted_text = text_formatter(text)
    children = text_to_children(formatted_text)
    return ParentNode(f"h{rank}", children)

def paragraph_to_htmlnode(block):
    formatted_text = text_formatter(block)
    children = text_to_children(formatted_text)
    return ParentNode("p", children)

def unordered_to_htmlnode(block):
    lines = block.split("\n")
    children_of_block = []
    for line in lines:
        new_line = line[2:]
        children_of_line = text_to_children(new_line.strip())
        parent_of_line = ParentNode("li", children_of_line)
        children_of_block.append(parent_of_line)
    return ParentNode("ul", children_of_block)

def ordered_to_htmlnode(block):
    lines = block.split("\n")
    children_of_block = []
    for line in lines:
        new_line = line[3:]
        children_of_line = text_to_children(new_line.strip())
        parent_of_line = ParentNode("li", children_of_line)
        children_of_block.append(parent_of_line)
    return ParentNode("ol", children_of_block)

def text_formatter(text):
    lines = text.strip().split("\n")
    stripped_lines = [line.strip() for line in lines]
    return " ".join(stripped_lines)

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for node in textnodes:
        new_node = textnode_to_htmlnode(node)
        htmlnodes.append(new_node)
    return htmlnodes

def handle_block_type(block):
     blocktype = block_to_block_type(block)
     match blocktype:
        case BlockType.HEADING:
            return heading_to_htmlnode(block)
        case BlockType.CODE:
            return code_to_htmlnode(block)
        case BlockType.QUOTE:
            return quote_to_htmlnode(block)
        case BlockType.UNORDERED_LIST:
            return unordered_to_htmlnode(block)
        case BlockType.ORDERED_LIST:
            return ordered_to_htmlnode(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_htmlnode(block)
        case _:
            raise Exception("Unknown blocktype")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        parent_node = handle_block_type(block)
        parent_nodes.append(parent_node)
    grandpa_node = ParentNode("div", parent_nodes)
    return grandpa_node