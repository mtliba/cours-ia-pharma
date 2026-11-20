from lib import *
import numpy as np

SIMS = [0.9, 0.7, 0.3, 0.0, -0.2, -0.5]

def fig_contrast():
    f = Fig(800, 600, "Embedding space: the two views of one example are pulled together, other examples are pushed away")
    f.circle(400, 250, 235, "#F2F4F8", GRID, 3)
    a, p = (345, 215), (450, 180)
    negs = [(545, 335), (265, 370), (455, 415), (235, 150), (575, 165)]
    for n in negs:
        dx, dy = n[0] - a[0], n[1] - a[1]; d = (dx * dx + dy * dy) ** 0.5
        f.arrow(n[0] - dx / d * 74, n[1] - dy / d * 74, n[0] - dx / d * 24, n[1] - dy / d * 24, RED, 4, 14)
        f.circle(n[0], n[1], 15, INK)
    f.arrow(a[0] + 20, a[1] - 7, p[0] - 22, p[1] + 8, BLUE, 5, 14); f.arrow(p[0] - 20, p[1] + 7, a[0] + 22, a[1] - 8, BLUE, 5, 14)
    f.circle(a[0], a[1], 18, BLUE); f.circle(p[0], p[1], 18, BLUE)
    f.lab(0, 500, "blue: two views of one patient, pulled together", 800, "center", "axh")
    f.lab(0, 548, "black: other patients, pushed away", 800, "center", "axh", RED)
    return f

def fig_temp():
    f = Fig(800, 620, "Softmax probabilities over one positive and five negatives for three temperatures")
    f.axes(130, 70, 760, 480, (0, 6), (0, 1), [], [0.0, 0.25, 0.5, 0.75, 1.0], "", "Probability assigned to each candidate", fmt=lambda v: f"{v:.2f}")
    s = np.array(SIMS)
    for ti, (tau, col) in enumerate([(0.05, BLUE), (0.2, AMBER), (1.0, GREY)]):
        p = np.exp(s / tau); p /= p.sum()
        for k in range(6):
            x = f.X(k + 0.14 + ti * 0.25); w = (f.X(1) - f.X(0)) * 0.22
            f.rect(x, f.Y(p[k]), w, f.Y(0) - f.Y(p[k]), col, None)
    names = ["0.9<br>positive", "0.7<br>hard", "0.3", "0.0", "−0.2", "−0.5"]
    for k in range(6): f.lab(f.X(k), 490, names[k], f.X(1) - f.X(0), "center", "ax ax-b" if k == 0 else "ax")
    for ti, (t, col) in enumerate([("τ = 0.05", BLUE), ("τ = 0.2", AMBER), ("τ = 1", GREY)]):
        f.rect(470, 96 + ti * 46, 30, 30, col, None); f.lab(512, 96 + ti * 46, t, 200, "left", "ax ax-b")
    f.lab(130, 572, "cosine similarity with the anchor", 630, "center", "ax ax-b")
    return f

def fig_unif():
    f = Fig(800, 440, "Two embedding distributions on a circle: collapsed to one region, and spread uniformly")
    r = np.random.default_rng(2)
    for cx, title, ang in [(200, "collapsed", r.normal(0.6, 0.12, 22)), (600, "aligned and uniform", np.repeat(np.linspace(0, 2 * np.pi, 11, endpoint=False), 2) + np.tile([-0.07, 0.07], 11))]:
        f.circle(cx, 200, 150, "#F2F4F8", GRID, 3)
        for a in ang: f.circle(cx + 150 * np.cos(a), 200 - 150 * np.sin(a), 10, RED if cx == 200 else BLUE, WHITE, 2)
        f.lab(cx - 190, 376, title, 380, "center", "axh", RED if cx == 200 else BLUE)
    return f

def grid(f, x0, y0, n, cs, masked, colors=(PALE, BLUE)):
    for i in range(n):
        for j in range(n):
            m = (i * n + j) in masked
            f.rect(x0 + j * cs, y0 + i * cs, cs - 5, cs - 5, "#DFE2EA" if m else colors[0], None if m else colors[1], 2, 4)

def fig_mae():
    f = Fig(800, 420, "Masked autoencoder: most patches hidden, encoder sees the visible ones, a light decoder reconstructs the rest")
    r = np.random.default_rng(4); masked = set(r.choice(16, 12, replace=False).tolist())
    grid(f, 0, 120, 4, 46, masked)
    f.arrow(190, 210, 226, 210, INK, 4)
    f.box(232, 155, 180, 110, "<b>Encoder</b><br>visible only", PALE, BLUE, "axw", lines=2)
    f.arrow(418, 210, 446, 210, INK, 4)
    f.box(452, 170, 130, 80, "Decoder", "#F2F4F8", MUTE, "axw")
    f.arrow(588, 210, 616, 210, INK, 4)
    grid(f, 624, 126, 4, 43, set(), (PINK, RED))
    f.lab(0, 322, "75 % hidden", 184, "center", "ax ax-b"); f.lab(610, 322, "reconstruction", 190, "center", "ax ax-b", RED)
    f.lab(0, 60, "input patches", 184, "center", "ax ax-b"); f.lab(232, 86, "we keep this", 200, "left", "axh")
    return f

def fig_jepa():
    f = Fig(800, 540, "Joint-embedding predictive architecture: a predictor maps the context representation to the target representation")
    f.box(0, 60, 190, 90, "context<br>(visible part)", WHITE, INK, "axw", lines=2); f.box(0, 360, 190, 90, "target<br>(hidden part)", WHITE, INK, "axw", lines=2)
    f.box(260, 50, 230, 110, "<b>Context<br>encoder</b>", PALE, BLUE, "axw", lines=2); f.box(260, 350, 230, 110, "<b>Target encoder</b><br>moving average", "#F2F4F8", MUTE, "axw", lines=2)
    f.box(570, 50, 200, 110, "<b>Predictor</b>", PINK, RED, "axw")
    f.arrow(194, 105, 254, 105, INK, 4); f.arrow(194, 405, 254, 405, INK, 4); f.arrow(494, 105, 564, 105, INK, 4)
    f.arrow(670, 164, 670, 262, RED, 4); f.arrow(494, 405, 640, 336, MUTE, 4)
    f.box(536, 266, 264, 64, "<b>loss in latent space</b>", WHITE, RED, "ax ax-b")
    f.arrow(375, 344, 375, 166, MUTE, 4, dash="8 8")
    f.lab(170, 236, "slow copy", 190, "right", "axh", MUTE)
    f.lab(0, 484, "no pixel or value is reconstructed", 780, "left", "axh")
    return f

def fig_label():
    f = Fig(800, 600, "Schematic: performance against number of labels, with and without self-supervised pre-training")
    n = np.linspace(1, 4, 60)
    f.axes(130, 70, 760, 500, (1, 4), (0.5, 1.0), [1, 2, 3, 4], [0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "Number of labelled examples", "Performance (AUC)", fmt=lambda v: {1: "10", 2: "100", 3: "1,000", 4: "10,000"}[v], fmty=lambda v: f"{v:.1f}")
    pre = 0.9 - 0.2 * np.exp(-(n - 1) / 0.7); scr = 0.9 - 0.4 * np.exp(-(n - 1) / 1.5)
    f.curve(n, pre, BLUE, 6); f.curve(n, scr, GREY, 5, "12 9")
    f.lab(f.X(1.5), f.Y(0.985), "pre-trained, then adapted", 440, cls="axh")
    f.lab(f.X(2.2), f.Y(0.66), "trained from scratch", 380, cls="axh", color=GREY)
    return f

CODE = '''import torch
import torch.nn.functional as F

def info_nce(z1, z2, tau=0.2):
    # z1, z2: (N, d) embeddings of two views
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    sim = z @ z.T / tau                # (2N, 2N) logits
    sim.fill_diagonal_(float("-inf"))  # no self-pairs
    N = z1.shape[0]
    pos = torch.arange(2 * N).roll(N)  # the positive
    return F.cross_entropy(sim, pos)'''

def nce(tau):
    s = np.array([0.8, 0.2, 0.0, -0.4]); e = np.exp(s / tau); return e, e[0] / e.sum(), -np.log(e[0] / e.sum())

def build():
    S = Session(7, "en", "Part II · Advanced track", "Representation learning and self-supervision", "Learning from unlabelled data: contrastive, non-contrastive, masked and predictive objectives.")
    e2, p2, l2 = nce(0.2); e1, p1, l1 = nce(1.0)
    s = np.array(SIMS); pp = {t: (np.exp(s / t) / np.exp(s / t).sum()) for t in (0.05, 0.2, 1.0)}
    S.sec("Opening: many records, few labels.")
    S.cover("Session seven. This is the conceptual centre of the course. Foundation models, in session nine, are large encoders trained with the objectives we study today. The question is simple to state: how do we learn a useful description of data without labels? I will insist on what each objective assumes, because those assumptions are where transfer to clinical and pharmacological data succeeds or fails.")
    S.sit("Many records, few labels", "A hospital holds follow-up records for tens of thousands of transplant recipients: doses, drug levels, laboratory values, reports.<br><br>Graft loss is recorded for a few thousand of them. Biopsy-proven rejection is annotated for a few hundred.",
          "How can the unlabelled majority make the labelled minority sufficient?",
          "Here is the usual situation in clinical research. Tens of thousands of patients with rich follow-up: doses, drug levels, laboratory values, reports. But the outcome you care about is available for a few thousand, and a carefully annotated one, such as biopsy-proven rejection, for a few hundred. Training a deep network on a few hundred labels fails. Yet the unlabelled records contain a great deal of structure: how creatinine evolves, how levels respond to dose changes. Self-supervised learning uses that structure to build an encoder first, so that a few hundred labels are enough afterwards.")
    S.obj(["Define a representation, and state what makes one good.", "Write the InfoNCE loss and explain the role of the temperature.", "Explain how non-contrastive, masked and predictive methods avoid collapse.", "Choose views, masks and evaluation protocols for a modality that is not an image."],
          "Four objectives. Define a representation and say what makes one good. Write the contrastive loss, InfoNCE, and explain what the temperature does. Explain how the other families, non-contrastive, masked, and predictive, avoid the trivial solution called collapse. And, most important for your own work, choose views, masks and evaluation protocols for data that are not natural images.")
    S.plan([("What is a good representation?", "The pre-train, then adapt pipeline"), ("Contrastive learning", "InfoNCE, temperature, alignment and uniformity"), ("Learning without negatives", "Self-distillation and explicit regularizers"), ("Masked and predictive objectives", "MAE, JEPA, and contrastive pairs across modalities"), ("Views, evaluation, pitfalls", "The augmentation question outside images")],
           "Five parts. What a representation is, and the pipeline it serves. Contrastive learning, in detail. Methods that work without negative pairs. Masked and predictive objectives, and contrastive learning across modalities. And finally the practical questions: which views, which evaluation, which pitfalls.")
    S.sec("What a representation is, and what makes it good.")
    S.wide("Pre-train once, adapt many times", "The encoder is trained without labels; only a small head needs them.",
           flow(["<b>x</b><br>raw record", "<b>Encoder f</b><br>pre-trained,<br>no labels", "<b>z = f(x)</b><br>representation", "<b>Small head</b><br>few labels", "<b>ŷ</b><br>prediction"], 1500, 290, "Pipeline: raw data, pre-trained encoder, representation, small head, prediction", subs=["images, sequences, molecules", "the expensive step, done once", "a vector of a few hundred numbers", "linear layer or small network", "one head per task"], gap=44),
           "The pipeline has two stages. First, an encoder f is trained on unlabelled data with a self-supervised objective. This is the expensive step, and it is done once. The encoder maps a raw input x, an image, a sequence, a molecule, to a vector z of a few hundred numbers: the representation. Second, for each task, a small head is trained on top of z with the few labels available: a linear layer, or a small network. The same encoder serves many tasks: graft-loss prediction, rejection, phenotyping, retrieval of similar patients. Everything in this session is about the first stage.",
           band="The representation z is the product. The pre-training objective is only a means to obtain it.")
    S.cols("What makes a representation good?", "Three properties, in decreasing order of how easily they are measured.",
           [("Useful with a simple head", "A linear classifier on z does well, with few labels. Information is not only present, it is easy to extract."),
            ("Invariant to nuisance, sensitive to signal", "z should ignore the assay batch or the scanner, and keep the dose, the timing, the lesion. Deciding which is which is the whole difficulty."),
            ("Transferable", "z still works on another hospital, another period, another task. This is the property clinicians need and the one papers test least.")],
           "What makes a representation good? Three properties. First, it is useful with a simple head: a linear classifier on top does well with few labels. The information is not only present, it is easy to extract. Second, it is invariant to nuisance factors and sensitive to signal. It should ignore the assay batch or the scanner model and keep the dose, the timing, the lesion. Deciding what is nuisance and what is signal is the whole difficulty, and we will return to it. Third, it transfers: to another hospital, another period, another task. This is what clinical use requires, and what papers test least.")
    S.tbl("Four families of self-supervised learning", "They differ in the training signal and in how they avoid the trivial solution.", ["Family", "Training signal", "How collapse is avoided", "Examples"],
          [["Contrastive", "Views of the same example match; views of different examples do not", "Negative pairs", "SimCLR, MoCo, CLIP"],
           ["Non-contrastive", "Views of the same example match", "Asymmetry between branches, or explicit variance terms", "BYOL, DINO, VICReg"],
           ["Masked modelling", "Reconstruct hidden parts of the input", "The target is the data itself", "BERT, MAE"],
           ["Latent prediction", "Predict the representation of hidden parts", "Slowly moving target encoder", "I-JEPA"]],
          "Four families. Contrastive methods say: two views of the same example should have similar representations, and views of different examples should not. Non-contrastive methods keep only the first half. That raises a problem: mapping every input to the same vector satisfies the objective perfectly. This is collapse, and each method has a mechanism against it. Masked modelling hides part of the input and reconstructs it; the target is the data, so collapse is not an issue. Latent prediction hides part of the input and predicts its representation rather than its raw values. Keep this table in mind; the rest of the session fills it in.",
          widths=[18, 34, 28, 20], small=True)
    S.sec("Contrastive learning: InfoNCE, temperature, alignment and uniformity.")
    S.pts("The contrastive principle", "Two views of one example are a positive pair; everything else in the batch is a negative.",
          ["Build two <b>views</b> of each example: two crops of an image, two masked versions of a record.", "Pull the two views together in embedding space.", "Push the views of other examples away.", "No label is used: the pairing comes from the data."],
          "The contrastive principle. Take an example and build two views of it: two random crops of an image, or two differently masked versions of a patient record. Encode both. These two embeddings form a positive pair, in blue. All other embeddings in the batch come from other examples: they are negatives, in black. The loss pulls the positive pair together and pushes the negatives away. No label is used anywhere; the supervision is the knowledge of which views came from the same example. Everything the model learns is therefore determined by how you build the views.",
          fig=fig_contrast())
    S.eq("The InfoNCE loss", "A classification problem: find the positive among all candidates.", r"\ell_{i,j} = -\log\frac{\exp\left(\mathrm{sim}(z_i,z_j)/\tau\right)}{\sum_{k\neq i}\exp\left(\mathrm{sim}(z_i,z_k)/\tau\right)}",
         [(r"z_i,\ z_j", "Embeddings of the <b>two views</b> of the same example: the positive pair."), (r"\mathrm{sim}(u,v)", "<b>Cosine similarity</b>: the dot product of the two vectors after normalizing them to length 1."),
          (r"\sum_{k\neq i}", "Sum over all other embeddings in the batch: the positive and 2N − 2 negatives, for a batch of N examples."), (r"\tau", "The <b>temperature</b>: a small positive number that sharpens the distribution.")],
         "Here is the loss. Read it as a classification problem. For the anchor z i, there are two N minus one candidates in the batch: one positive, z j, and the rest negatives. We compute the cosine similarity of the anchor with each candidate, divide by a temperature tau, and apply a softmax. The loss is the negative log-probability assigned to the positive. It is the cross-entropy of session five, where the classes are the candidates. Minimizing it maximizes a lower bound on the mutual information between the two views, and that bound cannot exceed the logarithm of the number of candidates: one reason large batches help.",
         band="Cross-entropy over candidates: the label is “which one is the other view of me?”")
    S.pts("What the temperature does", "One positive (similarity 0.9) and five negatives; the same similarities, three temperatures.",
          [f"<b>τ = 0.05</b>: the positive gets {pp[0.05][0]:.2f}, the hard negative {pp[0.05][1]:.2f}. Only the hard negative produces gradient.", f"<b>τ = 1</b>: the positive gets only {pp[1.0][0]:.2f}; all negatives count almost equally.", "Small τ: sharper separation, but similar examples are torn apart.", "Typical values: 0.05 to 0.2. Treat it as a hyperparameter of first importance."],
          f"The temperature is not a detail. Here are the softmax probabilities for one positive, with similarity zero point nine, and five negatives, for three temperatures. In blue, tau equals zero point zero five: the positive gets {pp[0.05][0]:.2f} and almost all the rest goes to the hardest negative, the one with similarity zero point seven. The gradient comes from hard negatives only. In grey, tau equals one: the distribution is nearly flat, the positive gets {pp[1.0][0]:.2f}, and every negative counts about the same. A low temperature separates fine-grained differences, but it also pushes apart examples that truly are similar, two patients with the same phenotype for instance. Typical values lie between zero point zero five and zero point two.",
          fig=fig_temp(), widget="temperature")
    S.eq("Alignment and uniformity", "What the contrastive loss optimizes, split in two.", [r"\mathcal{L}_{\mathrm{align}} = \mathbb{E}_{(x,\,x^{+})}\left\Vert f(x)-f(x^{+})\right\Vert^2", r"\mathcal{L}_{\mathrm{unif}} = \log\,\mathbb{E}_{x,\,y}\,\exp\left(-2\left\Vert f(x)-f(y)\right\Vert^2\right)"],
         [(r"f(x)", "The embedding, normalized to length 1: a point on a sphere."), (r"(x,\,x^{+})", "A positive pair. <b>Alignment</b>: positives should be close."), (r"x,\ y", "Two independent examples. <b>Uniformity</b>: embeddings should spread over the whole sphere.")],
         "A useful way to understand the contrastive loss, due to Wang and Isola. It does two things. Alignment: the two views of an example should land close to each other; the first line is their mean squared distance. Uniformity: embeddings of different examples should spread evenly over the sphere; the second line is small when points are far apart. On the left, a collapsed representation: perfectly aligned, not uniform at all, and useless. On the right, what we want. These two numbers can be computed on any encoder and are good diagnostics during pre-training, long before you have a downstream result.",
         fig=fig_unif(), band="Collapse satisfies alignment and fails uniformity.")
    S.sec("Learning without negatives: self-distillation and explicit regularizers.")
    S.tbl("Learning without negatives", "Each method replaces negatives by another mechanism against collapse.", ["Method", "Mechanism against collapse", "Remark"],
          [["BYOL, SimSiam", "A predictor on one branch and a stop-gradient on the other; in BYOL the target is a moving average of the online network", "Works with small batches"],
           ["DINO, DINOv2", "The teacher is a moving average of the student; its outputs are centred and sharpened", "Strong general-purpose image features"],
           ["Barlow Twins", "The cross-correlation matrix between the two views is driven to the identity", "Decorrelates the dimensions"],
           ["VICReg", "Explicit variance, invariance and covariance terms", "The most transparent objective"]],
          "Negatives have a cost: large batches, and the risk of pushing apart examples that are truly similar. Can we do without them? Yes, with care. BYOL and SimSiam make the two branches asymmetric: one has an extra predictor, and the gradient is stopped on the other. In BYOL the target branch is a slowly moving average of the online one. DINO uses a moving-average teacher and centres and sharpens its outputs; DINOv2 is today a standard source of image features. Barlow Twins makes the cross-correlation matrix of the two views close to the identity. VICReg, on the next slide, writes each requirement as an explicit term.",
          widths=[20, 54, 26], small=True)
    S.eq("VICReg: each requirement as one term", "The clearest statement of what a joint-embedding method needs.", r"\mathcal{L} = \lambda\,s(Z,Z^{\prime}) + \mu\left[v(Z)+v(Z^{\prime})\right] + \nu\left[c(Z)+c(Z^{\prime})\right]",
         [(r"Z,\ Z^{\prime}", "The batch of embeddings for the first and second views."), (r"s", "<b>Invariance</b>: mean squared distance between the two views of each example."),
          (r"v", "<b>Variance</b>: keeps the standard deviation of every dimension, across the batch, above a threshold. This term forbids collapse."), (r"c", "<b>Covariance</b>: penalizes correlations between dimensions, so that they carry different information.")],
         "VICReg is worth knowing because it states the requirements one by one. Z and Z prime are the embeddings of the two views for a whole batch. The first term, s, is invariance: the two views of each example should match. Alone, it leads to collapse. The second term, v, is variance: each dimension of the embedding must keep a standard deviation above a threshold across the batch. A constant embedding has zero variance, so this term forbids collapse. The third term, c, penalizes covariance between dimensions, so that the dimensions do not all encode the same thing. This last failure, where the embedding uses only a few directions, is called dimensional collapse.",
         band="Invariance alone collapses. Variance prevents it. Covariance spreads information across dimensions.")
    S.sec("Masked and predictive objectives; contrastive learning across modalities.")
    S.eq("Masked modelling", "Hide most of the input, reconstruct it.", r"\mathcal{L} = \mathbb{E}_{x,\,M}\sum_{i\in M}\left\Vert x_i - g_\phi\left(f_\theta(x_{\setminus M})\right)_i\right\Vert^2",
         [(r"M", "The set of <b>masked</b> positions: 75 % of patches in MAE, 15 % of tokens in BERT."), (r"f_\theta", "The <b>encoder</b>; it sees only the visible part."), (r"g_\phi", "A light <b>decoder</b>, discarded after pre-training.")],
         "The second large family: masked modelling. Hide a random set M of positions; the encoder sees only the visible part; a light decoder predicts the hidden values; the loss is the reconstruction error on the masked positions. For categorical tokens, replace the squared error by a cross-entropy: that is BERT. The decoder is thrown away afterwards; we keep the encoder. One parameter matters: the mask ratio. Images are highly redundant, so the masked autoencoder hides seventy-five percent of the patches, otherwise the task is solved by local interpolation. Text is dense, so BERT hides fifteen percent. For a new modality, ask how redundant it is.",
         fig=fig_mae(), band="The mask ratio sets the difficulty: high for redundant signals, low for dense ones.")
    S.pts("Predicting in latent space: JEPA", "Predict the representation of the hidden part, not its raw values.",
          ["A <b>context encoder</b> reads the visible part.", "A <b>target encoder</b>, a moving average of the first, reads the hidden part.", "A <b>predictor</b> maps one representation to the other; the loss is computed between representations.", "Unpredictable detail, such as measurement noise, does not have to be modelled."],
          "A more recent idea: joint-embedding predictive architectures. Masked autoencoders reconstruct raw values, so they spend capacity on details that may be pure noise. Here the context encoder reads the visible part; a target encoder, which is a slowly moving average of the context encoder, reads the hidden part; and a predictor maps the context representation to the target representation. The loss is computed between representations. Nothing is reconstructed in input space. The attraction for clinical measurements is clear: assay noise and irrelevant fluctuation do not need to be predicted. Collapse is avoided by the moving-average target, as in BYOL.",
          fig=fig_jepa())
    S.eq("Contrastive learning across modalities", "The two “views” are two modalities of the same object.", r"\ell(u_i\rightarrow v) = -\log\frac{\exp\left(u_i^{\top}v_i/\tau\right)}{\sum_{k=1}^{N}\exp\left(u_i^{\top}v_k/\tau\right)}",
         [(r"u_i,\ v_i", "Normalized embeddings of the i-th <b>image</b> and of its <b>text</b>, from two separate encoders."), (r"N", "The batch size: each image must pick its own caption among N."),
          (None, "The full loss averages both directions, image to text and text to image (CLIP). After training, a class can be described in words and recognized without any labelled example: zero-shot classification.")],
         "The views do not have to come from augmentation. They can be two modalities of the same object: an image and its caption, a chest radiograph and its report, a molecule and the description of its assay. This is CLIP. Two encoders, one per modality. For a batch of N pairs, each image must find its own text among the N texts, and each text its own image. It is the InfoNCE loss, with a different notion of positive pair. After training, the two modalities live in one space. You can then classify an image by comparing it with the embeddings of sentences describing each class, with no labelled image: zero-shot classification. We return to multimodal fusion in session ten.")
    S.sec("Views, evaluation and pitfalls outside natural images.")
    S.tbl("The augmentation question", "A view states an invariance. A wrong invariance deletes the signal.", ["Modality", "Common views or masks", "What to question"],
          [["Images", "Crops, colour jitter, blur", "In histology, colour carries diagnostic information"], ["Molecules", "SMILES enumeration, atom masking, conformers", "A small structural edit can change activity completely"],
           ["Proteins", "Masking residues", "One mutation can abolish function"], ["Clinical sequences", "Masking events, time windows, dropping a modality", "Time since the last dose and dose size are signal, not nuisance"]],
          "This is the slide I would like you to remember. A view is a statement: these two inputs should have the same representation. In other words, an invariance. If the invariance is wrong, the encoder is trained to delete signal. Colour jitter is harmless for photographs of dogs; in histology, stain colour is diagnostic. For molecules, a small edit can change activity by orders of magnitude: so-called activity cliffs. For clinical sequences, shifting timestamps or rescaling doses would make the encoder blind to exactly what pharmacology is about. Masking and predictive objectives are often safer than augmentation here, because they assume less.",
          widths=[20, 38, 42], small=True, band="Before choosing an augmentation, ask: would a pharmacologist call these two inputs equivalent?")
    S.tbl("Evaluating a representation", "Report several protocols; each answers a different question.", ["Protocol", "What is trained", "What it tells you"],
          [["Linear probe", "A linear layer on frozen features", "Whether the information is easy to extract"], ["k-nearest neighbours", "Nothing", "The geometry of the space, without hyperparameters"],
           ["Fine-tuning", "The whole network", "The best achievable performance"], ["Label-efficiency curve", "Head or whole network, with 1 %, 10 %, 100 % of labels", "The practical value of pre-training"],
           ["Transfer under shift", "Evaluated on another site or period", "Robustness: what clinical use requires"]],
          "How do you know the representation is good? Not by the pre-training loss, which is not comparable across methods. Use downstream protocols, and report several. A linear probe: freeze the encoder, train a linear layer. It tells you whether information is easy to extract. Nearest neighbours: no training at all. Fine-tuning gives the best achievable number but hides the quality of the representation. The label-efficiency curve, performance with one, ten and a hundred percent of the labels, shows the practical value of pre-training. And transfer under shift, to another site or period, is what clinical use requires.",
          widths=[24, 40, 36], small=True)
    S.pts("What to expect: label efficiency", "A schematic curve, not measured data.",
          ["With many labels, pre-training and training from scratch often converge.", "With few labels, the pre-trained encoder is far ahead.", "The gain is largest exactly where clinical datasets live: hundreds to thousands of labelled patients.", "Always include a strong non-deep baseline on the same splits."],
          "What should you expect? This schematic shows the typical shape; it is not measured data. On the horizontal axis, the number of labelled examples, on a logarithmic scale. With tens of thousands of labels, training from scratch catches up with the pre-trained encoder. With a few hundred, the pre-trained encoder is far ahead. The gain is largest exactly where clinical datasets live. One caution: always include a strong non-deep baseline on the same splits, boosted trees on hand-crafted summaries for instance. On small tabular problems it often remains the model to beat.",
          fig=fig_label())
    S.code("InfoNCE in eleven lines", "The SimCLR loss for a batch of N pairs.", CODE,
           ["<b>normalize</b>: dot products become cosine similarities.", "The diagonal is set to −∞: an embedding is not its own candidate.", "<b>pos</b>: for row i the positive sits N positions away.", "The loss is an ordinary <b>cross-entropy</b> over 2N − 1 candidates."],
           "The loss as code. z one and z two hold the embeddings of the two views for a batch of N examples. We concatenate and normalize them, so that dot products are cosine similarities. The similarity matrix, divided by the temperature, is two N by two N. We set the diagonal to minus infinity, because an embedding is not a candidate for itself. For row i, the positive is the other view of the same example, which sits N rows away; that is what the roll computes. Then a plain cross-entropy. Eleven lines. The difficulty of contrastive learning is not the loss; it is the choice of views.")
    S.ex("A loss by hand, and four candidate views", ["For one anchor, the cosine similarities are: positive 0.8; negatives 0.2, 0.0 and −0.4. Compute the InfoNCE loss with τ = 0.2, then with τ = 1.", "You pre-train on tacrolimus monitoring sequences: dose, trough level, creatinine, time. For each candidate view, is the implied invariance sensible?", "(a) Masking 30 % of the events. (b) Shifting all times by a random offset of up to 12 hours.", "(c) Multiplying all doses by a random factor. (d) Dropping all creatinine values."],
         dict(time="10 minutes", mat="A calculator with exp and ln", out="Two losses; four verdicts with one line of justification each"),
         "Your turn, in two parts. First, a loss by hand. For one anchor, the cosine similarities are zero point eight for the positive, and zero point two, zero and minus zero point four for three negatives. Compute the InfoNCE loss with temperature zero point two, then with temperature one. Second, a design question. You pre-train on tacrolimus monitoring sequences: dose, trough level, creatinine and time. Four candidate views are proposed: masking thirty percent of the events; shifting all times by a random offset of up to twelve hours; multiplying all doses by a random factor; dropping all creatinine values. For each, is the implied invariance sensible? Ten minutes.")
    S.sol("A loss by hand, and four candidate views", [f"<b>τ = 0.2</b>: logits 4, 1, 0, −2; exponentials {e2[0]:.1f}, {e2[1]:.2f}, 1, {e2[3]:.2f}; p = {p2:.3f}; loss = <b>{l2:.3f}</b>. <b>τ = 1</b>: p = {p1:.3f}; loss = <b>{l1:.3f}</b>.", "<b>(a) Sensible.</b> Hidden events can be inferred from the rest; this is masked modelling.", "<b>(b) Not sensible.</b> Twelve hours turns a trough into a peak: timing is the signal.", "<b>(c) Not sensible.</b> The dose–exposure relation is what the encoder should learn. <b>(d) Sensible</b>, as robustness to a missing modality."],
          f"Solutions. With temperature zero point two, the logits are four, one, zero and minus two. The exponentials are {e2[0]:.1f}, {e2[1]:.2f}, one and {e2[3]:.2f}. The positive gets probability {p2:.3f} and the loss is {l2:.3f}. With temperature one, the probability falls to {p1:.3f} and the loss rises to {l1:.3f}: the same embeddings, a very different loss. For the views. Masking events is sensible. Shifting times by up to twelve hours is not: with twice-daily dosing it turns a trough into a peak. Rescaling doses is not: the relation between dose and exposure is precisely what we want the encoder to capture. Dropping creatinine is sensible, as robustness to a missing modality.",
          band="Time and dose are signal. Any view that hides them teaches the encoder to ignore pharmacology.")
    S.quiz([("In InfoNCE, lowering the temperature:", ["Flattens the distribution over candidates", "Concentrates the gradient on hard negatives", "Removes the need for negatives"], 1, "The softmax sharpens, so the most similar negatives dominate."),
            ("A collapsed representation is:", ["Aligned but not uniform", "Uniform but not aligned", "Neither"], 0, "All inputs map to the same point: positives coincide, and so does everything else."),
            ("Masked autoencoders hide 75 % of image patches because:", ["Images are highly redundant", "It saves labels", "The decoder is large"], 0, "With little masking, neighbouring patches make the task trivial.")],
           "Three questions. Lowering the temperature concentrates the gradient on hard negatives. A collapsed representation is aligned but not uniform. And masked autoencoders hide seventy-five percent of the patches because images are highly redundant.")
    S.take(["Self-supervision turns unlabelled data into an encoder; a small head then needs few labels.", "Contrastive learning = alignment of positives + uniformity of everything; the temperature controls the balance.", "Without negatives, collapse must be prevented by asymmetry or by explicit variance terms.", "Masked and latent-prediction objectives assume less than augmentation: often safer for clinical and molecular data.", "A view is an invariance. Time and dose are signal."],
           "Five takeaways. Self-supervision turns unlabelled data into an encoder, and a small head then needs few labels. Contrastive learning is alignment of positives plus uniformity of everything, with the temperature controlling the balance. Without negatives, collapse must be prevented by asymmetry or explicit variance terms. Masked and latent-prediction objectives assume less than augmentation and are often safer for clinical and molecular data. And a view is an invariance: time and dose are signal.")
    S.refs(["T. Chen, S. Kornblith, M. Norouzi, G. Hinton, “A Simple Framework for Contrastive Learning of Visual Representations”, <i>ICML</i>, 2020.", "A. van den Oord, Y. Li, O. Vinyals, “Representation Learning with Contrastive Predictive Coding”, arXiv:1807.03748, 2018.",
            "T. Wang, P. Isola, “Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere”, <i>ICML</i>, 2020.", "J.-B. Grill et al., “Bootstrap Your Own Latent”, <i>NeurIPS</i>, 2020.",
            "A. Bardes, J. Ponce, Y. LeCun, “VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning”, <i>ICLR</i>, 2022.", "K. He et al., “Masked Autoencoders Are Scalable Vision Learners”, <i>CVPR</i>, 2022.",
            "M. Assran et al., “Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture”, <i>CVPR</i>, 2023.", "A. Radford et al., “Learning Transferable Visual Models From Natural Language Supervision”, <i>ICML</i>, 2021."],
           "References, one per method discussed: SimCLR, contrastive predictive coding for InfoNCE, the alignment and uniformity analysis, BYOL, VICReg, masked autoencoders, I-JEPA and CLIP.")
    S.end("Session 8 · Deep generative models", "That is the end of session seven. We have learned to encode data. Next session we learn to generate it: autoregressive models, variational autoencoders, diffusion and flow matching.")
    return S
