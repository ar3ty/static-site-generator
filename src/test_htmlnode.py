import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        props = {"href": "https://www.google.com"}
        node1 = HTMLNode("p", "text inside the paragraph", None, props)
        self.assertEqual(repr(node1), "HTMLNode(Tag: p, value: text inside the paragraph, children: None, props: {'href': 'https://www.google.com'})")

    def test_props_method_and_values(self):
        props = {
            "href": "https://www.google.com",
          "target": "_blank",
        }
        node1 = HTMLNode("a", "text inside the paragraph", None, props)
        self.assertEqual(node1.props_to_html(),  ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node1.props, {'href': 'https://www.google.com', 'target': '_blank'})
        self.assertEqual(node1.tag, "a")
        self.assertEqual(node1.children, None)
        self.assertEqual(node1.value, "text inside the paragraph")
    
    def test_repr_children(self):
        props = {"href": "https://www.google.com"}
        children = [HTMLNode("span", "child text")]
        node1 = HTMLNode("a", "text inside the paragraph", children, props)
        self.assertEqual(repr(node1), 
                         "HTMLNode(Tag: a, value: text inside the paragraph, children: [HTMLNode(Tag: span, value: child text, children: None, props: None)], props: {'href': 'https://www.google.com'})")
        
    def test_leafnode(self):
        node1 = LeafNode("p", "paragraph of text")
        self.assertEqual(node1.to_html(), '<p>paragraph of text</p>')

    def test_leafnode2(self):
        node1 = LeafNode("a", "hypertext", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), '<a href="https://www.google.com">hypertext</a>')

    def test_leafnode_no_tag(self):
        node1 = LeafNode(None, "text")
        self.assertEqual(node1.to_html(), "text")

    def test_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        str_node = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), str_node)
    
    def test_parentnode_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_parentnode_no_tag(self):
        node = ParentNode(None, None)
        self.assertRaises(ValueError, lambda: node.to_html())
  
    def test_parentnode_parent(self):
        node = ParentNode(
            "h1",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        str_node = '<h1><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><i>italic text</i>Normal text</h1>'
        self.assertEqual(node.to_html(), str_node)
    
    def test_perentnode_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchildren")
        child = ParentNode("p", [grandchild])
        parent = ParentNode("h1", [child])
        self.assertEqual(parent.to_html(), '<h1><p><b>grandchildren</b></p></h1>')