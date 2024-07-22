import os
import glob
import numpy as np
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# Function to load and embed markdown files
def load_markdown_files(path):
    files = glob.glob(os.path.join(path, "*.md"))
    contents = [open(file, 'r').read() for file in files]
    return files, contents

# Function to load images
def load_images(path):
    files = glob.glob(os.path.join(path, "*.png")) + glob.glob(os.path.join(path, "*.jpg"))
    images = [Image.open(file) for file in files]
    return files, images

# Embedding function using CLIP
def embed_with_clip(texts, images):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    # Embed texts
    text_inputs = processor(text=texts, return_tensors="pt", padding=True, truncation=True).to(device)
    text_embeddings = model.get_text_features(**text_inputs)

    # Embed images
    image_inputs = processor(images=images, return_tensors="pt").to(device)
    image_embeddings = model.get_image_features(**image_inputs)

    # Combine embeddings
    all_embeddings = torch.cat([text_embeddings, image_embeddings], dim=0)
    return all_embeddings.cpu().detach().numpy()

# Dimensionality reduction to 3D
def reduce_to_3d(embeddings):
    pca = PCA(n_components=3)
    reduced_embeddings = pca.fit_transform(embeddings)
    return reduced_embeddings

# Main function to create 3D plot
def create_3d_plot(path):
    print('loading content...')
    md_files, md_contents = load_markdown_files(path)
    img_files, images = load_images(path)

    all_files = md_files + img_files
    all_texts = md_contents + [""] * len(images)  # Empty texts for images

    print('calculating embeddings...')    
    all_embeddings = embed_with_clip(all_texts, images)

    print('dimensionality reduction...')
    reduced_embeddings = reduce_to_3d(all_embeddings)

    md_points = reduced_embeddings[:len(md_files)]
    img_points = reduced_embeddings[len(md_files):]

    print('plotting...')
    trace_md = go.Scatter3d(
        x=md_points[:, 0], y=md_points[:, 1], z=md_points[:, 2],
        mode='markers',
        marker=dict(size=5, color='blue'),
        text=md_files,
        name='Markdown Files'
    )
    
    trace_img = go.Scatter3d(
        x=img_points[:, 0], y=img_points[:, 1], z=img_points[:, 2],
        mode='markers',
        marker=dict(size=5, color='red'),
        text=img_files,
        name='Images'
    )
    
    layout = go.Layout(
        title='3D Visualization of Markdown Files and Images',
        scene=dict(
            xaxis_title='PCA1',
            yaxis_title='PCA2',
            zaxis_title='PCA3'
        )
    )
    
    fig = go.Figure(data=[trace_md, trace_img], layout=layout)
    fig.show()

# Run the main function
create_3d_plot('content')
