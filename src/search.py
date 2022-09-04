import numpy as np
import math
import pandas as pd
import torchvision
from cloudpathlib import CloudPath
from tqdm.notebook import tqdm
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image
import clip
from pathlib import Path



device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

text = '''
[rhackathon]
aws_access_key_id = AKIA3FLER3QPHGOGS7YD 
aws_secret_access_key = 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
region = us-east-1
'''
path = "awscli.ini"
with open(path, 'w') as f:
    f.write(text)


cp = CloudPath("s3://img-up123/images/")
cp.download_to("getter")

# Set the path to the photos
dataset_version = "lite"  # Use "lite" or "full"
photos_path = Path("getter")

# List all JPGs in the folder
photos_files = list(photos_path.glob("*.jpg"))

def compute_clip_features(photos_batch):
    photos = [Image.open(photo_file) for photo_file in photos_batch]
    photos_preprocessed = torch.stack(
        [preprocess(photo) for photo in photos]).to(device)
    with torch.no_grad():
        photos_features = model.encode_image(photos_preprocessed)
        photos_features /= photos_features.norm(dim=-1, keepdim=True)
    return photos_features.cpu().numpy()


batch_size = 8
features_path = Path("artifacts")
batches = math.ceil(len(photos_files) / batch_size)

for i in range(batches):
    print(f"Processing batch {i+1}/{batches}")

    batch_ids_path = features_path / f"{i:010d}.csv"
    batch_features_path = features_path / f"{i:010d}.npy"
    if not batch_features_path.exists():
        try:
            batch_files = photos_files[i*batch_size: (i+1)*batch_size]
            batch_features = compute_clip_features(batch_files)
            np.save(batch_features_path, batch_features)
            photo_ids = [photo_file.name.split(
                ".")[0] for photo_file in batch_files]
            photo_ids_data = pd.DataFrame(photo_ids, columns=['photo_id'])
            photo_ids_data.to_csv(batch_ids_path, index=False)
        except:
            print(f'Problem with batch {i}')


features_list = [np.load(features_file)
                 for features_file in sorted(features_path.glob("*.npy"))]

features = np.concatenate(features_list)
np.save(features_path / "features.npy", features)

photo_ids = pd.concat([pd.read_csv(ids_file)
                       for ids_file in sorted(features_path.glob("*.csv"))])
photo_ids.to_csv(features_path / "photo_ids.csv", index=False)


photo_ids = pd.read_csv("artifacts/photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])
photo_features = np.load("artifacts/features.npy")

if device == "cpu":
    photo_features = torch.from_numpy(photo_features).float().to(device)
else:
    photo_features = torch.from_numpy(photo_features).to(device)


def encode_search_query(search_query):
    with torch.no_grad():
        text_encoded = model.encode_text(
            clip.tokenize(search_query).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
    return text_encoded


def find_best_matches(text_features, photo_features, photo_ids, results_count=3):
    similarities = (photo_features @ text_features.T).squeeze(1)
    best_photo_idx = (-similarities).argsort()
    return [photo_ids[i] for i in best_photo_idx[:results_count]]

'''
This is not being used for now so commenting it out
'''
# def display_photo(photo_id):
#     photo_image_url = f"images/{photo_id}.jpg"
#     display(Image(filename=photo_image_url))
#     print()


def search_s3(search_query, photo_features, photo_ids, results_count=3):
    text_features = encode_search_query(search_query)
    best_photo_ids = find_best_matches(
        text_features, photo_features, photo_ids, results_count)
    lt = []
    for photo_id in best_photo_ids:
        lt.append(photo_id)
        # display_photo(photo_id)
    return lt

def search(search_query):
    return search_s3(search_query, photo_features, photo_ids, 1)

# search_query = predict(image_path)

# if __main__ == "__name__":
    # search_s3(search_query, photo_features, photo_ids, 2)
