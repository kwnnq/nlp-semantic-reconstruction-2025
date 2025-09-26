import json, numpy as np, pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from .config import paths
from .dataio import load_raw_texts, save_markdown

def sbert_embed(texts):
    m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return m.encode(texts, normalize_embeddings=True)

def sent_cos(a, b):
    emb = sbert_embed([a, b])
    return float(cosine_similarity([emb[0]], [emb[1]])[0, 0])

def chunk(text):
    import re
    s = re.split(r"(?<=[.!?])\s+", text.strip())
    return [x for x in s if x]

def main():
    data = load_raw_texts()
    recon = json.load(open(paths.recon/"reconstructed_texts.json","r",encoding="utf-8"))

    # συνολική ομοιότητα ανά pipeline/κείμενο
    rows=[]
    for name, pair in recon.get("B_pipelines", {"rule_based": recon["B_rule_based_full"]}).items():
        for key in ("text1","text2"):
            score = sent_cos(data[key], pair[key])
            rows.append({"pipeline": name, "text": key, "sentence_cosine": round(score, 4)})

    df = pd.DataFrame(rows).sort_values(["text","sentence_cosine"], ascending=[True,False])
    (paths.analysis/"sentence_cosine.csv").parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(paths.analysis/"sentence_cosine.csv", index=False)

    # sentence-level alignment 1-προς-1
    rows2=[]
    for name, pair in recon.get("B_pipelines", {"rule_based": recon["B_rule_based_full"]}).items():
        for key in ("text1","text2"):
            o, r = chunk(data[key]), chunk(pair[key])
            n = min(len(o),len(r))
            if n == 0: continue
            vals = [sent_cos(o[i], r[i]) for i in range(n)]
            rows2.append({"pipeline": name, "text": key, "n_aligned": n, "avg_sent_cosine": round(float(np.mean(vals)), 4)})
    pd.DataFrame(rows2).to_csv(paths.analysis/"sentence_alignment_cosine.csv", index=False)

    # μικρό markdown summary
    save_markdown(
        "# Παραδοτέο 2 — Αποτελέσματα SBERT cosine\n\n" + df.to_markdown(index=False),
        paths.analysis/"results.md"
    )

if __name__ == "__main__":
    main()
