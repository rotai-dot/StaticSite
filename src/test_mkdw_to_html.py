import unittest
from mkdw_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):

    # PÁRRAFOS

    def test_simple_paragraph(self):
        md = "This is a paragraph."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph.</p></div>",
        )

    def test_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph.</p><p>Second paragraph.</p></div>",
        )

    def test_multiline_paragraph(self):
        md = "First line\nSecond line\nThird line"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>First line Second line Third line</p></div>",
        )

    def test_paragraph_with_inline_formatting(self):
        md = "Hello **bold**, _italic_ and `code`."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>Hello <b>bold</b>, <i>italic</i> and <code>code</code>.</p></div>",
        )

    def test_paragraph_with_link(self):
        md = "Visit [Python](https://python.org)."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><p>Visit <a href="https://python.org">Python</a>.</p></div>',
        )

    # ENCABEZADOS

    def test_heading_h1(self):
        html = markdown_to_html_node("# Title").to_html()
        self.assertEqual(html, "<div><h1>Title</h1></div>")

    def test_heading_h2(self):
        html = markdown_to_html_node("## Subtitle").to_html()
        self.assertEqual(html, "<div><h2>Subtitle</h2></div>")

    def test_heading_h3(self):
        html = markdown_to_html_node("### Section").to_html()
        self.assertEqual(html, "<div><h3>Section</h3></div>")

    def test_heading_h6(self):
        html = markdown_to_html_node("###### Small heading").to_html()
        self.assertEqual(
            html,
            "<div><h6>Small heading</h6></div>",
        )

    def test_heading_with_bold(self):
        html = markdown_to_html_node("## Hello **world**").to_html()
        self.assertEqual(
            html,
            "<div><h2>Hello <b>world</b></h2></div>",
        )

    # CITAS

    def test_simple_quote(self):
        html = markdown_to_html_node("> Hello").to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Hello</blockquote></div>",
        )

    def test_multiline_quote(self):
        md = "> First line\n> Second line"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>First line\nSecond line</blockquote></div>",
        )

    def test_quote_without_spaces(self):
        md = ">First line\n>Second line"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>First line\nSecond line</blockquote></div>",
        )

    def test_quote_with_inline_formatting(self):
        html = markdown_to_html_node("> Hello **world**").to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Hello <b>world</b></blockquote></div>",
        )

    # LISTAS NO ORDENADAS

    def test_unordered_list(self):
        md = "- Apple\n- Banana\n- Cherry"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul></div>",
        )

    def test_unordered_list_with_bold(self):
        md = "- Apple\n- **Banana**"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Apple</li><li><b>Banana</b></li></ul></div>",
        )

    def test_unordered_list_single_item(self):
        html = markdown_to_html_node("- Only item").to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Only item</li></ul></div>",
        )

    # LISTAS ORDENADAS

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_ordered_list_with_inline_formatting(self):
        md = "1. **Bold**\n2. _Italic_"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>Bold</b></li><li><i>Italic</i></li></ol></div>",
        )

    def test_ordered_list_twelve_items(self):
        md = "\n".join(f"{i}. Item {i}" for i in range(1, 13))
        html = markdown_to_html_node(md).to_html()
        expected_items = "".join(
            f"<li>Item {i}</li>" for i in range(1, 13)
        )
        self.assertEqual(
            html,
            f"<div><ol>{expected_items}</ol></div>",
        )

    # BLOQUES DE CÓDIGO

    def test_code_block(self):
        md = "```\nprint('hello')\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>print('hello')\n</code></pre></div>",
        )

    def test_code_block_preserves_markdown(self):
        md = "```\n**bold** and _italic_\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>**bold** and _italic_\n</code></pre></div>",
        )

    def test_code_block_multiline(self):
        md = "```\nline one\nline two\nline three\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>line one\nline two\nline three\n</code></pre></div>",
        )

    # DOCUMENTO COMPLETO

    def test_mixed_document(self):
        md = (
            "# Title\n\n"
            "Hello **world**.\n\n"
            "- First\n- Second\n\n"
            "> A quote\n\n"
            "```\nprint('done')\n```"
        )

        html = markdown_to_html_node(md).to_html()

        self.assertEqual(
            html,
            "<div>"
            "<h1>Title</h1>"
            "<p>Hello <b>world</b>.</p>"
            "<ul><li>First</li><li>Second</li></ul>"
            "<blockquote>A quote</blockquote>"
            "<pre><code>print('done')\n</code></pre>"
            "</div>",
        )

    def test_empty_document(self):
        html = markdown_to_html_node("").to_html()
        self.assertEqual(html, "<div></div>")
