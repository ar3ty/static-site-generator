import unittest

from block import *
from textnode import *
from inline import *

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
        block = "> This is a quote\n> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_2(self):
        block = "> This is a quote\nThis is not a quote"
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

class TestConverters (unittest.TestCase):
    def test_paragraph_to_html(self):
        block = "This is a paragraph\nwith **bold** and _italic_ text"
        children = [
            LeafNode(None, "This is a paragraph with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text")
        ]
        expected = ParentNode("p", children)
        self.assertEqual(paragraph_to_htmlnode(block), expected)

    def test_paragraph_to_html_2(self):
        block = "This is a paragraph with **bold** and _italic_ text"
        children = [
            LeafNode(None, "This is a paragraph\nwith "),
            LeafNode("b", "bold"),
            LeafNode("i", "italic"),
            LeafNode(None, " text")
        ]
        expected = ParentNode("p", children)
        self.assertNotEqual(paragraph_to_htmlnode(block), expected)

    def test_code_to_html(self):
        block = "```This is a code\nwith **bold** and _italic_ text```"
        children = [
            LeafNode("code", "This is a code\nwith **bold** and _italic_ text")
        ]
        expected = ParentNode("pre", children)
        node = code_to_htmlnode(block)
        self.assertEqual(node, expected)
        self.assertEqual(node.to_html(), "<pre><code>This is a code\nwith **bold** and _italic_ text</code></pre>")

    def test_quote_to_html(self):
        block = "> This is a quote\n> with **bold** and _italic_ text"
        children = [
            LeafNode(None, "This is a quote with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text"),
        ]
        expected = ParentNode("blockquote", children)
        self.assertEqual(quote_to_htmlnode(block), expected)

    def test_heading_to_html(self):
        block = "###### This is a heading"
        children = [
            LeafNode(None, "This is a heading"),
        ]
        expected = ParentNode("h6", children)
        self.assertEqual(heading_to_htmlnode(block), expected)

    def test_heading_to_html_2(self):
        block = "## This is a heading\nwith **bold** and _italic_ text"
        children = [
            LeafNode(None, "This is a heading with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text"),
        ]
        expected = ParentNode("h2", children)
        self.assertEqual(heading_to_htmlnode(block), expected)

    def test_unordered_to_html(self):
        block = "- This is a **list**\n- with **bold** and _italic_ text"
        children1 = [
            LeafNode(None, "This is a "),
            LeafNode("b", "list")
        ]
        children2 = [
            LeafNode(None, "with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text")
        ]
        expected = ParentNode("ul", [ParentNode("li", children1), ParentNode("li", children2)])
        self.assertEqual(unordered_to_htmlnode(block), expected)

    def test_ordered_to_html(self):
        block = "1. This is a **list**\n2. with **bold** and _italic_ text"
        children1 = [
            LeafNode(None, "This is a "),
            LeafNode("b", "list")
        ]
        children2 = [
            LeafNode(None, "with "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text")
        ]
        expected = ParentNode("ol", [ParentNode("li", children1), ParentNode("li", children2)])
        node = ordered_to_htmlnode(block)
        self.assertEqual(node, expected)
        self.assertEqual(node.to_html(), "<ol><li>This is a <b>list</b></li><li>with <b>bold</b> and <i>italic</i> text</li></ol>")

    def test_ordered_to_html_2(self):
        block = "1. This is a **list**"
        children1 = [
            LeafNode(None, "This is a "),
            LeafNode("b", "list")
        ]
        expected = ParentNode("ol", [ParentNode("li", children1)])
        self.assertEqual(ordered_to_htmlnode(block), expected)

    def test_text_to_children(self):
        text = "This is a paragraph\nwith **bold** and _italic_ text"
        expected = [
            LeafNode(None, "This is a paragraph\nwith "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text"),
        ]
        self.assertEqual(text_to_children(text), expected)
    
    def test_format(self):
        md = """
This is **bolded** paragraph
text in a p
tag here
"""
        expected = "This is **bolded** paragraph text in a p tag here"
        self.assertEqual(text_formatter(md), expected)

        

class TestMarkdownToHtmlNodes (unittest.TestCase):
    def test_to_html(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        expected = markdown_to_html_nodes(md)
        self.assertEqual(
            expected.to_html(), 
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )
            
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        expected = markdown_to_html_nodes(md)
        self.assertEqual(
            expected.to_html(), 
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )

    def test_block_of_quote(self):
        md = """
> This is quote
> text in quote

This is paragraph with _italic_ text and `code` here

"""
        expected = markdown_to_html_nodes(md)
        self.assertEqual(
            expected.to_html(), 
            "<div><blockquote>This is quote text in quote</blockquote><p>This is paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_lists(self):
        md = """
1. Ordered list
2. with some text
3. third line

- This is list
- text in list
- here you are
"""
        expected = markdown_to_html_nodes(md)
        self.assertEqual(
            expected.to_html(), 
            "<div><ol><li>Ordered list</li><li>with some text</li><li>third line</li></ol><ul><li>This is list</li><li>text in list</li><li>here you are</li></ul></div>"
        )

    def test_headings(self):
        md = """
# this is an heading rank 1

####### this is not heading 

this is paragraph text

###### this is an h6
"""

        node = markdown_to_html_nodes(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an heading rank 1</h1><p>####### this is not heading</p><p>this is paragraph text</p><h6>this is an h6</h6></div>",
        )




if __name__ == "__main__":
    unittest.main()