# utils/translator.py
from transformers import MarianMTModel, MarianTokenizer
import functools

MODEL_NAME = "Helsinki-NLP/opus-mt-en-hi"

_tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
_model = MarianMTModel.from_pretrained(MODEL_NAME)

@functools.lru_cache(maxsize=512)
def _translate_cached(text: str) -> str:
    inputs = _tokenizer(text, return_tensors="pt", padding=True)
    translated = _model.generate(**inputs, max_length=128)
    return _tokenizer.decode(translated[0], skip_special_tokens=True)

def translate_text(text: str, lang: str = "en") -> str:
    if not text or lang == "en":
        return text
    try:
        return _translate_cached(text)
    except Exception:
        return text
