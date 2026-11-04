import unittest
from markdown_block import BlockType, markdown_to_blocks, block_to_block_type, is_list_or_quote

class test_mardown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_basic(self):
        markdown = (
            "# Heading\n\n"
            "This is a paragraph.\n\n"
            "- Item 1\n- Item 2"
        )
        self.assertEqual(markdown_to_blocks(markdown), [
            "# Heading",
            "This is a paragraph.",
            "- Item 1\n- Item 2",
        ])


    def test_markdown_to_blocks_multiple_empty_lines(self):
        markdown = "First paragraph.\n\n\n\nSecond paragraph.\n\n\n\nThird paragraph."
        self.assertEqual(markdown_to_blocks(markdown), [
            "First paragraph.",
            "Second paragraph.",
            "Third paragraph.",
        ])


    def test_markdown_to_blocks_leading_trailing_newlines(self):
        markdown = "\n\n\n# Title\n\nParagraph\n\n\n"
        self.assertEqual(markdown_to_blocks(markdown), [
            "# Title",
            "Paragraph",
        ])


    def test_markdown_to_blocks_whitespace(self):
        markdown = "   First paragraph   \n\n  Second paragraph  "
        self.assertEqual(markdown_to_blocks(markdown), [
            "First paragraph",
            "Second paragraph",
        ])


    def test_markdown_to_blocks_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])


    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n  \n\n   "
        self.assertEqual(markdown_to_blocks(markdown), [])


    def test_markdown_to_blocks_single_block(self):
        markdown = "A paragraph without blank lines."
        self.assertEqual(markdown_to_blocks(markdown), [
            "A paragraph without blank lines.",
        ])


    def test_markdown_to_blocks_preserve_internal_newlines(self):
        markdown = "- First item\n- Second item\n- Third item"
        self.assertEqual(markdown_to_blocks(markdown), [
            "- First item\n- Second item\n- Third item",
        ])


    def test_markdown_to_blocks_preserve_inline_markdown(self):
        markdown = (
            "A **bold** and _italic_ paragraph.\n\n"
            "A paragraph with `code` and [link](https://example.com)."
        )
        self.assertEqual(markdown_to_blocks(markdown), [
            "A **bold** and _italic_ paragraph.",
            "A paragraph with `code` and [link](https://example.com).",
        ])


    def test_markdown_to_blocks_whitespace_only_between_blocks(self):
        markdown = "First\n\n   \n\nSecond"
        self.assertEqual(markdown_to_blocks(markdown), [
            "First",
            "Second",
        ])


    def test_markdown_to_blocks_heading_and_paragraph(self):
        markdown = "## Subtitle\n\nSome text below the subtitle."
        self.assertEqual(markdown_to_blocks(markdown), [
            "## Subtitle",
            "Some text below the subtitle.",
        ])


    def test_markdown_to_blocks_preserve_single_newlines(self):
        markdown = "Line one\nLine two\nLine three\n\nNext block"
        self.assertEqual(markdown_to_blocks(markdown), [
            "Line one\nLine two\nLine three",
            "Next block",
        ])
class test_block_to_block_type(unittest.TestCase):

# HEADINGS

    def test_heading_level_1(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )


    def test_heading_level_6(self):
        self.assertEqual(
            block_to_block_type("###### Heading"),
            BlockType.HEADING,
        )


    def test_heading_level_7_invalid(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH,
        )


    def test_heading_without_space(self):
        self.assertEqual(
            block_to_block_type("##Heading"),
            BlockType.PARAGRAPH,
        )


    def test_heading_with_empty_text(self):
        self.assertEqual(
            block_to_block_type("### "),
            BlockType.HEADING,
        )


    # CODE BLOCKS

    def test_code_block(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"),
            BlockType.CODE,
        )


    def test_code_block_multiline(self):
        self.assertEqual(
            block_to_block_type("```\nline 1\nline 2\n```"),
            BlockType.CODE,
        )


    def test_code_block_without_newline(self):
        self.assertEqual(
            block_to_block_type("```print('hello')```"),
            BlockType.PARAGRAPH,
        )


    def test_code_block_missing_closing_backticks(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')"),
            BlockType.PARAGRAPH,
        )


    # QUOTES

    def test_quote_single_line(self):
        self.assertEqual(
            block_to_block_type("> Quote"),
            BlockType.QUOTE,
        )


    def test_quote_multiline(self):
        self.assertEqual(
            block_to_block_type("> First\n> Second\n> Third"),
            BlockType.QUOTE,
        )


    def test_quote_without_space(self):
        self.assertEqual(
            block_to_block_type(">Quote"),
            BlockType.QUOTE,
        )


    def test_quote_invalid_second_line(self):
        self.assertEqual(
            block_to_block_type("> First\nSecond"),
            BlockType.PARAGRAPH,
        )


    # UNORDERED LISTS

    def test_unordered_list_single_item(self):
        self.assertEqual(
            block_to_block_type("- First"),
            BlockType.UNORDERED_LIST,
        )


    def test_unordered_list_multiline(self):
        self.assertEqual(
            block_to_block_type("- First\n- Second\n- Third"),
            BlockType.UNORDERED_LIST,
        )


    def test_unordered_list_missing_space(self):
        self.assertEqual(
            block_to_block_type("-First"),
            BlockType.PARAGRAPH,
        )


    def test_unordered_list_invalid_middle_item(self):
        self.assertEqual(
            block_to_block_type("- First\nSecond\n- Third"),
            BlockType.PARAGRAPH,
        )


    # ORDERED LISTS

    def test_ordered_list_single_item(self):
        self.assertEqual(
            block_to_block_type("1. First"),
            BlockType.ORDERED_LIST,
        )


    def test_ordered_list_multiline(self):
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\n3. Third"),
            BlockType.ORDERED_LIST,
        )


    def test_ordered_list_wrong_start(self):
        self.assertEqual(
            block_to_block_type("2. First\n3. Second"),
            BlockType.PARAGRAPH,
        )


    def test_ordered_list_skipped_number(self):
        self.assertEqual(
            block_to_block_type("1. First\n3. Third"),
            BlockType.PARAGRAPH,
        )


    def test_ordered_list_repeated_number(self):
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\n2. Again"),
            BlockType.PARAGRAPH,
        )


    # PARAGRAPHS

    def test_plain_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is an ordinary paragraph."),
            BlockType.PARAGRAPH,
        )


    def test_paragraph_with_inline_markdown(self):
        self.assertEqual(
            block_to_block_type("Some **bold** and _italic_ text."),
            BlockType.PARAGRAPH,
        )


    # AUXILIARY FUNCTION

    def test_invalid_helper_type(self):
        with self.assertRaises(ValueError):
            is_list_or_quote("- First", "x")
