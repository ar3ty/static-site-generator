import unittest

from delimeter import split_nodes_delimeter
from textnode import *

class TestDelimiterSplit (unittest.TestCase):
    def test_simple(self):
        node1 = TextNode("this is **bold** text", TextType.TEXT)
        nodes = split_nodes_delimeter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))


    def test_multiple(self):
        node1 = TextNode("this is **bold** text and **bold also** text again", TextType.TEXT)
        nodes = split_nodes_delimeter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text and ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode("bold also", TextType.BOLD))
        self.assertEqual(nodes[4], TextNode(" text again", TextType.TEXT))


    def test_no_delimeter(self):
        node1 = TextNode("this is text", TextType.TEXT)
        nodes = split_nodes_delimeter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is text", TextType.TEXT))

    def test_odd_delimiters(self):
        node1 = TextNode("**this is text", TextType.TEXT)
        node2 = TextNode("**this** is text**", TextType.TEXT)
        self.assertRaises(Exception, lambda: split_nodes_delimeter([node1], "**", TextType.BOLD))
        self.assertRaises(Exception, lambda: split_nodes_delimeter([node2], "**", TextType.BOLD))

    def test_empty_inner_text(self):
        node1 = TextNode("this is ** ** text", TextType.TEXT)
        nodes = split_nodes_delimeter([node1], "**", TextType.BOLD)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(" ", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))

    def test_code_sample(self):
        node1 = TextNode("this is `code` text", TextType.TEXT)
        nodes = split_nodes_delimeter([node1], "`", TextType.CODE)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))

    def test_italic_sample(self):
        node1 = TextNode("this is *italic* text", TextType.TEXT)
        nodes = split_nodes_delimeter([node1], "*", TextType.ITALIC)
        self.assertEqual(nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes[2], TextNode(" text", TextType.TEXT))