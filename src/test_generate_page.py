import unittest
import os
from generate_page import extract_title, generate_page

class test_extrac_title(unittest.TestCase):
    def test_extract_title_basic(self):
        self.assertEqual(
            extract_title("# Hello"),
            "Hello",
        )


    def test_extract_title_not_first_line(self):
        markdown = "Introduction\n\n# Main Title\n\nParagraph"
        self.assertEqual(
            extract_title(markdown),
            "Main Title",
        )


    def test_extract_title_strip_whitespace(self):
        self.assertEqual(
            extract_title("#   Hello   "),
            "Hello",
        )

