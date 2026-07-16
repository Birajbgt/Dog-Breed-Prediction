from io import BytesIO
from typing import Dict

import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

from backend.services import dogbreed as dogbreed_service

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict[str, object]:
    dogbreed_service.ensure_model_ready()

    if file.content_type not in {"image/jpeg", "image/png", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Please upload a JPG or PNG image")

    image_bytes = await file.read()
    embedding = dogbreed_service.extract_embedding_from_bytes(image_bytes)

    if dogbreed_service.model is not None:
        array = np.expand_dims(
            dogbreed_service.preprocess_input(
                np.asarray(Image.open(BytesIO(image_bytes)).convert("RGB").resize(dogbreed_service.IMAGE_SIZE), dtype=np.float32)
            ),
            axis=0,
        )
        probabilities = dogbreed_service.model.predict(array, verbose=0)[0]
        predicted_index = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_index]) * 100.0
        predicted_breed = dogbreed_service.class_names[predicted_index] if predicted_index < len(dogbreed_service.class_names) else "unknown"

        return {
            "predicted_breed": predicted_breed,
            "confidence": round(confidence, 2),
            "all_probabilities": {
                dogbreed_service.class_names[i]: round(float(probabilities[i]) * 100.0, 2)
                for i in range(len(dogbreed_service.class_names))
            },
        }

    scores = {}
    for breed, prototype in dogbreed_service.class_prototypes.items():
        similarity = float(np.dot(embedding, prototype))
        scores[breed] = similarity

    predicted_breed, confidence = max(scores.items(), key=lambda item: item[1])
    normalized_scores = {breed: round(float(score) * 100.0, 2) for breed, score in scores.items()}

    return {
        "predicted_breed": predicted_breed,
        "confidence": round(float(confidence) * 100.0, 2),
        "all_probabilities": normalized_scores,
    }
