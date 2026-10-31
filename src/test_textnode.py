import unittest
from textnode import TextNode, TextType, text_node_to_html_node, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
            node = TextNode("This is a text node", TextType.BOLD, "https://pene.org")
            node2 = TextNode("This is a text node", TextType.BOLD, "https://pene.org")
            self.assertEqual(node, node2)

    def test_changed_text(self):
            node = TextNode("This is a text node", TextType.BOLD, "https://pene.org")
            node2 = TextNode("This is nota text node", TextType.BOLD, "https://pene.org")
            self.assertNotEqual(node, node2)

    def test_changed_type(self):
                node = TextNode("This is a text node", TextType.ITALIC, "https://pene.org")
                node2 = TextNode("This is a text node", TextType.BOLD, "https://pene.org")
                self.assertNotEqual(node, node2)

    def test_changed_url(self):
                    node = TextNode("This is a text node", TextType.BOLD, "https://vulva.org")
                    node2 = TextNode("This is a text node", TextType.BOLD, "https://pene.org")
                    self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Important text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Important text")
        self.assertEqual(html_node.to_html(), "<b>Important text</b>")


    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")


    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(
            html_node.to_html(),
            "<code>print('hello')</code>"
        )


    def test_link(self):
        node = TextNode(
            "Google",
            TextType.LINK,
            "https://google.com"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(
            html_node.props,
            {"href": "https://google.com"}
        )
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://google.com">Google</a>'
        )


    def test_image(self):
        node = TextNode(
            "A beautiful sunset",
            TextType.IMAGE,
            "https://example.com/sunset.png"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/sunset.png",
                "alt": "A beautiful sunset"
            }
        )
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/sunset.png" alt="A beautiful sunset"></img>'
        )


    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), "")


    def test_bold_empty_text(self):
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.to_html(), "<b></b>")


    def test_invalid_text_type(self):
        node = TextNode("Invalid text", "unknown")

        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


    def test_none_text_type(self):
        node = TextNode("Some text", None)

        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    

    




    


if __name__ == "__main__":
    unittest.main()