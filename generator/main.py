import os
import glob
import json
import shutil
import argparse
from PIL import Image
import markdown2
import numpy as np
import re

from embedding import embed_with_clip, reduce_to_3d

def clear_output_dir(output_dir):
    content_dir = os.path.join(output_dir, 'content')
    nodes_dir = os.path.join(output_dir, 'nodes')
    nodes_json_file = os.path.join(output_dir, 'nodes.json')

    # Clear content of the content directory
    if os.path.exists(content_dir):
        for filename in os.listdir(content_dir):
            file_path = os.path.join(content_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(content_dir)

    # Clear content of the nodes directory
    if os.path.exists(nodes_dir):
        for filename in os.listdir(nodes_dir):
            file_path = os.path.join(nodes_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(nodes_dir)

    # Delete nodes.json file if it exists
    if os.path.exists(nodes_json_file):
        os.remove(nodes_json_file)

def load_markdown_files(input_path):
    md_files = []
    md_contents = []
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    md_contents.append(f.read())
    return md_files, md_contents

def load_images(path):
    files = glob.glob(os.path.join(path, "*.png")) + glob.glob(os.path.join(path, "*.jpg"))
    images = [Image.open(file) for file in files]
    print(f"Loaded {len(files)} images from {path}")
    return files, images

def extract_image_metadata(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        file_size = os.path.getsize(image_path)
    return {
        'width': width,
        'height': height,
        'file_size': file_size
    }

def save_image_files(img_files, output_dir):
    for img_file in img_files:
        shutil.copy(img_file, os.path.join(output_dir, 'content'))

def save_markdown_to_html(md_files, md_data, output_dir):
    for md_file, data in zip(md_files, md_data):
        html_content = markdown2.markdown(data['processed_content'], extras=["fenced-code-blocks", "tables", "cuddled-lists", "footnotes", "toc", "metadata", "code-friendly", "strike", "admonitions", "task_list"])
        output_file = os.path.join(output_dir, 'nodes', os.path.basename(md_file).replace('.md', '.html'))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

def process_md(content):
    # Extract YAML metadata block
    yaml_metadata = {}
    yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    yaml_match = yaml_pattern.match(content)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        yaml_metadata = yaml.safe_load(yaml_content)
        # Remove YAML metadata block from content
        content = content[yaml_match.end():]

    # Extract tags from metadata
    metadata_tags = set(yaml_metadata.get('tags', []))

    # Extract tags from content
    tag_pattern = re.compile(r'#(\w+[-_\/]?\w*)')
    content_tags = set(tag_pattern.findall(content))

    # Combine tags
    tags = list(metadata_tags.union(content_tags))

    # Extract links and images
    link_pattern = re.compile(r'!\[\[([^|\]]+)(?:\|([^\]]+))?\]\]|\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')
    links = []
    images = []

    def replace_links_and_images(match):
        if match.group(1):  # This is an image
            src = match.group(1)
            alt = match.group(2) if match.group(2) else src
            images.append(src)
            links.append(src)
            return f'![{alt}](/content/{src})'
        else:  # This is a link
            page = match.group(3)
            alias = match.group(4) if match.group(4) else page
            links.append(page)
            return f'[{alias}](/?node={page})'

    # Convert links and images
    content = re.sub(link_pattern, replace_links_and_images, content)

    # Add links and tags to metadata
    yaml_metadata['links'] = links
    yaml_metadata['tags'] = tags

    return {
        'metadata': yaml_metadata,
        'tags': tags,
        'links': links,
        'images': images,
        'processed_content': content
    }

def generate_metadata_file(md_files, md_data, img_files, reduced_embeddings, output_dir):
    metadata = {}

    for i, (md_file, data) in enumerate(zip(md_files, md_data)):
        metadata[os.path.basename(md_file)] = {
            'embedding': reduced_embeddings[i].tolist(),
            'filetype': 'markdown',
            'metadata': data['metadata'],
            'path': f'/nodes/{os.path.basename(md_file).replace(".md", ".html")}',
            'decorativePath': f'/nodes/{os.path.basename(md_file)}',
        }

    for i, img_file in enumerate(img_files):
        img_metadata = extract_image_metadata(img_file)
        metadata[os.path.basename(img_file)] = {
            'embedding': reduced_embeddings[len(md_files) + len(img_files) + i].tolist(),
            'filetype': 'image',
            'metadata': img_metadata,
            'path': f'/content/{os.path.basename(img_file)}',
            'decorativePath':  f'/nodes/{os.path.basename(img_file)}',
        }

    with open(os.path.join(output_dir, 'nodes.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

def main(input_path, output_dir, reduction_method):
    clear_output_dir(output_dir)

    md_files, md_contents = load_markdown_files(input_path)
    img_files, images = load_images(input_path)

    md_data = [process_md(content) for content in md_contents]
    print(md_data)

    all_texts = [datum['processed_content'] for datum in md_data]
    all_texts += [""] * len(images)  # Add image captions later?
    
    text_embeddings, image_embeddings = embed_with_clip(all_texts, images)
    
    save_image_files(img_files, output_dir)
    save_markdown_to_html(md_files, md_data, output_dir)

    reduced_embeddings = reduce_to_3d(np.vstack((text_embeddings, image_embeddings)), method=reduction_method)

    generate_metadata_file(md_files, md_data, img_files, reduced_embeddings, output_dir)

# Run the main function with arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process markdown and image content.")
    parser.add_argument("input_path", type=str, help="Path to the input content directory.")
    parser.add_argument("output_dir", type=str, help="Path to the output directory.")
    parser.add_argument("--reduction_method", type=str, default="pca", choices=["pca", "tsne", "umap", "isomap"],
                        help="Dimensionality reduction method to use.")
    args = parser.parse_args()
    main(args.input_path, args.output_dir, args.reduction_method)
