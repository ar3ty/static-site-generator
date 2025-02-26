import unittest

from block import *

class TestMarkdownToBlock (unittest.TestCase):
    def test_simple(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text"
        expected_list = [
            "# This is a heading",
            "This is a paragraph of text"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_list)

    def test_three(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text\n\n Another one"
        expected_list = [
            "# This is a heading",
            "This is a paragraph of text",
            "Another one"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_list)

    def test_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text\n\n Another one\n Here you go"
        expected_list = [
            "# This is a heading",
            "This is a paragraph of text",
            "Another one\n Here you go"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_list)

    def test_another_text(self):
        markdown = """
# This is a heading

This is a paragraph of text

* Another one
* Here you go

Yep        
"""        
        expected_list = [
            "# This is a heading",
            "This is a paragraph of text",
            "* Another one\n* Here you go",
            "Yep"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_list)

class TestBlockToBlockType (unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph\nThis is a paragraph of text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_2(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_3(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_4(self):
        block = "####This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = ">This is a quote\n>This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_2(self):
        block = ">This is a quote\nThis is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code(self):
        block = "```\nthis is\na code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
    def test_code_2(self):
        block = """
```
this is not
a code 
"""       
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered(self):
        block = "- This is a list\n- This is an another line of list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_2(self):
        block = "- This is a list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_3(self):
        block = "- This is a list\nThis is not an another line of list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered(self):
        block = "1. This is a list\n2. This is an another line of list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_2(self):
        block = "1. This is a list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_3(self):
        block = "1. This is a list\nThis is not an another line of list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()