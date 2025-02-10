import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "https:/www.tro.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https:/www.tro.com")
        self.assertEqual(node, node2)

    def test_ineq2(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https:/www.tro.com")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_print(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), node2)

class TestTextNodeToHTML(unittest.TestCase):
    def test_convert(self):
        textnode = TextNode("This is a text node", TextType.ITALIC, "https:/www.tro.com")   
        node = textnode_to_htmlnode(textnode)
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "This is a text node")

    def test_convert_no_tag(self):
        textnode = TextNode("This is a text node", TextType.TEXT)   
        node = textnode_to_htmlnode(textnode)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "This is a text node")

    def test_convert_link(self):
        textnode = TextNode("This is a text node", TextType.LINK, "https://www.tro.com")   
        node = textnode_to_htmlnode(textnode)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a text node")
        self.assertEqual(node.props, {"href": "https://www.tro.com"})

    def test_error(self):
        self.assertRaises(Exception, lambda: textnode_to_htmlnode(TextNode("text", "normal", "https://tro.com")))

    def test_convert_image(self):
        textnode = TextNode("This is an image", TextType.IMAGE, "https://www.tro.com")
        node = textnode_to_htmlnode(textnode)
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src": "https://www.tro.com", "alt": "This is an image"})

    def test_convert_code(self):
        textnode = TextNode("This is a code", TextType.CODE)
        node = textnode_to_htmlnode(textnode)
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, "This is a code")

    def test_convert_bold(self):
        textnode = TextNode("This is a text", TextType.BOLD)
        node = textnode_to_htmlnode(textnode)
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "This is a text")
    

if __name__ == "__main__":
    unittest.main()