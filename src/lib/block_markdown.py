import re
from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered list"
    ORDERED = "ordered list"
    PARAGRAPH = "paragraph"

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
