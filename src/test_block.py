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


if __name__ == "__main__":
    unittest.main()