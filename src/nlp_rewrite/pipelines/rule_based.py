import re

# ——— Κανόνες αντικατάστασης (deterministic) ———
REPLACEMENTS = [
    # Τυποποίηση εορτής & πολιτισμικής φράσης
    (r"\bdragon boat festival\b", "Dragon Boat Festival"),
    (r"\bour Dragon Boat Festival\b", "the Dragon Boat Festival"),
    (r"Festival,\s+In Chinese culture", "Festival. In Chinese culture"),
    (r"\bin our Chinese culture\b", "in Chinese culture"),
    (r"\bin Chinese culture, to celebrate it\b", "In Chinese culture, we celebrate it"),
    (r"\bto celebrate it wishing\b", "we celebrate it by wishing"),
    (r"\bwe celebrate it wishing\b", "we celebrate it by wishing"),

    # Ευχές / ευγένεια
    (r"\bwith all safe and great in our lives\b", "wishing safety and prosperity for everyone"),
    (r"\bHope you too, to enjoy it\b", "I hope you enjoy it too"),
    (r"\bI hope you enjoy it too\b", "I hope you enjoy it as well"),
    (r"\btoo with my warmest wishes\b", "as well, with my warmest wishes"),
    (r"\bas my deepest wishes\b", "with my warmest wishes"),

    # Ευχαριστίες & προώθηση μηνύματος
    (r"\bThank your message\b", "Thank you for your message"),
    (r"Thank you for your message for forwarding", "Thank you for your message and for forwarding"),
    (r"\bto show our words to the doctor\b", "for forwarding our comments to the doctor"),
    (r"to the doctor,\s+ahead", "to the doctor ahead"),
    (r"\bas his next contract checking\b", "ahead of his next contract review"),
    (r",?\s*to all of us\b", ""),

    # Updates / professor / approval
    (r"\bI got this message to see the approved message\b", "I received this update confirming the approval"),
    (r"\bI have received the message from the professor\b", "I also received a message from the professor"),
    (r"\bI also received a message from the professor, to show me, this, a couple of days ago\b",
     "I also received a message from the professor a couple of days ago"),
    (r"\bI am very appreciated\b", "I greatly appreciate"),
    (r"\bthe full support of the professor,?\s+for our\b", "the professor's full support for our"),
    (r"\bSpringer proceedings publication\b", "publication in the Springer proceedings"),

    # Κείμενο 2 — συζήτηση/updates
    (r"\bduring our final discuss\b", "During our final discussion"),
    (r"\bupdates was\b", "updates were"),
    (r"\bit not included\b", "they did not include"),
    (r"\bfrom reviewer or maybe editor\b", "from the reviewer or possibly the editor"),
    (r"from the reviewer or possibly the editor\?", "from the reviewer or possibly the editor."),
    (r"\balthough bit delay\b", "although there was a slight delay"),
    (r"\bat recent days\b", "in recent days"),
    (r"\btried best for paper\b", "did their best on the paper"),
    (r"\bpaper and cooperation\b", "paper and the collaboration"),
    (r"\bSpringer link came finally last week\b", "the Springer link was finally issued last week"),

    # Acknowledgments / reminders
    (r"\bdoctor still plan\b", "the doctor still plans"),
    (r"\bstill plans for the acknowledgments section edit\b", "still plans to edit the acknowledgments section"),
    (r"\bbefore he sending again\b", "before he sends it again"),
    (r"Also, kindly remind me please, if\b", "Please remind me if"),
    (r"\bdidn’t see that part final yet\b", "haven’t seen that section finalized yet"),
    (r"he sends it again\.\s*Because I haven’t seen that section finalized yet, or maybe I missed, I apologize if so\.?",
     "he sends it again, because I haven’t seen that section finalized yet; if I missed it, I apologize."),
    (r"\bmaybe I missed\b", "maybe I missed it"),

    # Συνολική ομαλοποίηση ύφους/σύνταξης (Text2 αρχή)
    (r"Anyway, I believe the team, although there was a slight delay and less communication in recent days, they really did",
     "Despite a slight delay and reduced communication in recent days, the team did"),

    # Κλείσιμο/ευγένεια
    (r"\bmake sure all are safe\b", "make sure everyone is safe"),
    (r"\bfuture targets\b", "our next goals"),
]

# ——— Βοηθητικές συναρτήσεις ———
def normalize(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,;:.?!])", r"\1", s)
    return s

def postprocess(s: str) -> str:
    # αφαίρεση διπλών άρθρων
    s = re.sub(r"\b(the|a|an)\s+\1\b", r"\1", s, flags=re.IGNORECASE)
    # κεφαλαίο μετά από τελεία
    s = re.sub(r"\.\s+([a-z])", lambda m: ". " + m.group(1).upper(), s)
    # πεζό μετά από κόμμα (για αποφυγή "..., In ...")
    s = re.sub(r",\s+([A-Z])", lambda m: ", " + m.group(1).lower(), s)
    # καθάρισμα κενών/κόμμα
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def apply_replacements(text: str) -> str:
    out = text
    for pat, rep in REPLACEMENTS:
        out = re.sub(pat, rep, out, flags=re.IGNORECASE)
    out = re.sub(r"\bI am very appreciate(d)?\b", "I greatly appreciate", out, flags=re.IGNORECASE)
    out = normalize(out)
    out = postprocess(out)
    return out

def reconstruct_text(text: str) -> str:
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    sents = [apply_replacements(s) for s in sents if s.strip()]
    sents = [s[0].upper() + s[1:] if s and s[0].islower() else s for s in sents]
    return " ".join(sents)

def reconstruct_two_sentences(text: str, idxs: list[int]) -> dict:
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return {str(i): apply_replacements(sents[i]) for i in idxs if 0 <= i < len(sents)}
