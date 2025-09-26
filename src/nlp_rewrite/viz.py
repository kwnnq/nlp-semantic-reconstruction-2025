import json, matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
from .config import paths
from .dataio import load_raw_texts

# — βασικό embedder —
def embed(texts):
    m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return m.encode(texts, normalize_embeddings=True)

def save_scatter(emb, labels, title, outpath: Path):
    xy = PCA(n_components=2, random_state=42).fit_transform(emb)

    fig, ax = plt.subplots(figsize=(8, 6), dpi=180)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")

    # original point (πρώτο στοιχείο)
    ax.scatter(xy[0,0], xy[0,1], marker="o", s=110, linewidths=0.8, edgecolors="black", alpha=0.95, label=labels[0])
    ax.annotate(
        labels[0], (xy[0,0], xy[0,1]),
        textcoords="offset points", xytext=(8, 6),
        fontsize=10, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.6", alpha=0.85)
    )

    # markers για τα pipelines
    mk = ["s", "^", "D", "P", "X", "*", "v"]
    for i in range(1, len(labels)):
        ax.scatter(xy[i,0], xy[i,1], marker=mk[(i-1) % len(mk)], s=90, alpha=0.95, label=labels[i])
        # βελάκι από original -> pipeline
        ax.annotate(
            "", xy=(xy[i,0], xy[i,1]), xytext=(xy[0,0], xy[0,1]),
            arrowprops=dict(arrowstyle="->", lw=1.1, alpha=0.35)
        )
        # label με μικρό πλαίσιο
        ax.annotate(
            labels[i], (xy[i,0], xy[i,1]),
            textcoords="offset points", xytext=(8, 6),
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.8", alpha=0.8)
        )

    ax.legend(loc="best", frameon=True, framealpha=0.9)
    fig.tight_layout()
    # υψηλής ευκρίνειας PNG + διανυσματικό SVG
    fig.savefig(outpath, dpi=220, bbox_inches="tight")
    fig.savefig(outpath.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)

def main():
    data = load_raw_texts()
    recon = json.load(open(paths.recon/"reconstructed_texts.json","r",encoding="utf-8"))
    pipelines = recon.get("B_pipelines", {"rule_based": recon["B_rule_based_full"]})

    # Προαιρετικός χάρτης για πιο «σύντομα» labels
    label_map = {
        "rule_based": "Rule-based",
        "languagetool": "LanguageTool",
        "t5_paraphrase": "T5 Paraphrase",
        "hybrid_rule_then_lt": "Hybrid (RB→LT)"
    }

    for key in ("text1","text2"):
        labels = [f"{key}-orig"]
        texts  = [data[key]]
        for name, pair in pipelines.items():
            labels.append(f"{key}-{label_map.get(name, name)}")
            texts.append(pair[key])

        emb = embed(texts)
        save_scatter(emb, labels, f"PCA — {key}", paths.figures / f"pca_{key}.png")

if __name__ == "__main__":
    main()
