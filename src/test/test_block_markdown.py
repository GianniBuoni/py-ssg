from unittest import TestCase, main
import unittest

from lib.block_markdown import block_to_block_type, markdown_to_blocks

class TestBlockMarkdown(TestCase):
    def test_split_blocks(self):
        markdown = (
            "# This is a heading\n\n"
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
            "* This is the first list item in a list block\n"
            "* This is a list item\n"
            "* This is another list item\n"
        ) 

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]

        self.assertListEqual(
            markdown_to_blocks(markdown),
            expected
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type(self):
        block = (
            "# Heading 1"
        )
        self.assertEqual(block_to_block_type(block), "heading")

        block = (
            "```py\ncode block\n```"
        )
        self.assertEqual(block_to_block_type(block), "code")

        block = "> quote one\n> quote two"
        self.assertEqual(block_to_block_type(block), "quote")

        block = (
            "- bullet\n"
            "* a different bullet"
        )
        self.assertEqual(block_to_block_type(block), "unordered list")

        block = (
            "1. item 1\n2. item 2"
        )
        self.assertEqual(block_to_block_type(block), "ordered list")

if __name__ == "__main__":
    main()