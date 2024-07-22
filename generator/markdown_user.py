import os
import glob
import shutil
import re
import yaml
from PIL import Image
import markdown

# Function to clear output directory
def clear_output_dir(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    os.makedirs(os.path.join(output_dir, 'content'))
    os.makedirs(os.path.join(output_dir, 'nodes'))
    print(f"Cleared and created output directory structure at {output_dir}")

# Function to load and embed markdown files
def load_markdown_files(path):
    files = glob.glob(os.path.join(path, "*.md"))
    contents = [open(file, 'r').read() for file in files]
    print(f"Loaded {len(files)} markdown files from {path}")
    return files, contents

# Function to load images
def load_images(path):
    files = glob.glob(os.path.join(path, "*.png")) + glob.glob(os.path.join(path, "*.jpg"))
    images = [Image.open(file) for file in files]
    print(f"Loaded {len(files)} images from {path}")
    return files, images

# Function to extract metadata from markdown content
def extract_metadata(content):
    # Extract YAML metadata block
    yaml_block = re.search(r'---(.*?)---', content, re.DOTALL)
    yaml_data = {}
    if yaml_block:
        try:
            yaml_content = yaml_block.group(1)
            yaml_data = yaml.safe_load(yaml_content)
            content = content.replace(yaml_block.group(0), '')
        except Exception as e:
            yaml_data = {}
            print('failed to extract yaml_data:', str(e))

    if yaml_data is None:
        yaml_data = {}

    # Extract links and image links
    links = re.findall(r'!\[\[(.*?)\|?(.*?)\]\]|\[\[(.*?)\|?(.*?)\]\]', content)
    links = [link for group in links for link in group if link]

    # Extract tags
    tags = re.findall(r'#([a-zA-Z0-9_/-]+)', content)

    print(yaml_data)

    # Combine YAML tags with inline tags
    if 'tags' in yaml_data:
        yaml_data['tags'] = list(set(yaml_data['tags'] + tags))
    else:
        yaml_data['tags'] = tags

    metadata = {
        'links': links,
        'tags': yaml_data.get('tags', [])
    }
    yaml_data.pop('tags', None)
    metadata.update(yaml_data)
    
    return content, metadata

# Function to preprocess markdown content
def preprocess_markdown(content, link_map, image_map):
    # Convert Obsidian image links to standard Markdown image links
    def replace_image(match):
        src, alt = match.groups()
        if not alt:
            alt = src
        return f"![{alt}]({image_map.get(src, src)})"

    content = re.sub(r'!\[\[(.*?)\|?(.*?)\]\]', replace_image, content)
    
    # Convert Obsidian links to standard Markdown links
    def replace_link(match):
        link, alias = match.groups()
        if not alias:
            alias = link
        return f"[{alias}]({link_map.get(link, link)})"

    content = re.sub(r'\[\[(.*?)\|?(.*?)\]\]', replace_link, content)
    
    return content

# Function to generate HTML content
def generate_html(content, content_type):
    if content_type == 'markdown':
        html_content = markdown.markdown(content)
    else:
        html_content = f'<img src="content/{os.path.basename(content)}" alt="Image">'
    return html_content

# Function to copy images to content directory
def copy_images(files, output_dir):
    output_paths = []
    for file in files:
        filename = os.path.basename(file)
        dest = os.path.join(output_dir, 'content', filename)
        shutil.copy(file, dest)
        output_paths.append(dest)
    print(f"Copied {len(files)} images to {output_dir}/content")
    return output_paths

# Function to write HTML files
def write_html_files(files, contents, content_type, output_dir):
    paths = []
    for file, content in zip(files, contents):
        filename = os.path.splitext(os.path.basename(file))[0] + '.html'
        html_content = generate_html(content, content_type)
        path = os.path.join(output_dir, 'nodes', filename)
        with open(path, 'w') as f:
            f.write(html_content)
        paths.append(path)
    print(f"Generated HTML files for {len(files)} {content_type} contents")
    return paths
