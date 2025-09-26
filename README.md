NLP Semantic Reconstruction 2025

Αυτό το αποθετήριο υλοποιεί μια ροή εργασίας για σημασιολογική ανακατασκευή κειμένων με Python/Poetry. Περιλαμβάνει:

Ανακατασκευή με πολλαπλά pipelines (Rule-based, LanguageTool GEC, T5 Paraphrase, Υβριδικό).

Υπολογιστική ανάλυση με Sentence-BERT embeddings και cosine similarity (σε επίπεδο κειμένου & πρότασης).

Οπτικοποίηση μετατόπισης νοήματος με PCA.

Δομημένη αναφορά στο report/report.md.

1) Προαπαιτούμενα

Python ≥ 3.10

Poetry
 (συνίσταται: pipx install poetry)

Git

Σε Windows/PowerShell: έχει δοκιμαστεί με Python 3.11 + Poetry 2.2.
Δεν απαιτείται χειροκίνητη ενεργοποίηση venv — τρέχουμε με poetry run ....

2) Γρήγορη εκτέλεση (Windows PowerShell)
# μέσα στον ριζικό φάκελο του project
poetry install

# Παραδοτέο 1: ανακατασκευές (A/B/C)
poetry run run-rewrite

# Παραδοτέο 2: μετρικές cosine & sentence alignment
poetry run run-analysis

# Παραδοτέο 2: PCA διαγράμματα (png/svg)
poetry run run-viz


Παράγονται αρχεία:

outputs/reconstructions/reconstructed_texts.{json,md}
outputs/analysis/{sentence_cosine.csv, sentence_alignment_cosine.csv, results.md}
outputs/figures/{pca_text1.png, pca_text2.png} (+ .svg)

3) Δομή αποθετηρίου
nlp-semantic-reconstruction-2025/
├─ data/raw_texts.json
├─ outputs/
│  ├─ reconstructions/
│  ├─ analysis/
│  └─ figures/
├─ report/
│  ├─ report.md
│  └─ figures/           
├─ src/nlp_rewrite/
│  ├─ pipelines/
│  │  ├─ rule_based.py
│  │  ├─ lt_corrector.py      # LanguageTool (GEC)
│  │  └─ t5_paraphrase.py     # FLAN-T5 paraphrasing
│  ├─ run_rewrite.py
│  ├─ analysis.py
│  ├─ viz.py
│  ├─ config.py
│  └─ dataio.py
├─ pyproject.toml
├─ poetry.lock
└─ .gitignore

4) Pipelines (Παραδοτέο 1)

Rule-based: Ντετερμινιστικοί κανόνες (regex) για τυποποίηση/στίξη/ευγένεια.

LanguageTool (GEC): Γραμματικο-ορθογραφικές διορθώσεις μέσω language_tool_python.

T5 Paraphrase: google/flan-t5-base, num_beams=5, do_sample=False για αναπαραγωγιμότητα.

Υβριδικό (RB→LT): Rule-based και στη συνέχεια GEC.

Στην τρέχουσα υλοποίηση, το Rule-based είναι πλήρως ενεργό. Τα άλλα pipelines είναι έτοιμα (αρχεία & imports) — αρκεί να είναι εγκατεστημένες οι βιβλιοθήκες:

poetry add language-tool-python transformers torch sentence-transformers scikit-learn pandas matplotlib tabulate

5) Μετρικές & Οπτικοποίηση (Παραδοτέο 2)

Embeddings: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (normalize).

Cosine: sklearn.metrics.pairwise.cosine_similarity για (α) ολόκληρο κείμενο, (β) sentence alignment 1→1.

PCA: 2D προβολή original vs. pipelines με βελάκια μετατόπισης.

Αναπαραγωγιμότητα: beam-only T5, σταθερά seeds όπου χρειάζεται, κλειδωμένες εκδόσεις στο poetry.lock.

6) Αναφορά (Παραδοτέο 3)

Η πλήρης αναφορά βρίσκεται στο report/report.md.
Για να φαίνονται τα PCA στο GitHub:

mkdir report\figures -ErrorAction SilentlyContinue
Copy-Item outputs\figures\pca_text1.png report\figures\ -Force
Copy-Item outputs\figures\pca_text2.png report\figures\ -Force
# (προαιρετικά) SVG
Copy-Item outputs\figures\pca_text1.svg report\figures\ -Force
Copy-Item outputs\figures\pca_text2.svg report\figures\ -Force

7) Συμβουλές/Αποσφαλμάτωση

pandas.DataFrame.to_markdown -> Missing 'tabulate'
poetry add tabulate

HuggingFace symlink warning (Windows)
Προαιρετικά απενεργοποίηση:
setx HF_HUB_DISABLE_SYMLINKS_WARNING "1"

PowerShell ExecutionPolicy στο Activate.ps1
Δεν χρειάζεται ενεργοποίηση venv — χρησιμοποίησε poetry run ....
(Αλλιώς προσωρινά: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force)

Γραφήματα πιο «καθαρά»
Το viz.py αποθηκεύει PNG και SVG (υψηλή ανάλυση για αναφορά).

8) Άδειες / Αναφορές

Χρησιμοποιούνται ανοιχτές βιβλιοθήκες:
Transformers, sentence-transformers, scikit-learn, pandas, matplotlib, language-tool-python.

Μοντέλα & εργαλεία:

SBERT: Reimers & Gurevych (2019)

T5: Raffel et al. (2020)

LanguageTool (GEC)

Τα αρχικά κείμενα παρέχονται από την εκφώνηση της εργασίας.

9) Scripts (Poetry)
[tool.poetry.scripts]
run-rewrite = "nlp_rewrite.run_rewrite:main"
run-analysis = "nlp_rewrite.analysis:main"
run-viz = "nlp_rewrite.viz:main"

10) Git workflow (ενδεικτικά)
git add .
git commit -m "feat: run pipelines + analysis + viz"
git push

Τέλος README
