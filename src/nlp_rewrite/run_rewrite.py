from .dataio import load_raw_texts, save_json, save_markdown
from .config import paths
from .pipelines.rule_based import reconstruct_text, reconstruct_two_sentences

def main():
    data = load_raw_texts()
    t1, t2 = data["text1"], data["text2"]

    # A: δύο προτάσεις από το Κείμενο 1 (2η & 3η, 0-based indices: 1 και 2)
    two = reconstruct_two_sentences(t1, [1, 2])

    # B: πλήρης ανακατασκευή με rule-based
    rb1 = reconstruct_text(t1)
    rb2 = reconstruct_text(t2)

    out = {
        "A_two_sentences": {"text1": two},
        "B_rule_based_full": {"text1": rb1, "text2": rb2}
    }
    save_json(out, paths.recon / "reconstructed_texts.json")

    md = [
        "# Ανακατασκευές (Minimal)",
        "## A. Δύο προτάσεις (custom automaton)",
        f"- (1) {two.get('1','')}",
        f"- (2) {two.get('2','')}",
        "## B. Πλήρη κείμενα — Rule-based",
        f"**Text1:**\n\n{rb1}\n\n**Text2:**\n\n{rb2}"
    ]
    save_markdown("\n\n".join(md), paths.recon / "reconstructed_texts.md")

if __name__ == "__main__":
    main()

