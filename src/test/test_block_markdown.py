from unittest import TestCase, main

from lib.block_markdown import (
    BlockType,
    block_to_block_type,
    code_node, heading_node,
    markdown_to_blocks,
    markdown_to_htmlnode,
    ordered_node,
    paragraph_node,
    quote_node,
    unordered_node
    )
from lib.htmlnode import LeafNode, ParentNode

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
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = (
            "```py\ncode block\n```"
        )
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = '```\nfunc main(){\n    fmt.Println("Hello, World!")\n}\n```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "> quote one\n> quote two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = (
            "- bullet\n"
            "* a different bullet"
        )
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED)

        block = (
            "1. item 1\n2. item 2"
        )
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)

    def test_block_to_html_node(self):
        text = "### Heading"
        self.assertEqual(
            heading_node(text).tag,
            "h3"
        )
        self.assertEqual(
            heading_node(text).children,
            [LeafNode(None, "Heading")]
        )

        text = "```\ncode\ncode block\n```"
        self.assertEqual(
            code_node(text).children,
            [
                ParentNode("pre", [LeafNode(None, "code")]),
                ParentNode("pre", [LeafNode(None, "code block")])
            ]
        )

        text = "> quote 1\n> quote 2"
        self.assertEqual(
            quote_node(text).children,
            [LeafNode(None, "quote 1"), LeafNode(None, "quote 2")]
        )

        text = "- list item\n- list item 2"
        self.assertEqual(
            unordered_node(text).children,
            [
                ParentNode("li", [LeafNode(None, "list item")]),
                ParentNode("li",[LeafNode(None, "list item 2")])
            ]
        )

        text = "1. list item\n2. list item 2"
        self.assertEqual(
            ordered_node(text).children,
            [
                ParentNode("li", [LeafNode(None, "list item")]),
                ParentNode("li",[LeafNode(None, "list item 2")])
            ]
        )

        text = "this has some *italic* and **bold** text"
        self.assertEqual(
            paragraph_node(text).children,
            [
                LeafNode(None, "this has some "),
                LeafNode("i", "italic"),
                LeafNode(None, " and "),
                LeafNode("b", "bold"),
                LeafNode(None, " text")
            ]
        )

        text = """
# Heading

This is a paragraph.

- Unordered list item.
- Unordered list item.

[Link to somewhere.](https://google.com)

![image](https://www.boot.dev/_nuxt/5.B754pGI7.png)

This has some *italic* and **bold** text.

```
func main(){
    fmt.Println("Hello, World!")
}
```
"""
        self.assertEqual(
            markdown_to_htmlnode(text).children,
            [
                ParentNode("h1", [LeafNode(None, "Heading")]),
                ParentNode("p", [LeafNode(None, "This is a paragraph.")]),
                ParentNode("ul", [
                    ParentNode("li", [LeafNode(None, "Unordered list item.")]),
                    ParentNode("li",[LeafNode(None, "Unordered list item.")])
                ]),
                ParentNode("p", [
                    LeafNode("a", "Link to somewhere.", {
                        "href": "https://google.com"
                    })
                ]),
                ParentNode("p", [
                    LeafNode("img", "", {
                        "src": "https://www.boot.dev/_nuxt/5.B754pGI7.png",
                        "alt": "image"
                    })
                ]),
                ParentNode("p", [
                    LeafNode(None, "This has some "),
                    LeafNode("i", "italic"),
                    LeafNode(None, " and "),
                    LeafNode("b", "bold"),
                    LeafNode(None, " text.")
                ]),
                ParentNode("code", [
                        ParentNode("pre", [LeafNode(None, "func main(){")]),
                        ParentNode("pre", [LeafNode(None, '    fmt.Println("Hello, World!")')]),
                        ParentNode("pre", [LeafNode(None, "}")]),
                ])
            ]
        )


if __name__ == "__main__":
    main()
