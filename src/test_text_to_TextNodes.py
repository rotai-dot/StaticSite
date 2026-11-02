import unittest
from textnode import TextType, TextNode
from text_to_TextNodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestDelimiterFunction(unittest.TestCase):
    def test_delimiter_at_start(self):
        node = TextNode("**bold** and normal", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and normal", TextType.TEXT),
        ])


    def test_delimiter_at_end(self):
        node = TextNode("normal and _italic_", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(result, [
            TextNode("normal and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])


    def test_multiple_delimited_sections(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.BOLD),
            TextNode(" e", TextType.TEXT),
        ])


    def test_preserve_non_text_nodes(self):
        nodes = [
            TextNode("Already bold", TextType.BOLD),
            TextNode(" and _italic_", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        self.assertEqual(result, [
            TextNode("Already bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])


    def test_unclosed_delimiter(self):
        node = TextNode("Text with **unclosed bold", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_no_delimiter(self):
        node = TextNode("Just normal text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [
        TextNode("Just normal text", TextType.TEXT)
    ])


    def test_empty_list(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)

        self.assertEqual(result, [])


    def test_multiple_passes(self):
        nodes = [
            TextNode("A **bold** and _italic_ sentence", TextType.TEXT)
        ]

        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        self.assertEqual(nodes, [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" sentence", TextType.TEXT),
        ])

class TestMarkdowImg_Links(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = (
            "First ![cat](https://example.com/cat.png) "
            "and second ![dog](https://example.com/dog.jpg)"
        )

        matches = extract_markdown_images(text)

        self.assertListEqual([
                ("cat", "https://example.com/cat.png"),
                ("dog", "https://example.com/dog.jpg")
            ], matches)


    def test_extract_no_images(self):
        text = "This is normal text without any images."

        matches = extract_markdown_images(text)

        self.assertListEqual([], matches)


    def test_extract_empty_alt_text(self):
        text = "An image ![](https://example.com/image.png)"

        matches = extract_markdown_images(text)

        self.assertListEqual([
            ("", "https://example.com/image.png")
        ], matches)


    def test_extract_image_at_start(self):
        text = "![logo](https://example.com/logo.svg) Some text"

        matches = extract_markdown_images(text)

        self.assertListEqual([
            ("logo", "https://example.com/logo.svg")
        ], matches)


    def test_extract_image_at_end(self):
        text = "Some text ![photo](https://example.com/photo.jpg)"

        matches = extract_markdown_images(text)

        self.assertListEqual([
            ("photo", "https://example.com/photo.jpg")
        ], matches)


    def test_extract_ignore_normal_links(self):
        text = (
            "Visit [Google](https://google.com) "
            "and see ![logo](https://example.com/logo.png)"
        )

        matches = extract_markdown_images(text)

        self.assertListEqual([
            ("logo", "https://example.com/logo.png")
        ], matches)


    def test_extract_image_with_spaces_in_alt(self):
        text = "![A beautiful red sunset](https://example.com/sunset.png)"

        matches = extract_markdown_images(text)

        self.assertListEqual([
            ("A beautiful red sunset", "https://example.com/sunset.png")
        ], matches)

    def test_extract_single_link(self):
        text = "Visit [Google](https://google.com)"

        matches = extract_markdown_links(text)

        self.assertListEqual([
            ("Google", "https://google.com")
        ], matches)


    def test_extract_multiple_links(self):
        text = (
            "Visit [Google](https://google.com) "
            "or [GitHub](https://github.com)"
        )

        matches = extract_markdown_links(text)

        self.assertListEqual([
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ], matches)


    def test_extract_no_links(self):
        text = "This is normal text without any links."

        matches = extract_markdown_links(text)

        self.assertListEqual([], matches)


    def test_extract_empty_link_text(self):
        text = "An empty link [](https://example.com)"

        matches = extract_markdown_links(text)

        self.assertListEqual([
            ("", "https://example.com")
        ], matches)


    def test_extract_link_at_start(self):
        text = "[Python](https://python.org) is useful"

        matches = extract_markdown_links(text)

        self.assertListEqual([
            ("Python", "https://python.org")
        ], matches)


    def test_extract_link_at_end(self):
        text = "Read the documentation at [Python](https://python.org)"

        matches = extract_markdown_links(text)

        self.assertListEqual([
            ("Python", "https://python.org")
        ], matches)


    def test_extract_ignore_images(self):
        text = (
            "This is an ![image](https://example.com/image.png) "
            "and a [link](https://example.com/page)"
        )

        matches = extract_markdown_links(text)

        self.assertListEqual([
            ("link", "https://example.com/page")
        ], matches)


class test_split_nodes_image_link(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    
# =========================
# TESTS: SPLIT NODES IMAGE
# =========================

    def test_image_single(self):
        node = TextNode("Before ![cat](cat.png) after", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("Before ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" after", TextType.TEXT),
        ])


    def test_image_multiple(self):
        node = TextNode(
            "A ![cat](cat.png) B ![dog](dog.png) C",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("A ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" B ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
            TextNode(" C", TextType.TEXT),
        ])


    def test_image_at_start(self):
        node = TextNode("![cat](cat.png) after", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" after", TextType.TEXT),
        ])


    def test_image_at_end(self):
        node = TextNode("Before ![cat](cat.png)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("Before ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ])


    def test_image_only(self):
        node = TextNode("![cat](cat.png)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ])


    def test_image_adjacent(self):
        node = TextNode("![a](a.png)![b](b.png)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("a", TextType.IMAGE, "a.png"),
            TextNode("b", TextType.IMAGE, "b.png"),
        ])


    def test_image_no_match(self):
        node = TextNode("Nothing to extract here", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])


    def test_image_empty_input(self):
        self.assertEqual(split_nodes_image([]), [])


    def test_image_preserve_formatted_nodes(self):
        bold = TextNode("Already bold", TextType.BOLD)
        code = TextNode("![fake](fake.png)", TextType.CODE)
        node = TextNode("See ![real](real.png)", TextType.TEXT)

        self.assertEqual(split_nodes_image([bold, code, node]), [
            bold,
            code,
            TextNode("See ", TextType.TEXT),
            TextNode("real", TextType.IMAGE, "real.png"),
        ])


    def test_image_multiple_input_nodes(self):
        nodes = [
            TextNode("A ![one](1.png)", TextType.TEXT),
            TextNode(" B ![two](2.png) C", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "1.png"),
            TextNode(" B ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "2.png"),
            TextNode(" C", TextType.TEXT),
        ])


    def test_image_empty_alt(self):
        node = TextNode("X ![](image.png) Y", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("X ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "image.png"),
            TextNode(" Y", TextType.TEXT),
        ])


    def test_image_same_markup_twice(self):
        node = TextNode("![cat](cat.png) and ![cat](cat.png)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ])


    # =========================
    # TESTS: SPLIT NODES LINK
    # =========================

    def test_link_single(self):
        node = TextNode("Visit [Google](https://google.com) today", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" today", TextType.TEXT),
        ])


    def test_link_multiple(self):
        node = TextNode(
            "Try [Google](https://google.com) and [GitHub](https://github.com)",
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_link([node]), [
            TextNode("Try ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ])


    def test_link_at_start(self):
        node = TextNode("[Python](python.org) is useful", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("Python", TextType.LINK, "python.org"),
            TextNode(" is useful", TextType.TEXT),
        ])


    def test_link_at_end(self):
        node = TextNode("Visit [Python](python.org)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Python", TextType.LINK, "python.org"),
        ])


    def test_link_only(self):
        node = TextNode("[Python](python.org)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("Python", TextType.LINK, "python.org"),
        ])


    def test_link_adjacent(self):
        node = TextNode("[A](a.com)[B](b.com)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("A", TextType.LINK, "a.com"),
            TextNode("B", TextType.LINK, "b.com"),
        ])


    def test_link_no_match(self):
        node = TextNode("Just ordinary text", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])


    def test_link_empty_input(self):
        self.assertEqual(split_nodes_link([]), [])


    def test_link_preserve_formatted_nodes(self):
        italic = TextNode("Already italic", TextType.ITALIC)
        code = TextNode("[fake](fake.com)", TextType.CODE)
        node = TextNode("Go to [real](real.com)", TextType.TEXT)

        self.assertEqual(split_nodes_link([italic, code, node]), [
            italic,
            code,
            TextNode("Go to ", TextType.TEXT),
            TextNode("real", TextType.LINK, "real.com"),
        ])


    def test_link_multiple_input_nodes(self):
        nodes = [
            TextNode("A [one](one.com)", TextType.TEXT),
            TextNode(" B [two](two.com) C", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes), [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.LINK, "one.com"),
            TextNode(" B ", TextType.TEXT),
            TextNode("two", TextType.LINK, "two.com"),
            TextNode(" C", TextType.TEXT),
        ])


    def test_link_empty_label(self):
        node = TextNode("X [](page.html) Y", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("X ", TextType.TEXT),
            TextNode("", TextType.LINK, "page.html"),
            TextNode(" Y", TextType.TEXT),
        ])


    def test_link_same_markup_twice(self):
        node = TextNode("[A](a.com) and [A](a.com)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [
            TextNode("A", TextType.LINK, "a.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("A", TextType.LINK, "a.com"),
        ])
    
    def test_split_images_then_links(self):
        nodes = [
            TextNode(
                "See ![cat](cat.png) and visit [Python](python.org)",
                TextType.TEXT,
            )
        ]

        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)

        self.assertEqual(nodes, [
            TextNode("See ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and visit ", TextType.TEXT),
            TextNode("Python", TextType.LINK, "python.org"),
        ])

class test_text_to_textnodes(unittest.TestCase):

    def test_text_to_textnodes_all_formats(self):
        text = (
            "Hola **mundo**, esto es _cursiva_, esto es `codigo`, "
            "mira ![gato](gato.png) y visita [Python](https://python.org)."
        )

        result = text_to_textnodes(text)

        self.assertEqual(result, [
            TextNode("Hola ", TextType.TEXT),
            TextNode("mundo", TextType.BOLD),
            TextNode(", esto es ", TextType.TEXT),
            TextNode("cursiva", TextType.ITALIC),
            TextNode(", esto es ", TextType.TEXT),
            TextNode("codigo", TextType.CODE),
            TextNode(", mira ", TextType.TEXT),
            TextNode("gato", TextType.IMAGE, "gato.png"),
            TextNode(" y visita ", TextType.TEXT),
            TextNode("Python", TextType.LINK, "https://python.org"),
            TextNode(".", TextType.TEXT),
        ])


    def test_text_to_textnodes_plain_text(self):
        result = text_to_textnodes("Just ordinary text")

        self.assertEqual(result, [
            TextNode("Just ordinary text", TextType.TEXT),
        ])


    def test_text_to_textnodes_code_protection(self):
        result = text_to_textnodes("Example: `**bold** and _italic_`")

        self.assertEqual(result, [
            TextNode("Example: ", TextType.TEXT),
            TextNode("**bold** and _italic_", TextType.CODE),
        ])


    def test_text_to_textnodes_multiple_bold(self):
        result = text_to_textnodes("**one** and **two**")

        self.assertEqual(result, [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
        ])


    def test_text_to_textnodes_image_and_link(self):
        result = text_to_textnodes(
            "![logo](logo.png) [website](https://example.com)"
        )

        self.assertEqual(result, [
            TextNode("logo", TextType.IMAGE, "logo.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("website", TextType.LINK, "https://example.com"),
        ])


    def test_text_to_textnodes_unclosed_bold(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This has **unclosed bold")

