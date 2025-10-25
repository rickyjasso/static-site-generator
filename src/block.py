from enum import Enum
from htmlnode import HTMLNode, ParentNode 
import re
from inline import TextNode, text_to_textnodes
from textnode import text_node_to_html_node, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "unordered list",
    ORDERED_LIST = "ordered list"

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def create_heading_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN_TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(create_heading_html_node(block))
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(ulist_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(olist_to_html_node(block))
            case _:
                raise ValueError("invalid block type")
    return ParentNode("div", children, None)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final = []
    for block in blocks:
        new_block = block.strip()
        if len(block) != 0 or block != "":
            final.append(new_block)
    return final

def block_to_block_type(block):
    is_quote = True
    is_ulist = True
    is_olist = True
    olist_number = 1
    split_lines = block.splitlines()
    #Code block
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    #Heading
    elif re.search(r"^#{1,6} \w*\S", block):
        return BlockType.HEADING
    #Quote
    if is_quote:
        for line in split_lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote == True:
            return BlockType.QUOTE
    #Ulist
    if is_ulist:
        for line in split_lines:
            if not line.startswith("- "):
                is_ulist = False
                break
        if is_ulist:
            return BlockType.UNORDERED_LIST
    #OList
    if is_olist:
        for line in split_lines:
            if not line.startswith(f"{olist_number}. "):
                is_olist = False
                break
            olist_number+=1
        if is_olist:
            return BlockType.ORDERED_LIST
    #Paragraph
    return BlockType.PARAGRAPH
