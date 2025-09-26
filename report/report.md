Δομημένη Αναφορά – NLP Semantic Reconstruction 2025
Σύνοψη (Executive Summary)

Υλοποιήθηκε αυτόματη σημασιολογική ανακατασκευή για δύο «θορυβώδη» κείμενα. Χρησιμοποιήθηκε κυρίως ένα rule-based pipeline (ντετερμινιστικοί κανόνες/regex) και αξιολογήθηκε με Sentence-BERT ενσωματώσεις και cosine similarity τόσο σε επίπεδο κειμένου όσο και ανά πρόταση. Τα διαγράμματα PCA έδειξαν μικρή μετατόπιση νοήματος, ειδικά στο Text2. Μετρήσεις: 0.9395 (Text1) και 0.9827 (Text2) σε ολική ομοιότητα· κατά μέσο όρο 0.8976 και 0.9398 αντίστοιχα σε ευθυγραμμισμένες προτάσεις. Συμπέρασμα: το rule-based βελτιώνει σαφήνεια/στίξη με ελάχιστη αλλοίωση νοήματος.

1. Εισαγωγή

Η σημασιολογική ανακατασκευή στοχεύει να μετασχηματίσει ασαφή ή ανορθόδοξα κείμενα σε σαφείς και συνεκτικές εκδοχές χωρίς να θίγεται το νόημα. Τα σύγχρονα NLP μοντέλα (embeddings, GEC, παραφράσεις) επιτρέπουν αυτοματοποίηση και μετρήσιμη αξιολόγηση μέσω διανυσματικών αναπαραστάσεων και μετρικών ομοιότητας.

Σε αυτή τη μελέτη:

Σχεδιάσαμε custom rule-based automaton για καθαρισμό/τυποποίηση.

Μετρήσαμε συνάφεια original ↔ ανακατασκευών με Sentence-BERT (SBERT).

Οπτικοποιήσαμε τη «μετατόπιση» στον σημασιολογικό χώρο με PCA.

Σημ.: Το έργο είναι δομημένο ώστε να υποστηρίξει και LanguageTool (GEC), T5 παραφράσεις και υβριδικό pipeline, όμως στην τρέχουσα εκτέλεση αναλύεται πλήρως το rule-based.

2. Μεθοδολογία
2.1 Δεδομένα

Χρησιμοποιήθηκαν τα κείμενα της εκφώνησης, αποθηκευμένα στο data/raw_texts.json:

Text1: ευχές για Dragon Boat Festival + αλληλογραφία με καθηγητή/εκδότη.

Text2: ενημέρωση για υποβολή άρθρου, καθυστερήσεις/επικοινωνία, acknowledgments.

2.2 Ανακατασκευή (Παραδοτέο 1)

A. Δύο προτάσεις (custom automaton):
Από το Text1 (original → reconstructed):

“Hope you too, to enjoy it as my deepest wishes.” →
“I hope you enjoy it as well, with my warmest wishes.”

“Thank your message to show our words to the doctor, as his next contract checking, to all of us.” →
“Thank you for your message and for forwarding our comments to the doctor ahead of his next contract review.”

B. Πλήρη κείμενα — Rule-based pipeline:
Ενδεικτικά αποσπάσματα:

“Today is our dragon boat festival, in our Chinese culture, to celebrate it…” →
“Today is the Dragon Boat Festival. In Chinese culture, we celebrate it by wishing safety and prosperity for everyone.”

“…the updates was confusing as it not included the full feedback from reviewer or maybe editor?” →
“…the updates were confusing as they did not include the full feedback from the reviewer or possibly the editor.”

C. Σύγκριση (ποιοτικά κριτήρια):

Σαφήνεια: διάσπαση υπερφορτωμένων προτάσεων, τυποποίηση όρων/ευγενικών τύπων.

Συνοχή/στίξη: διόρθωση άρθρων, χρόνων, κόμματα/τελείες, αφαίρεση επαναλήψεων.

Τόνος: σταθερά ευγενικός/επαγγελματικός, χωρίς υπερβολές.

2.3 Υπολογιστική Ανάλυση (Παραδοτέο 2)

Embeddings: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (κανονικοποιημένα).

Ομοιότητα: cosine (scikit-learn) σε ολόκληρο κείμενο και σε ευθυγραμμισμένες προτάσεις (1→1, με sentence split σε [.!?]).

Οπτικοποίηση: PCA 2D (fixed random_state) σε (original + reconstructed) για κάθε κείμενο.

Αναπαραγωγιμότητα: κλειδωμένες εκδόσεις (poetry.lock), σταθερός seed, deterministic ροές.

3. Πειράματα & Αποτελέσματα
3.1 Μετρικές ολικής συνάφειας (SBERT cosine)
pipeline	text	sentence_cosine
rule_based	text1	0.9395
rule_based	text2	0.9827

Ερμηνεία. Το Text2 εμφανίζει σχεδόν τέλεια διατήρηση νοήματος (0.9827), δείγμα ότι οι παρεμβάσεις ήταν κυρίως μορφοσυντακτικές. Στο Text1 (0.9395) η ελαφρώς μικρότερη τιμή οφείλεται σε σκόπιμες παραφράσεις/αναδομήσεις (π.χ. διάσπαση προτάσεων), οι οποίες βελτιώνουν ροή αλλά αυξάνουν λίγο την σημασιολογική απόσταση.

3.2 Μετρικές ανά πρόταση (ευθυγράμμιση 1→1)
pipeline	text	n_aligned	avg_sent_cosine
rule_based	text1	6	0.8976
rule_based	text2	6	0.9398

Ερμηνεία. Η μέση ομοιότητα ανά πρόταση είναι υψηλή και στα δύο κείμενα, με το Text2 να υπερέχει (0.9398). Το Text1 (0.8976) επηρεάζεται από τις πιο «δομικές» βελτιώσεις (π.χ. νέα σημεία στίξης/σύνδεση προτάσεων).

3.3 Οπτικοποίηση (PCA)

Σχήματα:

report/figures/pca_text1.png

report/figures/pca_text2.png

Ανάγνωση. Σε κάθε διάγραμμα, το original λειτουργεί ως «άγκυρα» και η ανακατασκευή (rule-based) βρίσκεται κοντά του. Το μικρό «βέλος μετατόπισης» στο Text2 επιβεβαιώνει τη σχεδόν μηδενική αλλοίωση νοήματος· στο Text1 το βέλος είναι ελαφρώς μεγαλύτερο λόγω παραφράσεων που βελτιώνουν αναγνωσιμότητα.


4. Συζήτηση

Καταλληλότητα embeddings. Τα sentence-level embeddings αποτυπώνουν πειστικά τη σχετική εγγύτητα original ↔ ανακατασκευών· μικρές γραμματικές διορθώσεις σχεδόν δεν μετακινούν το διάνυσμα, ενώ δομικές παραφράσεις προκαλούν ήπια μετατόπιση.

Κύριες προκλήσεις.

Μη φυσικές εκφράσεις από «διαγλωσσικές» επιρροές (διπλά άρθρα, κόμματα).

Ισορροπία μεταξύ ακρίβειας νοήματος και αναγνωσιμότητας.

Περιορισμοί του PCA (γραμμικός μειωτής διαστάσεων· η γεωμετρία στο 2D είναι απλοποίηση).

Πώς αυτοματοποιείται η διαδικασία.

Rule-based: ισχυρό για domain-specific τυποποιήσεις (ορολογία/ύφος), διαφανές & αναπαραγώγιμο.

GEC (LanguageTool): ιδανικό για ασφαλείς μορφοσυντακτικές βελτιώσεις με ελάχιστο drift.

Παραφράσεις (T5): βελτιώνουν ροή/συνοχή· απαιτούν μετρικό έλεγχο (cosine, BERTScore) και ενίοτε ανθρώπινη επιμέλεια.

Υβριδικό (κανόνες → GEC): συνήθως το καλύτερο trade-off.

5. Συμπεράσματα

Το rule-based pipeline πέτυχε υψηλή διατήρηση νοήματος (0.94–0.98) με σημαντική βελτίωση αναγνωσιμότητας και στίξης.

Η ευθυγράμμιση προτάσεων επιβεβαιώνει σταθερά υψηλή ομοιότητα (0.90–0.94).

Τα PCA διαγράμματα οπτικοποιούν τη μικρή σημασιολογική μετατόπιση, ειδικά ελάχιστη στο Text2.

Μελλοντική εργασία: ενσωμάτωση GEC και T5/υβριδικού με συγκριτικούς πίνακες, constrained decoding, και πρόσθετες μετρικές (BERTScore, BLEURT, NLI-based entailment checks).

6. Αναπαραγωγιμότητα & Εκτέλεση

Python ≥ 3.10, διαχείριση με Poetry.

Scripts:

poetry run run-rewrite     # Παρ.1: ανακατασκευές (A/B/C)
poetry run run-analysis    # Παρ.2: cosine & sentence alignment
poetry run run-viz         # Παρ.2: PCA διαγράμματα


Παραγόμενα αρχεία:

outputs/reconstructions/reconstructed_texts.{json,md}

outputs/analysis/{sentence_cosine.csv, sentence_alignment_cosine.csv, results.md}

outputs/figures/{pca_text1.png,pca_text2.png} (+ .svg)


7. Βιβλιογραφία

Reimers, N., & Gurevych, I. (2019). Sentence-BERT.

Raffel, C., et al. (2020). T5: Exploring the Limits of Transfer Learning…

LanguageTool: https://languagetool.org/

Mikolov, T., et al. (2013). word2vec.

Pennington, J., et al. (2014). GloVe.

Bojanowski, P., et al. (2017). FastText.

Devlin, J., et al. (2019). BERT.

scikit-learn (cosine, PCA), matplotlib (οπτικοποίηση).

Παράρτημα: Δομή Αποθετηρίου
nlp-semantic-reconstruction-2025/
├─ data/raw_texts.json
├─ report/
│  ├─ report.md
│  └─ figures/
│     ├─ pca_text1.png
│     └─ pca_text2.png
├─ outputs/
│  ├─ reconstructions/
│  ├─ analysis/
│  └─ figures/
├─ src/nlp_rewrite/
│  ├─ pipelines/{rule_based.py, lt_corrector.py, t5_paraphrase.py}
│  ├─ {run_rewrite.py, analysis.py, viz.py, config.py, dataio.py}
├─ pyproject.toml
├─ poetry.lock
└─ .gitignore
