import re
from enum import Enum

from lib.htmlnode import LeafNode, ParentNode
from lib.inline_markdown import text_to_textnodes
from lib.textnode import text_node_to_html_node

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered list"
    ORDERED = "ordered list"
    PARAGRAPH = "paragraph"

def markdown_to_htmlnode(doc) -> list[ParentNode]:
    children = []
    block_list = markdown_to_blocks(doc)

    for block in block_list:
        block_type = block_to_block_type(block)
        html_node = block_type_to_htmlnode(block, block_type)
        children.append(html_node)

    return children

def markdown_to_blocks(markdown):
    new_list = []
    inline_list = markdown.split("\n\n")
    for line in inline_list:
        if line != "":
            line = line.strip()
            new_list.append(line)
    return new_list

def block_to_block_type(block_text) -> BlockType:
    if re.fullmatch(r"^#{1,6}\s.+$", block_text): return BlockType.HEADING
    if re.fullmatch(r"`{3}(.*\s)+`{3}", block_text): return BlockType.CODE
    if re.fullmatch(r"(>\s.+\n?)+", block_text): return BlockType.QUOTE
    if re.fullmatch(r"(-?\*?\s.+\n?)+", block_text): return BlockType.UNORDERED
    if re.fullmatch(r"(\d\.\s.+\n?)+", block_text): return BlockType.ORDERED
    return BlockType.PARAGRAPH

def block_type_to_htmlnode(block: str, block_type: BlockType) -> ParentNode:
    match (block_type):
        case (BlockType.HEADING):
            return heading_node(block)
        case (BlockType.CODE):
            return code_node(block)
        case (BlockType.QUOTE):
            return quote_node(block)
        case (BlockType.UNORDERED):
            return unordered_node(block)
        case (BlockType.ORDERED):
            return ordered_node(block)
        case _:
            return paragraph_node(block) 

def extract_node(text: str, delimiter: str) -> list[list[LeafNode]]:
    children = []
    text_list: list[str] = (text.split("\n"))
    for substring in text_list:
        # regex remove symbols and white space
        substring = re.sub(delimiter, "", substring)

        # raw strings turned into flat list of text nodes
        working_list = text_to_textnodes(substring)

        # turn all text nodes into flat list of leaf nodes
        working_list = list(map(
            lambda x: text_node_to_html_node(x),
            working_list
        ))

        children.append(working_list)

    return children


def heading_node(text: str) -> ParentNode:
    children = extract_node(text, r"^#{1,6}\s")

    # flatten list
    children = [x for xs in children for x in xs]
    
    heading_tag = f"h{len(re.findall(r'#', text))}"
    return ParentNode(heading_tag, children)

def code_node(text: str) -> ParentNode:
    children = extract_node(text, r"`{3}")

    # flatten list
    children = [x for xs in children for x in xs]

    children = list(map(
        lambda x: LeafNode(None, f"{x.value}\n"),
        children
    ))

    return (ParentNode("pre", [
        ParentNode("code", children)
    ]))

def quote_node(text: str) -> ParentNode:
    children = extract_node(text, r"^>\s")

    # flatten list
    children = [x for xs in children for x in xs]

    return ParentNode("blockquote",children)

def unordered_node(text: str) -> ParentNode:
    children = extract_node(text, r"^-?\*?\s")
    children = list(map(
        lambda x: ParentNode("li", x),
        children
    ))
    return ParentNode("ul", children)

def ordered_node(text: str) -> ParentNode:
    children = extract_node(text, r"^\d\.\s")
    children = list(map(
        lambda x: ParentNode("li", x),
        children
    ))
    return ParentNode("ol", children)

def paragraph_node(text: str) -> ParentNode:
    children = extract_node(text, r"")

    # flatten list
    children = [x for xs in children for x in xs]

    return ParentNode("p", children)
