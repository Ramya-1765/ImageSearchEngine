import torch
import clip
from PIL import Image
import faiss
import pandas as pd
import os
import json
import numpy as np
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def encode_image(image_path_or_obj):
    if isinstance(image_path_or_obj, str):
        image = preprocess(Image.open(image_path_or_obj)).unsqueeze(0).to(device)
    else:
        image = preprocess(image_path_or_obj).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(image).cpu().numpy()
    return embedding / np.linalg.norm(embedding)

def encode_text(text):
    token = clip.tokenize([text]).to(device)
    with torch.no_grad():
        embedding = model.encode_text(token).cpu().numpy()
    return embedding / np.linalg.norm(embedding)

def build_faiss_index(csv_path="data.csv", index_path="vector_store/faiss_index.bin", metadata_path="vector_store/metadata.json"):
    df = pd.read_csv(csv_path)
    image_embeddings = []
    metadata = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        image_path = row['image_path']
        full_path = os.path.join("static", image_path)
        if os.path.exists(full_path):
            emb = encode_image(full_path)
            image_embeddings.append(emb)
            metadata.append(full_path)

    image_embeddings = np.vstack(image_embeddings).astype("float32")
    index = faiss.IndexFlatL2(image_embeddings.shape[1])
    index.add(image_embeddings)

    faiss.write_index(index, index_path)
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)

def load_faiss_index(index_path="vector_store/faiss_index.bin", metadata_path="vector_store/metadata.json"):
    index = faiss.read_index(index_path)
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    return index, metadata

def search_similar(query_embedding, index, metadata, k=4):
    D, I = index.search(query_embedding.astype("float32"), k)
    return [metadata[i] for i in I[0]]
