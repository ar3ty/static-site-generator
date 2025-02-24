import unittest

from inline import *
from textnode import *

class TestDelimiterSplit (unittest.TestCase):
    def test_simple(self):
        node1 = TextNode("this is **bold** text", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))

    def test_multiple(self):
        node1 = TextNode("this is **bold** text and **bold also** text again", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text and ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode("bold also", TextType.BOLD))
        self.assertEqual(nodes[4], TextNode(" text again", TextType.TEXT))

    def test_no_delimeter(self):
        node1 = TextNode("this is text", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is text", TextType.TEXT))

    def test_odd_delimiters(self):
        node1 = TextNode("**this is text", TextType.TEXT)
        node2 = TextNode("**this** is text**", TextType.TEXT)
        self.assertRaises(Exception, lambda: split_nodes_delimiter([node1], "**", TextType.BOLD))
        self.assertRaises(Exception, lambda: split_nodes_delimiter([node2], "**", TextType.BOLD))

    def test_empty_inner_text(self):
        node1 = TextNode("this is ** ** text", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(" ", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))

    def test_code_sample(self):
        node1 = TextNode("this is `code` text", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))

    def test_italic_sample(self):
        node1 = TextNode("this is *italic* text", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "*", TextType.ITALIC)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))
    
    def test_nonexist_inner_text(self):
        node1 = TextNode("this is **** text", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(" text", TextType.TEXT))

    def test_bold_and_italic(self):
        node1 = TextNode("this text is **bold** and *italic*", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("this text is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
           nodes
        )

class TestExtractLinks (unittest.TestCase):
    def test_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(extract_markdown_links(text), [])

    def test_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(extract_markdown_images(text), [])

class TestSplitNodeImages (unittest.TestCase):
    def test_before_and_after(self):
        node = TextNode("Here is an image ![alt1](link1), and here is text after it.", TextType.TEXT)
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "link1"),
            TextNode(", and here is text after it.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_images([node]), expected_nodes)

    def test_before(self):
        node = TextNode("Here is an image ![alt1](link1)", TextType.TEXT)
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "link1"),
        ]
        self.assertEqual(split_nodes_images([node]), expected_nodes)

    def test_after(self):
        node = TextNode("![alt1](link1), and here is text after it.", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.IMAGE, "link1"),
            TextNode(", and here is text after it.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_images([node]), expected_nodes)

    def test_before_and_after_sequence(self):
        node = TextNode("Here is an image ![alt1](link1), and here is text after it ![alt2](link2), and another part of text", TextType.TEXT)
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "link1"),
            TextNode(", and here is text after it ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "link2"),
            TextNode(", and another part of text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_images([node]), expected_nodes)

    def test_multiple(self):
        node = TextNode("![alt1](link1)![alt2](link2)![alt3](link3)", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.IMAGE, "link1"),
            TextNode("alt2", TextType.IMAGE, "link2"),
            TextNode("alt3", TextType.IMAGE, "link3")
        ]
        self.assertEqual(split_nodes_images([node]), expected_nodes)

    def test_multiple_and_text(self):
        node = TextNode("![alt1](link1)![alt2](link2), and text", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.IMAGE, "link1"),
            TextNode("alt2", TextType.IMAGE, "link2"),
            TextNode(", and text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_images([node]), expected_nodes)

    def test_single(self):
        node = TextNode("![alt1](link1)", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.IMAGE, "link1"),
        ]
        self.assertEqual(split_nodes_images([node]), expected_nodes)

class TestSplitNodeLinks (unittest.TestCase):
    def test_before_and_after(self):
        node = TextNode("Here is an link [alt1](link1), and here is text after it.", TextType.TEXT)
        expected_nodes = [
            TextNode("Here is an link ", TextType.TEXT),
            TextNode("alt1", TextType.LINK, "link1"),
            TextNode(", and here is text after it.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_links([node]), expected_nodes)

    def test_before(self):
        node = TextNode("Here is an link [alt1](link1)", TextType.TEXT)
        expected_nodes = [
            TextNode("Here is an link ", TextType.TEXT),
            TextNode("alt1", TextType.LINK, "link1"),
        ]
        self.assertEqual(split_nodes_links([node]), expected_nodes)

    def test_after(self):
        node = TextNode("[alt1](link1), and here is text after it.", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.LINK, "link1"),
            TextNode(", and here is text after it.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_links([node]), expected_nodes)

    def test_before_and_after_sequence(self):
        node = TextNode("Here is an link [alt1](link1), and here is text after it [alt2](link2), and another part of text", TextType.TEXT)
        expected_nodes = [
            TextNode("Here is an link ", TextType.TEXT),
            TextNode("alt1", TextType.LINK, "link1"),
            TextNode(", and here is text after it ", TextType.TEXT),
            TextNode("alt2", TextType.LINK, "link2"),
            TextNode(", and another part of text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_links([node]), expected_nodes)

    def test_multiple(self):
        node = TextNode("[alt1](link1)[alt2](link2)[alt3](link3)", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.LINK, "link1"),
            TextNode("alt2", TextType.LINK, "link2"),
            TextNode("alt3", TextType.LINK, "link3")
        ]
        self.assertEqual(split_nodes_links([node]), expected_nodes)

    def test_multiple_and_text(self):
        node = TextNode("[alt1](link1)[alt2](link2), and text", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.LINK, "link1"),
            TextNode("alt2", TextType.LINK, "link2"),
            TextNode(", and text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_links([node]), expected_nodes)

    def test_single(self):
        node = TextNode("[alt1](link1)", TextType.TEXT)
        expected_nodes = [
            TextNode("alt1", TextType.LINK, "link1"),
        ]
        self.assertEqual(split_nodes_links([node]), expected_nodes)

class TestTextToNode (unittest.TestCase):
    def test_multiple(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(text_to_textnodes(text), expected_nodes)

    def test_text(self):
        text = "This is text"
        expected_nodes = [
            TextNode("This is text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected_nodes)

if __name__ == "__main__":
    unittest.main()