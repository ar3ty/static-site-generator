from enum import Enum
from htmlnode import *
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
            check_heading = re.match('#{1,6}\s', block)
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
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parentnodes = []
    for block in blocks:
        new_parent = ParentNode()
