from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Dict, List

import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input

BASE_DIR = Path(__file__).resolve().parents[2]
TRAIN_DIR = BASE_DIR / "train"
MODEL_PATH = BASE_DIR / "dog_breed_model.h5"
IMAGE_SIZE = (128, 128)

model: tf.keras.Model | None = None
feature_model: tf.keras.Model | None = None
class_names: List[str] = []
class_prototypes: Dict[str, np.ndarray] = {}


def load_class_names() -> List[str]:
    if not TRAIN_DIR.exists():
        raise FileNotFoundError("Training folder not found")
    breed_dirs = sorted(p.name for p in TRAIN_DIR.iterdir() if p.is_dir())
    return breed_dirs


def get_feature_model() -> tf.keras.Model:
    global feature_model
    if feature_model is None:
        feature_model = MobileNetV2(
            weights="imagenet",
            include_top=False,
            pooling="avg",
            input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3),
        )
        feature_model.trainable = False
    return feature_model


def extract_embedding_from_bytes(image_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMAGE_SIZE)
    arr = np.asarray(img, dtype=np.float32)
    arr = np.expand_dims(preprocess_input(arr), axis=0)
    embedding = get_feature_model().predict(arr, verbose=0)[0]
    embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
    return embedding


def build_class_prototypes() -> Dict[str, np.ndarray]:
    global class_prototypes
    prototypes: Dict[str, np.ndarray] = {}
    for breed in class_names:
        breed_dir = TRAIN_DIR / breed
        sample_files = sorted(breed_dir.glob("*.jpg"))[:3]
        if not sample_files:
            continue

        embeddings = []
        for sample in sample_files:
            image_bytes = sample.read_bytes()
            embeddings.append(extract_embedding_from_bytes(image_bytes))

        prototype = np.mean(np.stack(embeddings, axis=0), axis=0)
        prototype = prototype / (np.linalg.norm(prototype) + 1e-8)
        prototypes[breed] = prototype

    class_prototypes = prototypes
    return prototypes


def ensure_model_ready() -> None:
    global model, class_names

    class_names = load_class_names()
    if model is not None:
        return

    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    except Exception as exc:
        print(f"Saved model load failed; using feature-prototype fallback. Error: {exc}")
        build_class_prototypes()
        model = None
