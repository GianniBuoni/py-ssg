def markdown_to_blocks(markdown):
    new_list = []
    inline_list = markdown.split("\n\n")
    for line in inline_list:
        if line != "":
            line = line.strip()
            new_list.append(line)
    return new_list
