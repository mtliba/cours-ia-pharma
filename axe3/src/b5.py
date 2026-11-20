from lib import *
import numpy as np

SCORES = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.5, 1.7, 1.9, 2.2, 2.6, 3.1, 4.0]

def fig_hub():
    f = Fig(800, 560, "One pre-trained model at the centre, adapted to six different downstream tasks")
    tasks = [(40, 30, "Risk prediction"), (300, 10, "Report drafting"), (560, 30, "Phenotyping"), (40, 440, "Retrieval"), (300, 460, "Property prediction"), (560, 440, "Question answering")]
    for x, y, t in tasks:
        f.arrow(400 + (x + 100 - 400) * 0.32, 280 + (y + 40 - 280) * 0.36, x + 100 + (400 - x - 100) * 0.12, y + 40 + (280 - y - 40) * 0.24, INK, 4, 14)
        f.box(x, y, 200, 80, t, WHITE, INK, "axw", lines=2 if len(t) > 12 else 1)
    f.box(230, 205, 340, 150, "<b>Foundation model</b><br>pre-trained once,<br>without task labels", PALE, BLUE, "axw", lines=3)
    return f

def fig_ladder():
    f = Fig(1500, 430, "Adaptation ladder: from prompting to training from scratch, with increasing need for labelled data and compute")
    steps = ["Zero-shot<br>prompt", "In-context<br>examples", "Linear<br>probe", "LoRA,<br>adapters", "Full<br>fine-tuning", "Train from<br>scratch"]
    sub = ["0 labels", "5 to 50", "100s", "100s to 1,000s", "1,000s +", "100,000s +"]
    for i, t in enumerate(steps):
        x = i * 250; y = 248 - i * 38; col = (PALE, BLUE) if i < 5 else (PINK, RED)
        f.rect(x + 4, y, 240, 360 - y, col[0], col[1], 3, 6)
        f.labc(x + 124, y + 46, f"<b>{t}</b>", 230, "axw", lines=2)
        f.lab(x + 4, 368, sub[i], 240, "center", "ax")
    f.lab(0, 4, "more labelled data, more compute, more weights changed →", 1100, "left", "axh")
    return f

def fig_lora():
    f = Fig(800, 520, "LoRA: a frozen weight matrix plus the product of two thin trainable matrices")
    f.rect(40, 110, 260, 260, "#DFE2EA", MUTE, 3, 6); f.labc(170, 240, "<b>W₀</b><br>frozen<br>d × k", 240, "axw", lines=3)
    f.labc(345, 240, "<b>+</b>", 60, "axw")
    f.rect(400, 110, 44, 260, PINK, RED, 3, 6); f.lab(382, 384, "<b>B</b> · d × r", 150, "left", "axw", RED)
    f.labc(480, 240, "<b>×</b>", 50, "axw")
    f.rect(520, 110, 260, 44, PINK, RED, 3, 6); f.lab(520, 166, "<b>A</b> · r × k", 260, "center", "axw", RED)
    f.lab(40, 40, "16.8 million weights", 320, "left", "axh", MUTE); f.lab(400, 40, "65,536 weights", 380, "left", "axh", RED)
    f.lab(40, 450, "d = k = 4,096 and r = 8: the update has 0.39 % of the weights", 760, "left", "ax ax-b")
    return f

def fig_rag():
    return flow(["<b>Question</b>", "<b>Retriever</b><br>embedding<br>search", "<b>Top passages</b><br>with their<br>sources", "<b>Language model</b><br>reads question<br>+ passages", "<b>Answer</b><br>with citations"], 1500, 300, "Retrieval-augmented generation: question, retriever, passages, language model, cited answer",
                subs=["from the user", "over a curated corpus", "product information, guidelines", "weights unchanged", "checkable by the reader"], gap=44, colors=[(WHITE, INK), (PALE, BLUE), (WHITE, BLUE), (PALE, BLUE), (WHITE, INK)])

def fig_agent():
    f = Fig(1500, 330, "Tool use: the language model plans, calls a pharmacokinetic simulator, reads the result, then answers")
    B = [(0, "<b>Request</b><br>dose for a target<br>exposure?", WHITE, INK), (300, "<b>Language model</b><br>plans and writes<br>a tool call", PALE, BLUE), (600, "<b>Tool</b><br>PK model,<br>database, code", PINK, RED), (900, "<b>Language model</b><br>reads the result", PALE, BLUE), (1200, "<b>Answer</b><br>computed value,<br>with its source", WHITE, INK)]
    for i, (x, t, fill, st) in enumerate(B):
        f.box(x, 60, 250, 150, t, fill, st, "axw", lines=3 if t.count("<br>") == 2 else 2)
        if i < 4: f.arrow(x + 254, 135, x + 296, 135, INK, 4, 14)
    f.lab(560, 218, "computes: it does not guess", 460, "left", "axh", RED)
    f.lab(0, 286, "The language model orchestrates. The number comes from a model you can audit.", 1500, "left", "ax ax-b")
    return f

def fig_conf():
    f = Fig(800, 380, "Nineteen calibration scores on a line; the eighteenth smallest defines the conformal threshold")
    X = lambda v: 60 + v / 4.2 * 700
    f.line(60, 200, 760, 200, MUTE, 3)
    for v in [0, 1, 2, 3, 4]:
        f.line(X(v), 192, X(v), 208, MUTE, 3); f.lab(X(v) - 40, 216, str(v), 80, "center")
    for i, s in enumerate(SCORES): f.circle(X(s), 200 - (16 if i % 2 else 0), 10, RED if i == 17 else BLUE, WHITE, 2)
    f.line(X(3.1), 90, X(3.1), 240, RED, 4, "10 8")
    f.lab(X(3.1) - 420, 40, "threshold: the 18th of 19 scores", 520, "right", "axh", RED)
    f.lab(60, 280, "Absolute error on 19 calibration patients (ng/mL)", 700, "center", "ax ax-b")
    return f

CODE = '''class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, r=8, alpha=16):
        super().__init__()
        self.base = base
        for p in base.parameters():     # freeze W0
            p.requires_grad = False
        d, k = base.out_features, base.in_features
        self.A = nn.Parameter(torch.randn(r, k) * 0.01)
        self.B = nn.Parameter(torch.zeros(d, r))
        self.scale = alpha / r

    def forward(self, x):
        delta = (x @ self.A.T) @ self.B.T   # low rank
        return self.base(x) + self.scale * delta'''

def build():
    S = Session(9, "en", "Part II · Advanced track", "Foundation models and adaptation", "From a large pre-trained model to a small clinical dataset: prompting, probing, low-rank adaptation, retrieval, and how to trust the result.")
    S.sec("Opening: 800 labelled patients and one week of compute.")
    S.cover("Session nine. Take the transformer of session six, train it with the self-supervised objectives of sessions six to eight on a very large corpus, and you obtain what is now called a foundation model. Most of you will never pre-train one. You will adapt one. This session is about that step: which adaptation strategy fits which data budget, and how to know whether the adapted model can be trusted.")
    S.sit("800 patients, one week", "You have 800 labelled transplant recipients, a graphics card for one week, and three options.<br><br><b>A.</b> Train a transformer from scratch.<br><b>B.</b> Adapt a published pre-trained model.<br><b>C.</b> Prompt a general-purpose language model.",
          "Which strategy fits which data budget, and how do you know the result can be trusted?",
          "A realistic starting point. Eight hundred labelled transplant recipients, one graphics card for a week, and three options. Train a transformer from scratch. Adapt a published pre-trained model. Or prompt a general-purpose language model with the records written out as text. After session five you know that option A will over-fit. Options B and C both rely on a model trained by someone else, on data you have not seen. So the session has two questions. A technical one: how to adapt. And a methodological one: how to check that what comes out is reliable on your patients.")
    S.obj(["Define a foundation model and locate the main ones used in the life sciences.", "Order the adaptation strategies by data and compute, and explain low-rank adaptation.", "Describe retrieval-augmented generation and tool use, and what each does and does not fix.", "Quantify uncertainty with conformal prediction, and design an honest evaluation."],
          "Four objectives. Define a foundation model and know the main ones in the life sciences. Order the adaptation strategies by the data and compute they need, and explain low-rank adaptation in detail. Describe retrieval-augmented generation and tool use: what each fixes, and what it does not. And quantify uncertainty with conformal prediction, within an evaluation protocol that an external reviewer would accept.")
    S.plan([("What a foundation model is", "Definition, and a map for the life sciences"), ("The adaptation ladder", "Prompting, in-context learning, probing, LoRA, fine-tuning"), ("Connecting a model to knowledge", "Retrieval, tools and agents"), ("What goes wrong, and how to check", "Shift, contamination, calibration, conformal prediction"), ("Choosing a strategy", "A decision guide and a short implementation")],
           "Five parts. What a foundation model is. The adaptation ladder, from prompting to fine-tuning. Connecting a model to external knowledge and to tools. What goes wrong, and how to check. And a decision guide, with a short implementation of low-rank adaptation.")
    S.sec("What a foundation model is, and where they exist in the life sciences.")
    S.pts("What is a foundation model?", "A model trained on broad data at scale, adaptable to many downstream tasks (Bommasani et al., 2021).",
          ["<b>Broad data</b>: not collected for one task.", "<b>At scale</b>: usually self-supervised, on far more data than any labelled set.", "<b>Adaptable</b>: one set of weights serves many tasks, after little or no further training.", "The economic point: pre-training is paid once and shared."],
          "The term was coined in 2021. A foundation model is trained on broad data at scale and can be adapted to a wide range of downstream tasks. Three ingredients. Broad data, not collected with one task in mind. Scale, which in practice means self-supervision, because labels do not exist at that scale. And adaptability: the same weights serve many tasks. The economics follow: pre-training is expensive and is paid once; adaptation is cheap and is paid per task. The risk follows too: any flaw in the shared model is inherited by everything built on it.",
          fig=fig_hub())
    S.tbl("A map for the life sciences", "The same recipe, applied to different kinds of sequence.", ["Domain", "Pre-training", "Example", "Adapted to"],
          [["Language", "Text; next-token prediction", "General-purpose language models", "Extraction, question answering, code"], ["Proteins", "Sequences; masked residues", "ESM-2 (Lin et al., 2023)", "Structure, function, variant effect"],
           ["Molecules", "SMILES or graphs; masked or contrastive", "Chemical language models", "Property prediction, generation"], ["Images", "Pathology, radiology; self-distillation, masking", "DINOv2-style encoders", "Classification, segmentation, retrieval"],
           ["Health records", "Event sequences; next-event prediction", "Delphi-2M (Shmatko et al., 2025)", "Disease risk, synthetic trajectories"], ["Tables", "Synthetic datasets; in-context prediction", "TabPFN (Hollmann et al., 2025)", "Small tabular problems"]],
          "Foundation models are not only language models. The same recipe has been applied to every kind of sequence. Proteins: ESM-2 is trained to fill in masked amino acids, and its representations support structure prediction. Molecules: language models over SMILES strings or graph encoders. Images: self-supervised encoders for pathology and radiology. Health records: Delphi-2M, trained to predict the next disease event. And tables: TabPFN, a transformer pre-trained on millions of synthetic datasets, which predicts on a new small table without any gradient step. For each line the question is the same: what was the pre-training data, and how far is it from mine?",
          widths=[16, 30, 28, 26], small=True)
    S.nums("An example: a model of disease histories", "Delphi-2M, a modified GPT architecture (Shmatko et al., Nature, 2025).",
           [("0.4 M", "UK Biobank participants used to train the model"), ("1.9 M", "Danish individuals used for external validation, with no change of parameters"), ("&gt; 1,000", "diseases whose rates are predicted from each person's past history")],
           "One example in detail, because it is close to what a pharmacology unit might build. Delphi-2M modifies the GPT architecture to model sequences of diagnoses over a lifetime. It was trained on four hundred thousand participants of the UK Biobank. It was then evaluated on one point nine million individuals from Danish registries, without changing a single parameter: a true external validation, in another country and another health system. It predicts the rates of more than a thousand diseases given a person's history, with accuracy comparable to single-disease models, and it can sample synthetic future trajectories. The authors also report biases learned from the training data. Read that paper as a template for how to validate.",
           band="Trained in one country, validated unchanged in another: that is the standard to aim for.")
    S.sec("The adaptation ladder: from prompting to full fine-tuning.")
    S.wide("The adaptation ladder", "Start at the bottom. Climb only when the step below is not enough.", fig_ladder(),
           "Here are the options, ordered by what they cost. Zero-shot prompting: describe the task in words, no labels. In-context examples: put a few solved cases in the prompt. Linear probe: freeze the model, train a linear layer on its representations. Low-rank adaptation and other adapters: train a small number of additional weights. Full fine-tuning: update everything. And at the top, in red, training from scratch, which is what we are trying to avoid. The labels under each step are orders of magnitude, not rules. The method is to start at the bottom and climb only when the step below is clearly insufficient, with a baseline measured at every step.",
           band="Each step up changes more weights, needs more labels, and is easier to over-fit.")
    S.tbl("What each strategy trains", "And the risk that comes with it.", ["Strategy", "What is trained", "Main risk"],
          [["Prompting, in-context", "Nothing", "Sensitive to wording and to the order of examples; hard to audit"], ["Linear probe", "One linear layer on frozen features", "Under-fits if the features miss the signal"],
           ["LoRA, adapters", "Small added matrices, under 1 % of the weights", "Rank and learning rate need tuning"], ["Full fine-tuning", "All weights", "Over-fitting; forgetting of general abilities"],
           ["Continued pre-training", "All weights, self-supervised, on your unlabelled data", "Compute; then one of the above is still needed"]],
          "The same ladder, with what is trained and the main risk. Prompting trains nothing; it is sensitive to the wording and even to the order of the examples, so fix and report the prompt. A linear probe is the safest first experiment and tells you whether the signal is in the features at all. Low-rank adaptation trains under one percent of the weights. Full fine-tuning over-fits small datasets and can erase general abilities, which is called catastrophic forgetting. One more option, often the best for a hospital: continue the self-supervised pre-training on your own unlabelled records, then probe or adapt.",
          widths=[24, 38, 38], small=True)
    S.eq("In-context learning", "Adaptation without changing any weight.", r"\hat{y} = f_\theta\left(\,x_{\mathrm{new}}\ ;\ (x_1,y_1),\,\dots,\,(x_k,y_k)\,\right)",
         [(r"(x_1,y_1),\dots,(x_k,y_k)", "A few <b>solved examples</b>, written into the model's input."), (r"x_{\mathrm{new}}", "The case to predict, appended after them."), (r"\theta", "The weights. They are <b>not updated</b>: all the adaptation happens in the forward pass."),
          (None, "TabPFN applies this to tables: the training set is the context, and the prediction for a new row takes one forward pass.")],
         "In-context learning deserves its own slide because it is conceptually new. The model receives, in its input, a few solved examples followed by a new case, and predicts the answer for the new case. No weight changes. The learning algorithm is executed by the forward pass. For language models this is few-shot prompting. TabPFN turns the idea into a tabular method: the whole training table is given as context, and the prediction for a new row takes one forward pass. On datasets of up to ten thousand samples its authors report that it outperforms tuned gradient-boosted trees. For small clinical tables it is now a baseline you should run.",
         band="The examples are data for the forward pass, not for gradient descent.")
    S.eq("Low-rank adaptation (LoRA)", "Freeze the weights; learn a small correction.", r"W = W_0 + \frac{\alpha}{r}\,BA,\qquad B\in\mathbb{R}^{d\times r},\quad A\in\mathbb{R}^{r\times k}",
         [(r"W_0", "A pre-trained weight matrix, d × k. <b>Frozen.</b>"), (r"B,\ A", "Two thin <b>trainable</b> matrices. B starts at zero, so training starts exactly from the pre-trained model."),
          (r"r", "The <b>rank</b>, typically 4 to 64, far below d and k. The update has r (d + k) weights instead of d k."), (r"\alpha", "A scaling constant.")],
         "Low-rank adaptation is the method you will use most. Take a weight matrix W zero of the pre-trained model, d by k, and freeze it. Add a correction, written as the product of two thin matrices: B, d by r, and A, r by k, where the rank r is small. Only A and B are trained. The update has r times d plus k weights instead of d times k. With d and k equal to four thousand ninety-six and rank eight, that is sixty-five thousand weights instead of almost seventeen million: zero point three nine percent. B is initialized to zero, so training starts exactly from the pre-trained model. After training, the product can be merged into W zero: no extra cost at inference.",
         fig=fig_lora())
    S.sec("Connecting a model to knowledge: retrieval, tools and agents.")
    S.wide("Retrieval-augmented generation", "Give the model the documents instead of hoping it remembers them.", fig_rag(),
           "A language model stores knowledge in its weights, imprecisely, and frozen at its training date. For drug information that is not acceptable. Retrieval-augmented generation separates knowledge from language. The question is embedded and used to search a curated corpus: summaries of product characteristics, guidelines, the unit's own protocols. The most relevant passages are placed in the prompt, with their sources. The model answers from them and cites them. The weights are unchanged, and updating knowledge means updating the corpus. What this fixes: outdated or missing knowledge, and traceability. What it does not fix: the model can still misread a passage or ignore it. Evaluate retrieval and generation separately.",
           band="Retrieval reduces hallucination and makes answers checkable. It does not make them correct.")
    S.wide("Tools: let the model call a model", "For a number, a language model should call a calculator.", fig_agent(),
           "The second way to ground a language model is tools. A language model is poor at arithmetic and has no pharmacokinetic model inside it. But it can be given functions to call: a population pharmacokinetic simulator, a database query, a piece of code. The model reads the request, decides which tool to call and with which arguments, receives the result, and writes the answer. A system that chains several such steps is called an agent. The division of labour is the important idea. The language model handles language and orchestration. The number comes from a validated model that you can audit. Every call can be logged, which matters for traceability.",
           band="Language for orchestration, mechanistic models for computation, logs for accountability.")
    S.sec("What goes wrong, uncertainty with conformal prediction, and an honest evaluation.")
    S.tbl("What goes wrong", "Six failure modes of adapted foundation models.", ["Risk", "What happens", "Countermeasure"],
          [["Distribution shift", "Your patients, assays or sites differ from the pre-training data", "External validation; monitoring after deployment"], ["Benchmark contamination", "The test items were in the pre-training corpus", "New, private or time-split test sets"],
           ["Shortcut learning", "The model predicts from a site marker or a text artefact", "Subgroup analysis; perturbation tests"], ["Catastrophic forgetting", "Fine-tuning erases general abilities", "Low learning rate; LoRA; re-test old tasks"],
           ["Miscalibration", "Confident and wrong", "Recalibration; conformal prediction"], ["Hallucination", "Fluent statements without support", "Retrieval, tools, and a reader who checks"]],
          "Six ways an adapted foundation model fails. Distribution shift: your patients, assays or sites differ from what the model saw. Benchmark contamination: the test questions were on the internet and therefore in the pre-training corpus, so the score measures memory. Shortcut learning: the model predicts from a hospital identifier or a formatting artefact. Catastrophic forgetting. Miscalibration: probabilities that do not match frequencies. And hallucination. Each has a countermeasure, in the right column, and none of the countermeasures is exotic: they are good experimental practice. The next slide gives one tool for the fifth line.",
          widths=[22, 42, 36], small=True)
    S.eq("Conformal prediction", "Prediction sets with a coverage guarantee, for any model.", [r"\hat{q} = \mathrm{Quantile}\left(\{s_i\}_{i=1}^{n}\ ;\ \frac{\lceil (n+1)(1-\alpha)\rceil}{n}\right)", r"\mathcal{C}(x) = \{\,y : s(x,y)\leq\hat{q}\,\}\qquad P\left(Y\in\mathcal{C}(X)\right)\geq 1-\alpha"],
         [(r"s_i", "A <b>non-conformity score</b> on calibration example i: for regression, the absolute error."), (r"\hat{q}", "A corrected quantile of the n calibration scores."), (r"\mathcal{C}(x)", "The <b>prediction set</b>: all outcomes whose score is at most q̂. For regression, prediction ± q̂."),
          (r"1-\alpha", "The guaranteed coverage, if calibration and new patients are exchangeable. It holds on average, not for each patient.")],
         "Conformal prediction turns any model into one that outputs sets with a coverage guarantee. Keep aside n calibration patients the model has not seen. On each, compute a score that measures how wrong the model was; for regression, the absolute error. Take a quantile of these scores, slightly corrected for the finite sample: that is q hat. For a new patient, the prediction set contains every outcome whose score is at most q hat; for regression, the prediction plus or minus q hat. The guarantee: the true value falls in the set with probability at least one minus alpha. It holds for any model, with no assumption on the distribution, except one: calibration patients and new patients must be exchangeable. Under shift the guarantee is lost.",
         fig=fig_conf())
    S.tbl("An evaluation an external reviewer accepts", "Five requirements, none specific to foundation models.", ["Requirement", "Why"],
          [["Split by patient; test on another site or period if you can", "Otherwise performance reflects memorized patients"], ["A strong simple baseline on the same splits", "Boosted trees, or a population pharmacokinetic model, are often hard to beat"],
           ["An ablation of the pre-training", "Same architecture from random weights: is the pre-training doing the work?"], ["Calibration and uncertainty, not only discrimination", "A decision needs a probability one can believe"],
           ["Several seeds, with confidence intervals", "Small datasets give noisy estimates"]],
          "Whatever the strategy, the evaluation must convince someone who does not trust you. Five requirements. Split by patient, and if you can, test on another site or a later period. Include a strong simple baseline on exactly the same splits: boosted trees, or a population pharmacokinetic model with Bayesian estimation. Ablate the pre-training: the same architecture from random weights, to show that the pre-training is doing the work. Report calibration and uncertainty, not only discrimination. And run several seeds with confidence intervals, because on a few hundred patients a difference of one point of AUC is usually noise.",
          widths=[48, 52], small=True)
    S.sec("A short implementation, and a decision guide.")
    S.code("LoRA in fourteen lines", "A wrapper around any linear layer.", CODE,
           ["The base layer is <b>frozen</b>.", "<b>A</b> is small and random; <b>B</b> is zero: the wrapped layer starts identical to the original.", "The forward pass adds the low-rank path, scaled by α / r.", "In practice, wrap the query and value projections of each attention block."],
           "Low-rank adaptation as code. A wrapper around an existing linear layer. In the constructor, we freeze the parameters of the base layer, read its dimensions, and create A, small and random, and B, zero. Because B is zero, the wrapped layer initially computes exactly what the original computed. In the forward pass we add the low-rank path, x times A transpose times B transpose, scaled by alpha over r. In practice you apply this to the query and value projections of every attention block, and you train with a learning rate around ten to the minus four. Libraries do this for you; knowing these fourteen lines lets you debug them.")
    S.tbl("A decision guide", "Where to start. Then measure, and climb only if needed.", ["Your situation", "Start with", "Why"],
          [["A question answerable from documents", "Retrieval with a general language model", "Citable sources; nothing to train"], ["Under 1,000 labelled rows, tabular", "Boosted trees, and a tabular foundation model", "Deep fine-tuning will over-fit"],
           ["Hundreds to thousands of labels, and a relevant encoder", "Linear probe, then LoRA", "Label-efficient; few weights to tune"], ["Tens of thousands of labels, shifted domain", "Full fine-tuning, or continued pre-training", "Enough signal to move all weights"],
           ["Large unlabelled domain data, no suitable model", "Pre-train your own", "Costly: justify it with baselines first"]],
          "A decision guide. If the question can be answered from documents, use retrieval with a general language model and train nothing. If you have a small table, under a thousand labelled rows, start with boosted trees and a tabular foundation model. If you have hundreds to thousands of labels and a relevant pre-trained encoder exists, a linear probe and then low-rank adaptation. With tens of thousands of labels in a shifted domain, full fine-tuning or continued pre-training. And if you hold a large unlabelled dataset in a domain where no suitable model exists, patient trajectories in transplantation for example, pre-training your own is justified, after the baselines have been measured.",
          widths=[34, 34, 32], small=True)
    S.ex("Count the weights, set the threshold", ["A model has 12 blocks and width d = 768, about 110 million weights. You apply LoRA with rank r = 8 to the query and value projections of every block. How many weights do you train? What fraction is that?", "A model predicts tacrolimus trough levels. On 19 calibration patients, the sorted absolute errors (ng/mL) are: 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.5, 1.7, 1.9, 2.2, 2.6, 3.1, 4.0.", "For 90 % coverage, which score is q̂? Give the prediction interval for a new patient predicted at 9.0 ng/mL.", "Name one situation in which the 90 % guarantee would no longer hold."],
         dict(time="8 minutes", mat="A calculator", out="A count, a fraction, an interval, one sentence"),
         "Your turn. First, count. A model has twelve blocks and width seven hundred sixty-eight, about a hundred and ten million weights. You apply low-rank adaptation with rank eight to the query and value projections of every block. How many weights do you train, and what fraction is that? Second, conformal prediction. On nineteen calibration patients you have the sorted absolute errors shown. For ninety percent coverage, which score is q hat? Give the interval for a new patient predicted at nine nanograms per millilitre. Third, name one situation in which the guarantee no longer holds.")
    S.sol("Count the weights, set the threshold", ["One matrix: r (d + k) = 8 × (768 + 768) = 12,288. Two matrices in each of 12 blocks: 24 × 12,288 = <b>294,912</b> weights, about <b>0.27 %</b> of 110 million.", "n = 19, α = 0.1: ⌈20 × 0.9⌉ = 18. q̂ is the 18th smallest score: <b>3.1 ng/mL</b>.", "Interval: 9.0 ± 3.1 = <b>[5.9 ; 12.1] ng/mL</b>.", "The guarantee fails under shift: another assay, another centre, a new formulation, a paediatric population."],
          "Solutions. One low-rank pair has eight times seven hundred sixty-eight plus seven hundred sixty-eight weights: twelve thousand two hundred eighty-eight. Two matrices in each of twelve blocks: twenty-four pairs, two hundred ninety-four thousand nine hundred twelve weights. That is about zero point two seven percent of the model. For conformal prediction: n plus one is twenty, times zero point nine is eighteen. q hat is the eighteenth smallest score, three point one. The interval is nine plus or minus three point one. Note how wide it is: the honest uncertainty of a model with these errors. And the guarantee fails whenever new patients are not exchangeable with the calibration patients: another assay, another centre, a new formulation, children.",
          band="A wide interval is information: it says the model is not ready for that decision.")
    S.quiz([("In LoRA, the matrix B is initialized to zero so that:", ["Training is faster", "The adapted model starts identical to the pre-trained one", "The rank is reduced"], 1, "The product BA is zero at the start, so nothing is perturbed."),
            ("Retrieval-augmented generation mainly addresses:", ["Outdated or missing knowledge, and traceability", "The cost of pre-training", "Over-fitting"], 0, "Knowledge lives in an updatable corpus, and answers can cite it."),
            ("The conformal coverage guarantee requires:", ["A well-calibrated model", "Exchangeable calibration and test data", "A Gaussian error"], 1, "It is distribution-free and model-agnostic, but not shift-proof.")],
           "Three questions. B is initialized to zero so that the adapted model starts identical to the pre-trained one. Retrieval mainly addresses outdated or missing knowledge, and traceability. The conformal guarantee requires that calibration and test data be exchangeable; it needs neither a calibrated model nor Gaussian errors.")
    S.take(["A foundation model is pre-trained once on broad data and adapted many times.", "Climb the adaptation ladder from the bottom: prompt, probe, LoRA, fine-tune.", "LoRA trains under 1 % of the weights and starts from the pre-trained model exactly.", "Retrieval and tools ground a language model in sources and in validated computation.", "Trust comes from the evaluation: patient-level splits, baselines, ablation, calibration, external data."],
           "Five takeaways. A foundation model is pre-trained once on broad data and adapted many times. Climb the adaptation ladder from the bottom. Low-rank adaptation trains under one percent of the weights and starts exactly from the pre-trained model. Retrieval and tools ground a language model in sources and in validated computation. And trust comes from the evaluation, not from the size of the model.")
    S.refs(["R. Bommasani et al., “On the Opportunities and Risks of Foundation Models”, arXiv:2108.07258, 2021.", "E. J. Hu et al., “LoRA: Low-Rank Adaptation of Large Language Models”, <i>ICLR</i>, 2022.", "P. Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”, <i>NeurIPS</i>, 2020.",
            "N. Hollmann et al., “Accurate predictions on small data with a tabular foundation model”, <i>Nature</i>, 2025; 637: 319–326.", "A. Shmatko et al., “Learning the natural history of human disease with generative transformers”, <i>Nature</i>, 2025; 647: 248–256.",
            "Z. Lin et al., “Evolutionary-scale prediction of atomic-level protein structure with a language model”, <i>Science</i>, 2023; 379: 1123–1130.", "A. N. Angelopoulos, S. Bates, “A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification”, arXiv:2107.07511, 2021.",
            "M. Oquab et al., “DINOv2: Learning Robust Visual Features without Supervision”, <i>TMLR</i>, 2024."],
           "References: the report that introduced the term foundation model; LoRA; retrieval-augmented generation; TabPFN; Delphi-2M; ESM-2; a tutorial on conformal prediction; and DINOv2.")
    S.end("Session 10 · Multimodal and longitudinal health data: from models to decisions", "That is the end of session nine. One session remains. It brings everything together on the data of clinical pharmacology: irregular, multimodal, longitudinal, and generated by clinicians who were making decisions.")
    return S
