from __future__ import annotations

import hashlib
import os
import pickle
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from model import DEFAULTS_PATH, normalize_record


MODEL_PATH = Path(os.getenv("MODEL_PATH", Path(__file__).with_name("pipeline.bin")))
with MODEL_PATH.open("rb") as model_file:
    pipeline = pickle.load(model_file)
MODEL_SHA256 = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()
FEATURE_DEFAULTS_SHA256 = hashlib.sha256(DEFAULTS_PATH.read_bytes()).hexdigest()

class Lead(BaseModel):
    lead_source: str | None = None
    industry: str | None = None
    employment_status: str | None = None
    location: str | None = None
    number_of_courses_viewed: int | None = None
    annual_income: float | None = None
    interaction_count: int | None = None
    lead_score: float | None = None


def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "model_sha256": MODEL_SHA256,
        "feature_defaults_sha256": FEATURE_DEFAULTS_SHA256,
    }


def predict(lead: Lead) -> dict[str, Any]:
    record = normalize_record(lead.model_dump())
    probability = float(pipeline.predict_proba([record])[0, 1])
    return {
        "conversion_probability": round(probability, 3),
        "conversion": probability >= 0.5,
    }
   
lead = Lead(
  lead_source = "paid_ads",
  industry = "technology",
  employment_status = "employed",
  location = "north_america",
  number_of_courses_viewed =2,
  annual_income = 79276.0,
  interaction_count = 4,
  lead_score = 0.41
)

# print(health())

print(predict(lead))

