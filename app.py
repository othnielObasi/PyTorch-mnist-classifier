import os
import sys
import glob
import numpy as np
import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional


# Force quantized inference backend
torch.backends.quantized.engine = 'fbgemm'

# === Model loading ===
matches = glob.glob("model/**/*.pt", recursive=True)
if not matches:
    print("❌ Could not find any .pt file in model/", file=sys.stderr)
    sys.exit(1)

MODEL_PATH = matches[0]
print(f"🔍 Loading model from {MODEL_PATH}", file=sys.stderr)

try:
    model = torch.jit.load(MODEL_PATH, map_location="cpu")
    model.eval()
except Exception as e:
    print(f"❌ Failed to load model: {e}", file=sys.stderr)
    sys.exit(1)

# FastAPI setup 
app = FastAPI(title="MNIST Quantized Digit Recognizer")

# Request/Response Schemas 
class PredictRequest(BaseModel):
    pixels: list  # 784 flat list or 28x28 nested list
    true_label: Optional[int] = None

class PredictResponse(BaseModel):
    predicted: int
    confidence: float  # percentage 0–100.0

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    arr = np.array(req.pixels, dtype=np.float32)

    if arr.size == 784:
        arr = arr.reshape(1, 1, 28, 28)
    elif arr.shape == (28, 28):
        arr = arr.reshape(1, 1, 28, 28)
    else:
        raise HTTPException(status_code=400, detail="Input must be 28×28 or a flat list of length 784")

    # Normalize using MNIST mean and stddev
    arr = (arr - 0.1307) / 0.3081
    tensor = torch.from_numpy(arr)

    with torch.no_grad():
        logits = model(tensor)
        probs = F.softmax(logits, dim=1)[0].cpu().numpy()
        pred = int(np.argmax(probs))
        conf = float(probs[pred])
        percent = round(conf * 100, 1)
    return PredictResponse(predicted=pred, confidence=percent)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "MNIST model is live and ready!"}
