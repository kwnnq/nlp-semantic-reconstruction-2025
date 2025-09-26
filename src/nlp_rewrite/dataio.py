import json
from .config import paths

def load_raw_texts():
    with open(paths.data / "raw_texts.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def save_markdown(text, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

