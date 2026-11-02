from textnode import TextType, TextNode
from enum import Enum
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    text_nodes = []

    for text in old_nodes:
        if text.text_type != TextType.TEXT:
            text_nodes.append(text)
        else:
            parts = text.text.split(delimiter)

            if len(parts) % 2 == 0:
                raise ValueError("ERROR: Unclosed delimiter")

            for index, item in enumerate(parts):
                if not item:
                    continue

                if index % 2 != 0:
                    node = TextNode(item, text_type)
                else:
                    node = TextNode(item, TextType.TEXT)

                text_nodes.append(node)

    return text_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text:str) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    text_nodes =[]
    for node in old_nodes:
            if node.text_type != TextType.TEXT:
                text_nodes.append(node)
            else:
                images = extract_markdown_images(node.text)
                if images == []:
                    text_nodes.append(node)
                else:   
                    remaining_text = node.text
                    for image in images:
                        other_parts = remaining_text.split(f"![{image[0]}]({image[1]})",1)
                        bfr_text = other_parts[0]
                        remaining_text = other_parts[1]
                        if bfr_text:
                            text_nodes.append(TextNode(bfr_text,TextType.TEXT))
                        text_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    if remaining_text:           
                        text_nodes.append(TextNode(remaining_text,TextType.TEXT))
    return text_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    text_nodes =[]
    for node in old_nodes:
            if node.text_type != TextType.TEXT:
                text_nodes.append(node)
            else:
                links = extract_markdown_links(node.text)
                if links == []:
                    text_nodes.append(node)
                else:   
                    remaining_text = node.text
                    for link in links:
                        other_parts = remaining_text.split(f"[{link[0]}]({link[1]})",1)
                        bfr_text = other_parts[0]
                        remaining_text = other_parts[1]
                        if bfr_text:
                            text_nodes.append(TextNode(bfr_text,TextType.TEXT))
                        text_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    if remaining_text:           
                        text_nodes.append(TextNode(remaining_text,TextType.TEXT))
    return text_nodes

def text_to_textnodes(text:str) -> list[TextNode]:
    input_list = [TextNode(text, TextType.TEXT)]
    text_nodes_list = split_nodes_delimiter(input_list,"`",TextType.CODE)
    text_nodes_list = split_nodes_delimiter(text_nodes_list, "**", TextType.BOLD)
    text_nodes_list = split_nodes_delimiter(text_nodes_list, "_", TextType.ITALIC)
    text_nodes_list = split_nodes_image(text_nodes_list)
    text_nodes_list = split_nodes_link(text_nodes_list)
    return text_nodes_list