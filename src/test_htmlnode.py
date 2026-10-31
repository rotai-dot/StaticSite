import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_multiple_leaf_children(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello"),
            LeafNode("b", "World"),
            LeafNode("i", "!")
        ])
        self.assertEqual(
            node.to_html(),
            "<div><p>Hello</p><b>World</b><i>!</i></div>"
        )

    def test_parent_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><p>Hello</p></div>'
        )

    def test_children_with_props(self):
        node = ParentNode("div", [
            LeafNode("a", "Google", {"href": "https://google.com"}),
            LeafNode("span", "Text", {"class": "highlight"})
        ])
        self.assertEqual(
            node.to_html(),
            '<div><a href="https://google.com">Google</a><span class="highlight">Text</span></div>'
        )

    def test_nested_parents_and_siblings(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("b", "Deep")
                ]),
                LeafNode("i", "Middle")
            ]),
            LeafNode("p", "Outside")
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><article><b>Deep</b></article><i>Middle</i></section><p>Outside</p></div>"
        )

    def test_children_without_tags(self):
        node = ParentNode("p", [
            LeafNode(None, "Hello "),
            LeafNode("b", "World"),
            LeafNode(None, "!")
        ])
        self.assertEqual(
            node.to_html(),
            "<p>Hello <b>World</b>!</p>"
        )

    def test_missing_tag(self):
        node = ParentNode(None, [
            LeafNode("p", "Hello")
        ])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_missing_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")




if __name__ == "__main__":
    unittest.main()
