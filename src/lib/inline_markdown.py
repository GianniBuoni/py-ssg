from lib.textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        
        # check if sections list has an even number
        # a split with valid markdown should only return a list with an odd length
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown: delimiter not closed")
        for i in range(len(sections)):
            # skip empty strings
            if sections[i] == "":
                continue
            # odd indexes are the ones that should be changed
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes) -> list:
    new_nodes = []
    for node in old_nodes:
        original_text = node.text

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # check if node to process has any images
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid Markdown: image not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(image[0], TextType.IMAGE, image[1])
            )
            # reassign original_text to process a shorter string in each iteration
            original_text = sections[1]
            
        # check value of remaining string
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes) -> list:
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # check if node to process has any images
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid Markdown: link not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(link[0], TextType.LINK, link[1])
            )
            # reassign original_text to process a shorter string in each iteration
            original_text = sections[1]
            
        # check value of remaining string
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    print(new_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
