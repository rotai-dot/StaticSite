from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"




def markdown_to_blocks(text:str)->list[str]:
    output = text.split("\n\n")
    blocks =[]
    for block in output:
        temp = block.strip()
        if temp:
            blocks.append(temp)
    return blocks


def is_list_or_quote(text: str, type:str)->bool:
    lines = text.split("\n")
    if type == "o":
        for index, line in enumerate(lines, start = 1):
            if not line.startswith(f"{index}. "):
                return False
        return True
    elif type == "q":
        for line in lines:
            if not line.startswith(">"):
                return False
        return True
    elif type == "u":
        for line in lines:
            if not line.startswith("- "):
                return False
        return True
    raise ValueError("ERROR: type of block not supported")
        

              

def block_to_block_type(block: str)->BlockType:
        if re.match(r"^#{1,6} ", block):
             return BlockType.HEADING
        elif block.startswith("```\n") and block.endswith("```"):
             return BlockType.CODE
        elif is_list_or_quote(block, "q"):
             return BlockType.QUOTE
        elif is_list_or_quote(block, "u"):
             return BlockType.UNORDERED_LIST
        elif is_list_or_quote(block, "o"):
             return BlockType.ORDERED_LIST
        else:
             return BlockType.PARAGRAPH
             
