from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL = "google/flan-t5-base"
_tok = None
_mdl = None

def _load():
    global _tok, _mdl
    if _tok is None:
        _tok = AutoTokenizer.from_pretrained(MODEL)
    if _mdl is None:
        _mdl = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    return _tok, _mdl

def paraphrase(text: str) -> str:
    tok, mdl = _load()
    prompt = (
        "Paraphrase the following to be clear, concise, and formal while preserving meaning:\n"
        + text
    )
    inputs = tok(prompt, return_tensors="pt", truncation=True)
    with torch.no_grad():
        ids = mdl.generate(
            **inputs,
            max_new_tokens=256,
            num_beams=5,       # deterministic
            do_sample=False,   # χωρίς sampling -> ίδια έξοδος κάθε φορά
            early_stopping=True
        )
    return tok.decode(ids[0], skip_special_tokens=True)
