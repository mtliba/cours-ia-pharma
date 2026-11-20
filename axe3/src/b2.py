from lib import *
import numpy as np

TOK = ["Tx day 0", "Tac 8 mg", "C₀ 14.2", "Creat ↑", "Tac 6 mg", "C₀ ?"]
SC = np.array([[0, 0, 0, 0, 0, 0], [1.0, 0.5, 0, 0, 0, 0], [0.2, 2.2, 0.6, 0, 0, 0], [0.3, 1.2, 2.0, 0.5, 0, 0], [0.1, 0.6, 2.4, 1.6, 0.4, 0], [-0.4, 0.8, 1.7, 0.6, 2.0, -1.0]])
MASK = np.triu(np.ones((6, 6)), 1).astype(bool)
A = np.exp(np.where(MASK, -np.inf, SC)); A = A / A.sum(1, keepdims=True)

def shade(v):
    a = np.array([255, 255, 255]); b = np.array([42, 70, 200]); c = (a + (b - a) * min(1, v / 0.6)).astype(int)
    return "#%02X%02X%02X" % tuple(c)

def fig_attn():
    f = Fig(800, 650, "Attention weights between six clinical events; each row sums to one and looks only at earlier events")
    x0, y0, cs = 200, 140, 82
    for i in range(6):
        for j in range(6):
            if j > i: f.rect(x0 + j * cs, y0 + i * cs, cs - 4, cs - 4, "#F2F4F8", None, rx=4)
            else: f.rect(x0 + j * cs, y0 + i * cs, cs - 4, cs - 4, shade(A[i, j]), GRID, 2, 4)
        f.lab(0, y0 + i * cs + 22, TOK[i], 188, "right", "ax ax-b" if i == 5 else "ax")
    for j in range(6):
        f.lab(x0 + j * cs - 8, y0 - 76, TOK[j].replace(" ", "<br>", 1), cs + 12, "center", "ax")
    for j in range(6): f.lab(x0 + j * cs, y0 + 5 * cs + 24, f"{A[5, j]:.2f}", cs - 4, "center", "ax ax-b", WHITE if A[5, j] > 0.3 else INK)
    f.rect(x0 - 4, y0 + 5 * cs - 4, 6 * cs + 4, cs + 4, "none", RED, 4, 6)
    f.lab(200, 14, "columns: the events it can look at", 590, "left", "axh")
    return f

def fig_block():
    f = Fig(1500, 330, "Pre-norm transformer block: normalization, multi-head attention, residual addition, normalization, MLP, residual addition")
    y = 150; h = 100
    items = [(0, 130, "<b>x</b>", WHITE, INK), (190, 150, "Norm", "#F2F4F8", MUTE), (400, 260, "<b>Multi-head<br>attention</b>", PALE, BLUE), (725, 70, "<b>+</b>", WHITE, INK), (860, 150, "Norm", "#F2F4F8", MUTE), (1070, 200, "<b>MLP</b>", PINK, RED), (1335, 70, "<b>+</b>", WHITE, INK)]
    for x, w, t, fill, st in items: f.box(x, y, w, h, t, fill, st, "axw", lines=t.count("<br>") + 1)
    for (x, w, *_), (x2, *_r) in zip(items[:-1], items[1:]): f.arrow(x + w + 4, y + h / 2, x2 - 4, y + h / 2, INK, 4, 14)
    f.arrow(1409, y + h / 2, 1494, y + h / 2, INK, 4, 14)
    for xa, xb in [(150, 760), (820, 1370)]:
        f.path(f"M{xa} {y + h / 2} L{xa} 80 L{xb} 80 L{xb} {y - 22}", BLUE, 4, dash="10 8")
        f.poly([(xb, y - 4), (xb - 9, y - 22), (xb + 9, y - 22)], None, 0, fill=BLUE, close=True)
    f.lab(170, 22, "residual path: the input is added back", 600, "left", "axh")
    f.lab(400, 268, "tokens exchange information", 260, "center", "ax"); f.lab(1040, 268, "each token on its own", 260, "center", "ax")
    return f

def fig_pos():
    f = Fig(800, 520, "Sinusoidal encodings: three dimensions oscillate at three different frequencies along the sequence")
    f.axes(130, 70, 760, 420, (0, 60), (-1.2, 1.2), [0, 20, 40, 60], [-1, 0, 1], "Position, or time since transplant (days)", "Encoding value")
    t = np.linspace(0, 60, 240)
    for k, (c, sw, dash) in zip([2.0, 7.0, 25.0], [(BLUE, 5, None), (RED, 4, None), (INK, 4, "10 8")]):
        f.curve(t, np.sin(t / k), c, sw, dash)
    return f

def fig_mask():
    f = Fig(800, 630, "Causal mask: each position may attend to itself and to earlier positions only")
    x0, y0, cs = 190, 90, 72
    for i in range(6):
        for j in range(6):
            ok = j <= i
            f.rect(x0 + j * cs, y0 + i * cs, cs - 5, cs - 5, PALE if ok else PINK, BLUE if ok else None, 2, 4)
        f.lab(0, y0 + i * cs + 17, f"predicts x{'₂₃₄₅₆₇'[i]}", 178, "right", "ax")
        f.lab(x0 + i * cs, y0 - 44, f"x{'₁₂₃₄₅₆'[i]}", cs - 5, "center", "ax ax-b")
    f.lab(x0, y0 + 6 * cs + 8, "blue: visible", 300, "left", "axh"); f.lab(x0, y0 + 6 * cs + 54, "pink: hidden, it is the future", 560, "left", "axh", RED)
    return f

CODE = '''import math, torch
import torch.nn.functional as F

def attention(X, Wq, Wk, Wv, causal=False):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv   # each (n, d_k)
    S = Q @ K.T / math.sqrt(K.shape[-1])  # (n, n)
    if causal:                         # hide the future
        n = S.shape[0]
        future = torch.triu(torch.ones(n, n), 1).bool()
        S = S.masked_fill(future, float("-inf"))
    A = F.softmax(S, dim=-1)           # rows sum to 1
    return A @ V, A'''

def build():
    S = Session(6, "en", "Part II · Advanced track", "Attention and transformers", "One architecture for text, molecules, proteins, images and patient records.")
    q = np.array([1.0, 0.0]); K = np.array([[2.0, 0], [0, 2.0], [1.0, 1.0]]); v = np.array([10.0, 2.0, 6.0])
    sc = K @ q / np.sqrt(2); w = np.exp(sc) / np.exp(sc).sum(); out = float(w @ v)
    S.sec("Opening: a patient record is a sequence of unequal events.")
    S.cover("Session six. Last time we built the training machinery. Today we build the architecture it is most often applied to: the transformer. The same block processes text, molecules, proteins, images and patient records. Once you understand one equation, attention, and one block, you can read most model papers published since 2017.")
    S.sit("Which past events matter?", "A kidney-transplant record: the transplant date, a tacrolimus dose, a trough level, a rise in creatinine, a dose reduction. Now predict the next trough level.<br><br>A fully connected network needs a fixed-size input. A recurrent network compresses the whole past into one vector and tends to forget early events.",
          "How can a model decide by itself which earlier events matter for the next prediction?",
          "Take a transplant record. The transplant date, a tacrolimus dose, a trough level, a rise in creatinine, a dose reduction. We want the next trough level. Which earlier events matter? The last dose, certainly. The previous level. Perhaps renal function. A fully connected network needs an input of fixed size, and records have different lengths. A recurrent network reads events one by one and squeezes the past into a single vector, so early events fade. Attention answers the question directly: let every element of the sequence look at every other element, and learn where to look.")
    S.obj(["Turn text, molecules, images and clinical events into sequences of tokens.", "Write scaled dot-product attention and explain every term.", "Describe a transformer block and the three model families built from it.", "Estimate the parameter count and the cost of a transformer."],
          "Four objectives. Turn any modality into a sequence of tokens. Write the attention equation and explain every term in it. Describe a transformer block, and the three families of models built from it: encoder-only, decoder-only, encoder-decoder. And estimate the size and the cost of a transformer before you train it.")
    S.plan([("Tokens and embeddings", "Everything becomes a sequence of vectors"), ("Attention", "Queries, keys, values, and multiple heads"), ("The block, and positions", "Residual stack; telling the model about order and time"), ("Three families and their objectives", "Encoder, decoder, encoder–decoder"), ("Cost, code, and limits", "Parameter counts; what attention is not")],
           "Five parts. Tokens and embeddings: how everything becomes a sequence of vectors. Attention itself. The block, and how we tell the model about order and time. The three families and their training objectives. And finally cost, a short implementation, and limits.")
    S.sec("Tokens and embeddings: every modality becomes a sequence of vectors.")
    S.tbl("Everything becomes tokens", "A token is the unit of the sequence; the choice is a modelling decision.", ["Modality", "A token is", "Vocabulary", "Example"],
          [["Text", "a sub-word piece", "30,000 to 100,000", "“tacro” + “limus”"], ["Molecule", "a SMILES symbol, or an atom", "about 100", "C, (, =, O"], ["Protein", "an amino acid", "20, plus special tokens", "M, K, V, L"],
           ["Image", "a 16 × 16 pixel patch", "continuous: linear projection", "224 × 224 image: 196 patches"], ["Patient record", "an event: code, value, time", "thousands of codes", "“tacrolimus C₀ = 14.2, day 31”"]],
          "A transformer reads sequences of tokens. What a token is depends on the modality, and choosing it is a modelling decision. For text, a token is a sub-word piece. For a molecule written as a SMILES string, a character or an atom. For a protein, an amino acid: twenty letters. For an image, a small patch of pixels, flattened and projected. For a patient record, an event: a code for what was measured or given, a value, and a time. The last line is where much current research sits: how to turn a laboratory value with a unit and a timestamp into a token is not settled.",
          widths=[18, 28, 26, 28], small=True)
    S.eq("From token to vector", "A learned table, plus information about position.", r"h_i^{(0)} = E\,[x_i] + p_i",
         [(r"x_i", "The <b>index</b> of the i-th token in the vocabulary: an integer."), (r"E", "The <b>embedding table</b>: one learned vector of size d per vocabulary entry."), (r"p_i", "A <b>positional</b> (or time) encoding: tells the model where, or when, token i occurs."),
          (r"h_i^{(0)}", "The vector that enters the first block. The superscript counts layers.")],
         "First step: turn each token into a vector. x i is an integer, the index of the token in the vocabulary. E is a table with one row per vocabulary entry; each row is a vector of size d, learned by gradient descent like any other weight. We look up row x i. Then we add p i, a vector that encodes the position of the token in the sequence, or for clinical data, the time of the event. We will see why this is needed in a few slides. The result, h i zero, is what enters the first block. From here on the model no longer knows whether it is reading words or lab values.",
         band="After this step every modality is a sequence of vectors.")
    S.sec("Attention: queries, keys and values; multiple heads.")
    S.eq("Scaled dot-product attention", "Each token becomes a weighted average of all tokens, with learned weights.", [r"Q = XW_Q\qquad K = XW_K\qquad V = XW_V", r"\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V"],
         [(r"X", "The n token vectors, stacked as an n × d matrix."), (r"Q,\ K", "<b>Queries</b> (what each token is looking for) and <b>keys</b> (what each token offers): two learned projections of X, of width d_k."),
          (r"\frac{QK^{\top}}{\sqrt{d_k}}", "An n × n table of dot products, one score per pair of tokens, rescaled so that the softmax does not saturate when d_k is large."),
          (r"\mathrm{softmax}", "Applied to each row: scores become positive weights that sum to 1."), (r"V", "<b>Values</b>: the content that is actually mixed.")],
         "This is the equation of the session. X holds the n token vectors, one per row. We project it three times, with three learned matrices, into queries, keys and values. Think of a query as what a token is looking for, a key as what a token advertises, and a value as what it hands over if selected. Q times K transpose is an n by n table of dot products: the score between every pair of tokens. We divide by the square root of the key dimension, otherwise dot products grow with dimension and the softmax saturates. The softmax, row by row, turns scores into weights that sum to one. Multiplying by V gives, for each token, a weighted average of all the values.",
         widget="attention")
    S.pts("Reading an attention map", "Illustrative weights for six events of a transplant record; not a trained model.",
          ["<b>Row</b>: the token being updated. <b>Columns</b>: where it looks.", "Each row sums to 1.", f"The last row, “C₀ ?”, puts {A[5, 4]:.2f} on the last dose and {A[5, 2]:.2f} on the previous level.", "Grey cells are masked: an event cannot look at the future."],
          f"Here is what the softmax output looks like. Rows are the tokens being updated, columns are the tokens they look at. Each row sums to one. Look at the last row, the level we want to predict. It puts {A[5, 4]:.2f} of its weight on the last dose, {A[5, 2]:.2f} on the previous level, and little on the transplant date. The grey cells are masked: an event may not look at the future. A caution that I will repeat: these weights are illustrative, I set the scores by hand. And even in a trained model, an attention map is not an explanation of the prediction.",
          fig=fig_attn())
    S.eq("Multi-head attention", "Several attention operations in parallel, each with its own projections.", [r"\mathrm{head}_h = \mathrm{Attention}\left(XW_Q^h,\ XW_K^h,\ XW_V^h\right)", r"\mathrm{MHA}(X) = \left[\,\mathrm{head}_1;\ \dots;\ \mathrm{head}_H\,\right]W_O"],
         [(r"H", "The number of <b>heads</b>, typically 8 to 16. Each works in a sub-space of width d / H."), (r"[\,\cdot\,;\,\cdot\,]", "Concatenation of the H outputs along the feature dimension."), (r"W_O", "A final learned projection that mixes the heads."),
          (None, "Why several heads: one can follow the last dose, another the trend in renal function, a third the time since transplant.")],
         "One attention operation produces one set of weights per token. But a token may need to look at several things for several reasons. So we run H attention operations in parallel, called heads, each with its own query, key and value projections, each working in a smaller sub-space of width d over H. We concatenate the H outputs and mix them with one more learned matrix. The cost is about the same as a single head of full width. In a clinical sequence, one head might follow the last dose, another the trend in creatinine, another the time since transplant. Nobody assigns these roles; they emerge from training.")
    S.sec("The block, and how the model learns about order and time.")
    S.wide("The transformer block", "Two sub-layers, each wrapped in a residual connection.", fig_block(),
           "Here is the whole block. The input x is normalized, goes through multi-head attention, and the result is added back to x: a residual connection, as in session five. Then a second normalization, a small fully connected network applied to each token separately, and a second residual addition. So the block alternates two operations. Attention moves information between tokens. The MLP transforms each token on its own; it holds about two thirds of the parameters. Stack this block L times and you have a transformer. This is the pre-norm arrangement used in current models; the original 2017 paper normalized after the addition.",
           band="Attention moves information between tokens; the MLP transforms each token on its own.")
    S.eq("Telling the model about order and time", "Attention alone treats its input as an unordered set.", [r"PE(t,\,2i) = \sin\left(\frac{t}{10000^{2i/d}}\right)", r"PE(t,\,2i+1) = \cos\left(\frac{t}{10000^{2i/d}}\right)"],
         [(r"t", "The position in the sequence. For clinical data, use the <b>actual time</b>: days since transplant."), (r"i", "The index of a pair of dimensions; each pair oscillates at its own frequency."), (None, "Alternatives: learned position vectors, relative positions, rotary embeddings (RoPE).")],
         "A detail that matters a great deal for clinical data. Shuffle the rows of X and the attention output is shuffled the same way: attention has no notion of order. We must inject it. The original recipe adds to each token a vector of sines and cosines of its position, at geometrically spaced frequencies; the figure shows three of them. Low frequencies encode coarse position, high frequencies fine position. For text, t is the rank of the word. For a patient record, use the actual time: days since transplant, not visit number. Two visits three days apart and two visits three months apart are not the same thing, and visit rank cannot tell them apart.",
         fig=fig_pos(), band="For irregular clinical data, encode real time, not rank.")
    S.sec("Three families of transformers and their training objectives.")
    S.cols("Three families", "Same block; different masking and different objective.",
           [("Encoder-only", "Every token sees the whole sequence.<br><br>Trained by masking tokens and predicting them (BERT).<br><br>Use: representations, classification, retrieval."),
            ("Decoder-only", "Every token sees only what precedes it (causal mask).<br><br>Trained to predict the next token (GPT).<br><br>Use: generation; also forecasting the next clinical event."),
            ("Encoder–decoder", "An encoder reads the input; a decoder generates the output and attends to the encoder through cross-attention.<br><br>Use: translation, summarization, reaction prediction.")],
           "Three families are built from the same block. Encoder-only models let every token see the whole sequence. They are trained by hiding some tokens and predicting them; BERT is the reference. They produce representations: use them for classification or retrieval. Decoder-only models apply a causal mask, so each token sees only its past, and are trained to predict the next token; that is the GPT family and every current chat assistant. They generate, and they are also the natural choice for forecasting the next clinical event. Encoder-decoder models read an input with an encoder and generate an output with a decoder that attends to the encoder; translation is the typical use.")
    S.eq("Two self-supervised objectives", "No labels needed: the sequence supervises itself.", [r"\mathcal{L}_{\mathrm{CLM}} = -\sum_{t=1}^{T}\log p_\theta\left(x_t\,|\,x_{<t}\right)", r"\mathcal{L}_{\mathrm{MLM}} = -\sum_{i\in M}\log p_\theta\left(x_i\,|\,x_{\setminus M}\right)"],
         [(r"x_{<t}", "All tokens before position t: the <b>causal</b> context."), (r"M", "A random set of <b>masked</b> positions, 15 % in BERT."), (r"x_{\setminus M}", "The sequence with the masked positions hidden.")],
         "Both families are trained without labels. Causal language modelling, first line: for every position, predict the token given everything before it, and sum the negative log-probabilities. The causal mask on the left makes this efficient: one forward pass gives the predictions for all positions at once, because position t is prevented from seeing positions after t. Masked language modelling, second line: hide a random set M of positions, fifteen percent in BERT, and predict them from the rest. Both are cross-entropy losses from session five. This is self-supervised learning, the subject of the next session.",
         fig=fig_mask())
    S.sec("Cost, a short implementation, applications beyond text, and limits.")
    S.tbl("How big, how expensive?", "Two formulas to remember before you launch a job.", ["Quantity", "Rule of thumb", "Example"],
          [["Parameters per block", "about 12 d² (4 d² attention + 8 d² MLP)", "d = 768: 7.1 million"], ["Parameters, L blocks", "about 12 L d², plus embeddings", "L = 12, d = 768: 85 million; about 110 million with embeddings (BERT-base)"],
           ["Attention cost per layer", "time and memory grow as n² · d", "Doubling the context multiplies the cost by 4"], ["Sequence length n", "depends on tokenization", "6 visits × 20 events = 120 tokens; a whole-slide image: millions of patches"]],
          "Two rules of thumb. Parameters: each block has four d-squared weights in attention, for the query, key, value and output projections, and eight d-squared in an MLP with the usual four-fold expansion. Twelve d-squared per block. With d seven hundred sixty-eight and twelve blocks, that is eighty-five million, and about a hundred and ten million with the embedding table: BERT-base. Cost: attention compares every token with every other, so time and memory grow with the square of the sequence length. Clinical sequences are short; a whole-slide image is millions of patches and needs a hierarchy.",
          widths=[24, 36, 40], small=True, band="For clinical sequences the bottleneck is the amount of data, not the context length.")
    S.code("Attention in twelve lines", "The equation, as code.", CODE,
           ["Three matrix products give <b>Q, K, V</b>.", "<b>S</b> holds the n × n scores, scaled by √d_k.", "The causal mask writes −∞ above the diagonal: after the softmax those weights are exactly 0.", "The function returns the new token vectors and the attention map <b>A</b>."],
           "The equation as code. Three matrix products give queries, keys and values. S is the table of scaled scores. For a causal model we build an upper-triangular mask and write minus infinity in those positions; after the softmax these weights are exactly zero. Softmax along the last dimension makes each row sum to one. We return A times V, the updated token vectors, together with the attention map. In practice you call the built-in scaled dot product attention function, which does the same thing with faster kernels. But you should be able to write these twelve lines from memory.")
    S.pts("The same block, beyond text", "What changes is the tokenizer and the positional information.",
          ["<b>Images</b>: patches as tokens (Vision Transformer, 2021).", "<b>Proteins</b>: amino acids as tokens; ESM-2 predicts structure from a single sequence (Lin et al., Science, 2023).", "<b>Molecules</b>: SMILES language models, and attention over atoms with bond and distance information.", "<b>Health records</b>: Delphi-2M, a modified GPT trained on 0.4 million UK Biobank participants (Shmatko et al., Nature, 2025)."],
          "The same block works well beyond text. For images, the Vision Transformer cuts the image into patches and treats them as tokens. For proteins, amino acids are tokens; the ESM-2 language model, trained only to fill in masked residues, learns enough to predict three-dimensional structure. For molecules, there are language models over SMILES strings, and attention over atoms with bond and distance information added to the scores. For health records, Delphi-2M modifies the GPT architecture to model disease histories; it was trained on four hundred thousand UK Biobank participants and validated on one point nine million Danish individuals without changing its parameters.")
    S.pts("What attention is not", "Four cautions before you use a transformer on clinical data.",
          ["<b>An attention map is not an explanation.</b> Different weight patterns can give the same prediction.", "<b>Weak built-in assumptions.</b> A transformer needs more data, or pretraining, than a tree ensemble or a mechanistic model.", "<b>No notion of time, dose–response or mass balance</b> unless you encode it.", "<b>Quadratic cost</b> in sequence length."],
          "Four cautions. First, an attention map is not an explanation. It has been shown that very different attention patterns can produce the same prediction; treat maps as a debugging aid, not as evidence for a clinician. Second, a transformer assumes very little about its input. That is why it is general, and why it needs a lot of data or pretraining. On five hundred patients and twelve variables, boosted trees or a population pharmacokinetic model will win. Third, it knows nothing about time, dose-response or mass balance unless you encode them; session ten returns to this. Fourth, the quadratic cost.")
    S.ex("Attention by hand", ["A query q = (1, 0). Three keys: k₁ = (2, 0), k₂ = (0, 2), k₃ = (1, 1). Here d_k = 2.", "Compute the three scores q · k / √d_k, then the softmax weights.", "The values are three earlier trough levels: 10, 2 and 6 ng/mL. What is the output?", "A model has L = 6 blocks and d = 256. Estimate its number of parameters, without embeddings."],
         dict(time="8 minutes", mat="A calculator with exp", out="Three weights, one output, one parameter count"),
         "Your turn. One query, the vector one, zero. Three keys: two, zero; zero, two; and one, one. The key dimension is two. Compute the three scaled scores, then the softmax weights. The values are three earlier trough levels: ten, two and six nanograms per millilitre. What is the output? Last question: a model has six blocks and width two hundred fifty-six. Estimate its parameter count, without embeddings. Eight minutes.")
    S.sol("Attention by hand", [f"Dot products: 2, 0, 1. Divided by √2: <b>{sc[0]:.2f}, {sc[1]:.2f}, {sc[2]:.2f}</b>.", f"Exponentials: {np.exp(sc[0]):.2f}, {np.exp(sc[1]):.2f}, {np.exp(sc[2]):.2f}; sum {np.exp(sc).sum():.2f}. Weights: <b>{w[0]:.2f}, {w[1]:.2f}, {w[2]:.2f}</b>.", f"Output: {w[0]:.2f} × 10 + {w[1]:.2f} × 2 + {w[2]:.2f} × 6 = <b>{out:.1f} ng/mL</b>.", f"Parameters: 12 × 6 × 256² = <b>{12 * 6 * 256 ** 2 / 1e6:.1f} million</b>."],
          f"Solution. The dot products are two, zero and one. Divided by the square root of two: {sc[0]:.2f}, zero and {sc[2]:.2f}. The exponentials sum to {np.exp(sc).sum():.2f}, so the weights are {w[0]:.2f}, {w[1]:.2f} and {w[2]:.2f}. The output is the weighted average of the values: {out:.1f} nanograms per millilitre, pulled toward the first value because its key is most aligned with the query. For the parameter count: twelve times six times two hundred fifty-six squared, about {12 * 6 * 256 ** 2 / 1e6:.1f} million. A small model by today's standards, and already large for a dataset of a few thousand patients.",
          band="The output is a weighted average of the values, with weights set by query–key agreement.")
    S.quiz([("Why divide the scores by √d_k?", ["To make the weights sum to 1", "To keep the softmax from saturating as d_k grows", "To encode position"], 1, "Dot products grow with dimension; rescaling keeps gradients healthy."),
            ("Without positional information, self-attention is:", ["Causal", "Insensitive to the order of the tokens", "Linear in sequence length"], 1, "Permuting the inputs permutes the outputs: order must be injected."),
            ("A decoder-only model is trained to:", ["Reconstruct masked tokens from both sides", "Predict each token from the preceding ones", "Classify the whole sequence"], 1, "Causal language modelling, with a triangular mask.")],
           "Three questions. We divide by the square root of the key dimension to keep the softmax from saturating. Without positional information, self-attention is insensitive to the order of the tokens. A decoder-only model is trained to predict each token from the preceding ones.")
    S.take(["Every modality becomes a sequence of token vectors; tokenization is a modelling decision.", "Attention replaces each token by a weighted average of values, with weights from query–key dot products.", "A transformer is a stack of pre-norm residual blocks: attention, then MLP.", "Encoder-only for representations, decoder-only for generation and forecasting.", "About 12 L d² parameters; cost quadratic in length; encode real time for clinical data."],
           "Five takeaways. Every modality becomes a sequence of token vectors, and tokenization is a modelling decision. Attention replaces each token by a weighted average of values, with weights given by query-key dot products. A transformer is a stack of pre-norm residual blocks: attention, then MLP. Encoder-only models for representations, decoder-only models for generation and forecasting. About twelve L d-squared parameters, a cost quadratic in length, and for clinical data, encode real time.")
    S.refs(["A. Vaswani et al., “Attention Is All You Need”, <i>NeurIPS</i>, 2017.", "J. Devlin, M.-W. Chang, K. Lee, K. Toutanova, “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding”, <i>NAACL</i>, 2019.",
            "A. Dosovitskiy et al., “An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale”, <i>ICLR</i>, 2021.", "Z. Lin et al., “Evolutionary-scale prediction of atomic-level protein structure with a language model”, <i>Science</i>, 2023; 379: 1123–1130.",
            "A. Shmatko et al., “Learning the natural history of human disease with generative transformers”, <i>Nature</i>, 2025; 647: 248–256.", "S. Jain, B. C. Wallace, “Attention is not Explanation”, <i>NAACL</i>, 2019."],
           "References: the original transformer paper, BERT, the Vision Transformer, the ESM-2 protein language model, Delphi-2M for health trajectories, and the paper that showed attention weights are not explanations.")
    S.end("Session 7 · Representation learning and self-supervision", "That is the end of session six. We have an architecture and two self-supervised objectives. Next session we ask the general question behind them: what is a good representation, and how do we learn one without labels?")
    return S
