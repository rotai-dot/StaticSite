from htmlnode import HTMLNode, LeafNode, ParentNode
from mkdw_to_html import markdown_to_html_node
import os

def extract_title(markdown:str)->str:
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            title = stripped_line[1:].strip()
            return title
    raise ValueError("Title not found")


def generate_page(from_path:str, template_path:str, dest_path:str, base_path:str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        read = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_object = markdown_to_html_node(read)
    html_str = html_object.to_html()
    title = extract_title(read)
    to_write = template.replace("{{ Title }}", title)
    to_write = to_write.replace("{{ Content }}", html_str) 
    to_write = to_write.replace('href="/',f'href="{base_path}')
    to_write = to_write.replace('src="/',f'src="{base_path}') 
    directory = os.path.dirname(dest_path)
    if directory != "":
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(to_write)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path:str)-> None:
    list = os.listdir(dir_path_content)
    for dir in list:
        updated_file_path = os.path.join(dir_path_content, dir)
        updated_dest_path = os.path.join(dest_dir_path, dir)
        if os.path.isfile(updated_file_path) and updated_dest_path.endswith(".md"):
            tuple = os.path.splitext(updated_dest_path)
            mkdw_dest_path = tuple[0] + ".html"
            generate_page(updated_file_path, template_path, mkdw_dest_path, base_path)
        elif os.path.isdir(updated_file_path):
            generate_pages_recursive(updated_file_path, template_path, updated_dest_path, base_path)
