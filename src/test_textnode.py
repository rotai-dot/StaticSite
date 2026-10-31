import unittest
from textnode import TextNode, TextType


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




    


if __name__ == "__main__":
    unittest.main()