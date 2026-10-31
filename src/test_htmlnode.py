import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_none_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_single_prop(self):
        node = HTMLNode(props={"class": "highlight"})
        self.assertEqual(
            node.props_to_html(),
            ' class="highlight"'
        )

    def test_different_props(self):
        node = HTMLNode(props={
            "id": "main",
            "class": "container"
        })
        self.assertEqual(
            node.props_to_html(),
            ' id="main" class="container"'
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_ref(self):
        node = LeafNode("a", "Hello, world!", {"href": "google.com"})
        self.assertEqual(node.to_html(), '<a href="google.com">Hello, world!</a>')

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Important!")
        self.assertEqual(node.to_html(), "<b>Important!</b>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Click here",
            {"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank">Click here</a>'
        )

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_empty_string(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("span", "Hello", {})
        self.assertEqual(node.to_html(), "<span>Hello</span>")




if __name__ == "__main__":
    unittest.main()
