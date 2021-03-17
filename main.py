from fastapi import Depends, FastAPI
from gector.gec_model import GecBERTModel
from pydantic import BaseModel

app = FastAPI()

MODEL_PATHS = "./bert_0_gector.th"
VOCAB_PATH = "./data/output_vocabulary"
TRANSFORMER_MODEL = "bert"
SPECIAL_TOKENS_FIX = 0
MAX_LEN = 50
MIN_LEN = 3
ITERATION_COUNT = 5
MIN_ERROR_PROBABILITY = 0
ADDITIONAL_CONFIDENCE = 0
IS_ENSEMBLE = 0
LOWERCASE_TOKENS = 0
WEIGHTS = None

model = GecBERTModel(
    vocab_path=VOCAB_PATH,
    model_paths=[MODEL_PATHS],
    max_len=MAX_LEN,
    min_len=MIN_LEN,
    iterations=ITERATION_COUNT,
    min_error_probability=MIN_ERROR_PROBABILITY,
    lowercase_tokens=LOWERCASE_TOKENS,
    model_name=TRANSFORMER_MODEL,
    special_tokens_fix=SPECIAL_TOKENS_FIX,
    log=False,
    confidence=ADDITIONAL_CONFIDENCE,
    is_ensemble=IS_ENSEMBLE,
    weigths=WEIGHTS,
)


def get_model():
    return model


class GrammarRequest(BaseModel):
    text: str


class GrammarResponse(BaseModel):
    result: str


@app.post("/predict/grammar/single", response_model=GrammarResponse)
def predict(request: GrammarRequest, model: GecBERTModel = Depends(get_model)):
    # return model.predict(request)
    preds, _ = model.handle_batch([request.text.split()])
    return GrammarResponse(result=" ".join(preds[0]))