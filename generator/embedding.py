import torch
from transformers import CLIPModel, CLIPProcessor
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, Isomap
import umap
import numpy as np

# Embedding function using CLIP
def embed_with_clip(texts, images):
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    print("Model and processor loaded to device:", device)

    # Embed texts
    text_inputs = processor(text=texts, return_tensors="pt", padding=True, truncation=True).to(device)
    text_embeddings = model.get_text_features(**text_inputs)
    print(f"Text embeddings computed for {len(texts)} texts")

    # Embed images
    image_inputs = processor(images=images, return_tensors="pt").to(device)
    image_embeddings = model.get_image_features(**image_inputs)
    print(f"Image embeddings computed for {len(images)} images")

    return text_embeddings.cpu().detach().numpy(), image_embeddings.cpu().detach().numpy()

# Dimensionality reduction to 3D
def reduce_to_3d(embeddings, method="pca"):
    if method == "pca":
        reducer = PCA(n_components=3)
        reduced_embeddings = reducer.fit_transform(embeddings)
        print("Reduced embeddings to 3D space using PCA")
    elif method == "tsne":
        reducer = TSNE(n_components=3, perplexity=min(30, len(embeddings)-1), n_iter=300)
        reduced_embeddings = reducer.fit_transform(embeddings)
        print("Reduced embeddings to 3D space using t-SNE")
    elif method == "umap":
        reducer = umap.UMAP(n_components=3)
        reduced_embeddings = reducer.fit_transform(embeddings)
        print("Reduced embeddings to 3D space using UMAP")
    elif method == "isomap":
        reducer = Isomap(n_components=3)
        reduced_embeddings = reducer.fit_transform(embeddings)
        print("Reduced embeddings to 3D space using Isomap")
    else:
        raise ValueError(f"Unsupported dimensionality reduction method: {method}")
    return reduced_embeddings
