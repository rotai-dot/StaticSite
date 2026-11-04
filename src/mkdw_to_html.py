from markdown_block  import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from text_to_TextNodes import text_to_textnodes

def num_of_headings(text:str)->int:
    if text.startswith("######"):
        return 6
    elif text.startswith("#####"):
        return 5
    elif text.startswith("####"):
        return 4
    elif text.startswith("###"):
        return 3
    elif text.startswith("##"):
        return 2
    elif text.startswith("#"):
        return 1
    else:
        raise ValueError("ERROR: argument not supported")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)

    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children



def markdown_to_html_node(markdown: str)-> HTMLNode:
    text_blocks = markdown_to_blocks(markdown)
    blocks_list = []
    for block in text_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                children = text_to_children(text)
                node = ParentNode("p",children)
                blocks_list.append(node)
            case BlockType.HEADING:
                headings = num_of_headings(block)
                text = block[(headings+1):]
                children = text_to_children(text)
                node = ParentNode(f"h{headings}", children)
                blocks_list.append(node)
            case BlockType.QUOTE:
                lines = block.split("\n")
                cleaned = [line[1:].removeprefix(" ") for line in lines]
                text = "\n".join(cleaned)
                children = text_to_children(text)
                node = ParentNode("blockquote", children)
                blocks_list.append(node)
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                cleaned = [line[1:].removeprefix(" ") for line in lines]
                li_nodes = []
                for line in cleaned:
                    children = text_to_children(line)
                    li = ParentNode("li", children)
                    li_nodes.append(li)
                node = ParentNode("ul",li_nodes)
                blocks_list.append(node)
            case BlockType.ORDERED_LIST:                
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    text = line.split(" ", 1)[1]
                    children = text_to_children(text)
                    li = ParentNode("li", children)
                    li_nodes.append(li)
                node = ParentNode("ol",li_nodes)
                blocks_list.append(node)
            case BlockType.CODE:
                text = block[4:-3]
                text_node = TextNode(text,TextType.TEXT)
                child = text_node_to_html_node(text_node)
                parent_node = ParentNode("code", [child])
                grand_parent_node = ParentNode("pre", [parent_node])
                blocks_list.append(grand_parent_node)
    return ParentNode("div", blocks_list)

                


