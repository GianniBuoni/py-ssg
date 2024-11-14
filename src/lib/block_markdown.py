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

def maarkdown_to_htmlnode(doc):
    # convert markdown to list of blocks: string -> list of strings
    block_list = markdown_to_blocks(doc)

    # loop through each block (string)
    for block in block_list:
        # determine block type: string -> BlockType string
        block_type = block_to_block_type(block)

    # create HTMLNode: string -> HTMLNode(
        # BlockType string -> block tag
        # value = None
        # children -> list of strings
        # use text to textnode on each child:
            # list of strings -> list of lists of textnodes
    #)

def blocknode_to_htmlnode(block, block_type):
    match (block_type):
        case (BlockType.HEADING.value):
            return ()

def markdown_to_blocks(markdown):
    new_list = []
    inline_list = markdown.split("\n\n")
    for line in inline_list:
        if line != "":
            line = line.strip()
            new_list.append(line)
    return new_list

def block_to_block_type(block_text) -> str:
    if re.fullmatch(r"^#{1,6}\s.+$", block_text): return BlockType.HEADING.value
    if re.fullmatch(r"`{3}(.+\s)+`{3}", block_text): return BlockType.CODE.value
    if re.fullmatch(r"(>\s.+\n?)+", block_text): return BlockType.QUOTE.value
    if re.fullmatch(r"(-?\*?\s.+\n?)+", block_text): return BlockType.UNORDERED.value
    if re.fullmatch(r"(\d\.\s.+\n?)+", block_text): return BlockType.ORDERED.value
    return BlockType.PARAGRAPH.value


def extract_node_children(text: str, delimiter: str) -> list[LeafNode]:
    children = []
    text_list: list[str] = (text.split("\n"))
    for substring in text_list:
        # regex substring replacement
        substring = re.sub(delimiter, "", substring)
        working_list = text_to_textnodes(substring)
        working_list = list(map(
            lambda x: text_node_to_html_node(x),
            working_list
        ))
        children.extend(working_list)
    return children

def heading_node(text: str) -> ParentNode:
    children = extract_node_children(text, r"^#{1,6}\s")
    heading_tag = f"h{len(re.findall(r'#', text))}"
    return ParentNode(heading_tag, children)

def code_node(text: str) -> ParentNode:
    children = extract_node_children(text, r"`{3}")
    children = list(map(
        lambda x: ParentNode("pre", [x]),
        children
    ))
    return ParentNode("code", children)

def quote_node(text: str) -> ParentNode:
    children = extract_node_children(text, r"^>\s")
    return ParentNode("quoteblock",children)

def unordered_node(text: str) -> ParentNode:
    children = extract_node_children(text, r"^-?\*?\s")
    children = list(map(
        lambda x: ParentNode("li", [x]),
        children
    ))
    return ParentNode("ul", children)

def ordered_node(text: str) -> ParentNode:
    children = extract_node_children(text, r"^\d\.\s")
    children = list(map(
        lambda x: ParentNode("li", [x]),
        children
    ))
    return ParentNode("ol", children)

def paragraph_node(text: str) -> ParentNode:
    children = extract_node_children(text, r"")
    return ParentNode("p", children)
