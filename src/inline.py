
from textnode import TextType, TextNode
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("invalid, format needs a closing delimiter")
            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(parts[i], TextType.PLAIN_TEXT))
                else:
                    split_nodes.append(TextNode(parts[i], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        images_data = extract_markdown_images(node.text)
        if len(images_data) == 0:
            new_nodes.append(node)
        else:
            split_nodes = []
            remainder = node.text
            for i in range(len(images_data)):
                img_alt = images_data[i][0]
                img_url = images_data[i][1]
                before, remainder = remainder.split(f"![{img_alt}]({img_url})", 1)
                if len(before) != 0:
                    split_nodes.append(TextNode(text=before, text_type=TextType.PLAIN_TEXT))
                split_nodes.append(TextNode(text=img_alt, text_type=TextType.IMAGE, url=img_url))
            if len(remainder) != 0:
                split_nodes.append(TextNode(text=remainder, text_type=TextType.PLAIN_TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        links_data = extract_markdown_links(node.text)
        if len(links_data) == 0:
            new_nodes.append(node)
        else:
            split_nodes = []
            remainder = node.text
            for i in range(len(links_data)):
                link_text = links_data[i][0]
                link_url = links_data[i][1]
                before, remainder = remainder.split(f"[{link_text}]({link_url})", 1)
                if len(before) != 0:
                    split_nodes.append(TextNode(text=before, text_type=TextType.PLAIN_TEXT))
                split_nodes.append(TextNode(text=link_text, text_type=TextType.LINK, url=link_url))
            if len(remainder) != 0:
                split_nodes.append(TextNode(text=remainder, text_type=TextType.PLAIN_TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

