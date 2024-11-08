from lib.textnode import TextType, TextNode

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
            raise ValueError("Invalid Markdown")
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
