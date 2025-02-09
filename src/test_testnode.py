import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()