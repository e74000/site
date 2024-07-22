import re
import yaml

def process_md(content):
    # Extract YAML metadata block
    yaml_metadata = {}
    yaml_pattern = re.compile(r'^\n*---\n(.*?)\n---\n', re.DOTALL)
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
            return f'![{alt}](/content/{src})'
        else:  # This is a link
            page = match.group(3)
            alias = match.group(4) if match.group(4) else page
            links.append(page)
            return f'[{alias}](/?page={page})'

    # Convert links and images
    content = re.sub(link_pattern, replace_links_and_images, content)

    return {
        'metadata': yaml_metadata,
        'tags': tags,
        'links': links,
        'images': images,
        'processed_content': content
    }

# Example usage:
markdown_content = """---
tags:
  - yaml_tag1
  - yaml_tag2
other_data:
  - foo
  - bar
---

# Example Markdown

This is an example markdown file with some #tags and [[links|aliases]] and ![[images|alt text]].

#tags:
#tag_underscore
#tag-hyphen
#tag/slash

Invalid tags:
# tag
#tag+a

# Links:
[[page_name|alias]]
[[page_name]]

# Images:
![[image_src|alt]]
![[image_src]]
"""

result = process_md(markdown_content)
print(result)
