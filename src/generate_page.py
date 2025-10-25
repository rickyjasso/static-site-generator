from block import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.split("\n\n")
    for line in lines:
        if line.startswith("#"):
            return line[1:].strip()
    raise Exception("markdown does not have an h1")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path)
    md_content = md_file.read()
    md_file.close()
    
    t_file = open(template_path)
    t_content = t_file.read()
    t_file.close()

    html_node = markdown_to_html_node(md_content)
    html_string = html_node.to_html()

    title = extract_title(md_content)

    html_page = t_content.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_string)
    
    file_dir = os.path.abspath(os.path.join(dest_path, ".."))
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(dest_path, "w") as file:
        file.write(html_page)
    print(f"File written succesfully to: {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    pass
