from lib import *
import numpy as np

LOG = np.array([3.0, 2.4, 2.0, 1.0, 0.2, -1.5]); TOKS = ["5 mg", "4 mg", "6 mg", "3 mg", "8 mg", "50 mg"]
PT = {T: np.exp(LOG / T) / np.exp(LOG / T).sum() for T in (0.5, 1.0, 1.5)}

def two_blobs(seed=0, n=26):
    r = np.random.default_rng(seed)
    a = r.normal([-1.1, 0.5], [0.45, 0.4], (n, 2)); b = r.normal([1.0, -0.5], [0.5, 0.45], (n, 2))
    return a, b

def fig_dg():
    f = Fig(800, 520, "Left: a discriminative model draws a boundary between two classes. Right: a generative model describes where the data lie")
    a, b = two_blobs()
    for k, x0 in enumerate([10, 410]):
        f.rect(x0, 70, 380, 360, "#F2F4F8", None, rx=8)
        X = lambda v: x0 + 190 + v * 78; Y = lambda v: 250 - v * 78
        if k == 1:
            for (cx, cy), col in [((-1.1, 0.5), BLUE), ((1.0, -0.5), RED)]:
                for s in (1.0, 1.9):
                    f.sv.append(f'<ellipse cx="{X(cx):.0f}" cy="{Y(cy):.0f}" rx="{48 * s:.0f}" ry="{42 * s:.0f}" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-width="2"/>')
        for p in a: f.circle(X(p[0]), Y(p[1]), 8, BLUE, WHITE, 2)
        for p in b: f.circle(X(p[0]), Y(p[1]), 8, RED, WHITE, 2)
        if k == 0: f.line(X(-0.75), Y(-1.9), X(0.75), Y(2.0), INK, 5)
    f.lab(10, 14, "Discriminative: p(y | x)", 380, "center", "axw ax-b"); f.lab(410, 14, "Generative: p(x)", 380, "center", "axw ax-b")
    f.lab(10, 446, "where is the boundary?", 380, "center", "axh", INK); f.lab(410, 446, "where do the data live?", 380, "center", "axh")
    return f

def fig_sampling():
    f = Fig(800, 620, "Next-token probabilities for six candidate doses at three sampling temperatures")
    f.axes(130, 70, 760, 480, (0, 6), (0, 0.8), [], [0.0, 0.2, 0.4, 0.6, 0.8], "", "Probability of the next token", fmt=lambda v: f"{v:.1f}")
    for ti, (T, col) in enumerate([(0.5, BLUE), (1.0, AMBER), (1.5, GREY)]):
        for k in range(6):
            x = f.X(k + 0.14 + ti * 0.25); w = (f.X(1) - f.X(0)) * 0.22; p = PT[T][k]
            f.rect(x, f.Y(p), w, max(2, f.Y(0) - f.Y(p)), col, None)
    for k in range(6): f.lab(f.X(k), 492, TOKS[k], f.X(1) - f.X(0), "center", "ax ax-b", RED if k == 5 else None)
    for ti, (t, col) in enumerate([("T = 0.5", BLUE), ("T = 1", AMBER), ("T = 1.5", GREY)]):
        f.rect(480, 96 + ti * 46, 30, 30, col, None); f.lab(522, 96 + ti * 46, t, 200, "left", "ax ax-b")
    f.lab(130, 540, "candidate continuation of “reduce tacrolimus to …”", 630, "center", "ax")
    return f

def fig_vae():
    f = flow(["<b>x</b><br>molecule,<br>record", "<b>Encoder</b><br>q(z | x)", "<b>μ, σ</b>", "<b>z = μ + σ ⊙ ε</b><br>sampled code", "<b>Decoder</b><br>p(x | z)", "<b>x̂</b><br>reconstruction"], 1500, 230, "Variational autoencoder: encoder, mean and standard deviation, sampled latent code, decoder, reconstruction", gap=36,
             colors=[(WHITE, INK), (PALE, BLUE), (WHITE, BLUE), (PINK, RED), (PALE, BLUE), (WHITE, INK)])
    return f

def fig_diff():
    f = Fig(1500, 470, "Forward diffusion turns structured data into Gaussian noise in steps; the learned reverse process goes back")
    r = np.random.default_rng(3); th = r.uniform(0, 2 * np.pi, 70)
    x0 = np.c_[np.cos(th), np.sin(th)] * 1.0 + r.normal(0, 0.06, (70, 2)); eps = r.normal(0, 1, (70, 2))
    for k, (ab, lab) in enumerate([(1.0, "t = 0 · data"), (0.92, "an early step"), (0.55, "a late step"), (0.0, "t = T · pure noise")]):
        cx = 170 + k * 385; xt = np.sqrt(ab) * x0 + np.sqrt(1 - ab) * eps
        f.rect(cx - 150, 70, 300, 290, "#F2F4F8", None, rx=8)
        for p in xt:
            px, py = cx + np.clip(p[0], -2.2, 2.2) * 62, 215 - np.clip(p[1], -2.2, 2.2) * 62
            f.circle(px, py, 6, BLUE if k < 3 else GREY, None)
        f.lab(cx - 150, 370, lab, 300, "center", "ax ax-b")
        if k < 3:
            f.arrow(cx + 160, 185, cx + 225, 185, INK, 4, 14); f.arrow(cx + 225, 245, cx + 160, 245, RED, 4, 14)
    f.lab(20, 14, "forward: add a little Gaussian noise at each step (fixed, nothing to learn)", 1300, "left", "axh", INK)
    f.lab(0, 416, "reverse: remove the noise step by step (learned)", 1490, "right", "axh", RED)
    return f

def fig_fm():
    f = Fig(800, 560, "Flow matching: straight paths from noise samples to data samples")
    r = np.random.default_rng(8); n = 16
    x0 = r.normal(0, 1, (n, 2)) * [60, 105] + [150, 280]; th = np.linspace(0, 2 * np.pi, n, endpoint=False) + 0.2
    x1 = np.c_[620 + 95 * np.cos(th), 270 + 95 * np.sin(th)]
    order = np.argsort(x0[:, 1]); o1 = np.argsort(x1[:, 1])
    for i, j in zip(order, o1):
        f.line(x0[i, 0], x0[i, 1], x1[j, 0], x1[j, 1], "#AEB9E6", 3)
        mx, my = x0[i] + 0.5 * (x1[j] - x0[i]); f.circle(mx, my, 6, AMBER, None)
    for p in x0: f.circle(p[0], p[1], 9, GREY, WHITE, 2)
    for p in x1: f.circle(p[0], p[1], 9, BLUE, WHITE, 2)
    f.lab(0, 10, "noise x₀", 300, "center", "axh", GREY); f.lab(480, 10, "data x₁", 300, "center", "axh")
    f.lab(200, 506, "orange: the interpolated point xₜ at t = 0.5", 590, "left", "ax ax-b", AMBER)
    return f

CODE = '''def ddpm_loss(model, x0, alpha_bar):
    # x0: (B, d) clean data
    # alpha_bar: (T,) cumulative noise schedule
    B = x0.shape[0]
    t = torch.randint(0, len(alpha_bar), (B,))
    ab = alpha_bar[t].unsqueeze(1)       # (B, 1)
    eps = torch.randn_like(x0)           # the noise
    xt = ab.sqrt() * x0 + (1 - ab).sqrt() * eps
    return F.mse_loss(model(xt, t), eps) # predict it'''

def build():
    S = Session(8, "en", "Part II · Advanced track", "Deep generative models", "Autoregressive models, variational autoencoders, diffusion and flow matching, with their uses in drug discovery and patient modelling.")
    S.sec("Opening: two requests for new samples.")
    S.cover("Session eight: generative models. So far our models mapped an input to a prediction. Today the model produces new data: a sentence, a molecule, a protein backbone, a patient trajectory. I will cover five families, with their objective functions written out. Two of them carry most of current practice: autoregressive models for anything discrete and sequential, and diffusion or flow models for anything continuous.")
    S.sit("Two requests", "A medicinal chemist asks for 1,000 new molecules that resemble known calcineurin inhibitors but are predicted to be less nephrotoxic.<br><br>A pharmacometrician asks for 10,000 plausible virtual patients on which to test a dosing rule before a trial.",
          "What does it mean to learn a distribution well enough to draw new, plausible samples from it?",
          "Two requests you might receive. A medicinal chemist wants a thousand new molecules that resemble known calcineurin inhibitors, with lower predicted nephrotoxicity. A pharmacometrician wants ten thousand plausible virtual patients to test a dosing rule before a trial. In both cases nobody wants a prediction for an existing object. They want new objects that could have come from the same distribution as the real ones, possibly steered toward a property. That is generative modelling: learn the distribution, then sample from it. The hard part, as we will see, is knowing whether the samples are any good.")
    S.obj(["State what a generative model learns, and place the five main families on one map.", "Derive the ELBO and the diffusion training loss, and explain every term.", "Explain sampling: temperature, guidance, and the number of steps.", "Choose evaluation criteria for generated molecules and synthetic patients."],
          "Four objectives. State what a generative model learns, and place the five main families on one map. Derive two objectives, the evidence lower bound for variational autoencoders and the noise-prediction loss for diffusion, and explain every term. Explain how sampling works and what controls it. And choose evaluation criteria for generated molecules and synthetic patients, which is where most projects go wrong.")
    S.plan([("What generative models learn", "p(x), and a map of five families"), ("Autoregressive models", "Factorization, sampling temperature, hallucination"), ("Latent-variable models", "The VAE and its bound; GANs in one slide"), ("Diffusion and flow matching", "Forward noising, the denoising loss, guidance, straight paths"), ("Applications and evaluation", "Molecules, proteins, trajectories; what to measure")],
           "Five parts. What generative models learn, with a map of the families. Autoregressive models. Latent-variable models: the variational autoencoder, and adversarial networks in one slide. Diffusion and flow matching, the longest part. Then applications in the pharmaceutical sciences, and evaluation.")
    S.sec("What a generative model learns, and a map of the five families.")
    S.pts("Discriminative or generative", "The same data, two different questions.",
          ["A <b>discriminative</b> model learns p(y | x): given an input, which label?", "A <b>generative</b> model learns p(x): which inputs are plausible at all?", "A <b>conditional</b> generative model learns p(x | c): plausible inputs given a condition c, such as a target or a phenotype.", "Sampling from p(x | c) is how one “designs”."],
          "The same data, two questions. A discriminative model learns the probability of a label given an input. It needs to know only where the boundary is. A generative model learns the distribution of the inputs themselves: which molecules, which records are plausible. That is a much harder problem, because the model must describe the whole space, not only a boundary. In practice we want a conditional generative model: the distribution of x given a condition c. Molecules given a target pocket. Trajectories given a patient's history. Sampling from a conditional model is what people mean by design.",
          fig=fig_dg())
    S.tbl("Five families on one map", "They differ in how the distribution is represented and how one samples.", ["Family", "Idea", "Likelihood", "Sampling", "Typical use"],
          [["Autoregressive", "Predict each element from the previous ones", "Exact", "One element at a time", "Text, SMILES, event sequences"], ["VAE", "Encode to a latent code, decode back", "Lower bound", "One pass", "Smooth latent spaces"],
           ["GAN", "A generator tries to fool a discriminator", "None", "One pass", "Images, historically"], ["Normalizing flow", "An invertible map from noise to data", "Exact", "One pass", "Densities, small dimensions"],
           ["Diffusion, flow matching", "Learn to reverse a gradual noising", "Bound, or via an ODE", "Many steps", "Images, 3D structures, molecules"]],
          "Five families. Autoregressive models predict each element from the previous ones; the likelihood is exact and sampling is sequential. Variational autoencoders compress to a latent code and decode; they optimize a lower bound. Adversarial networks train a generator against a discriminator; there is no likelihood at all. Normalizing flows are invertible maps from noise to data with an exact likelihood, at the price of restricted architectures. Diffusion and flow-matching models learn to reverse a gradual noising process; sampling takes many steps, and quality is currently the best for continuous data. For discrete sequences, think autoregressive. For continuous objects, think diffusion.",
          widths=[19, 27, 14, 17, 23], small=True)
    S.sec("Autoregressive models: factorization, sampling, and why language models hallucinate.")
    S.eq("Autoregressive models", "The chain rule of probability, with one network for all the factors.", r"p_\theta(x) = \prod_{t=1}^{T} p_\theta\left(x_t\,|\,x_{<t}\right)",
         [(r"x = (x_1,\dots,x_T)", "A sequence of T tokens: words, SMILES symbols, clinical events."), (r"x_{<t}", "Everything before position t."), (r"p_\theta(x_t\,|\,x_{<t})", "A categorical distribution over the vocabulary, produced by a causal transformer."),
          (None, "Taking minus the logarithm gives the causal language-modelling loss of session 6: training is maximum likelihood.")],
         "Any joint distribution over a sequence factorizes exactly into a product of conditionals: the first element, the second given the first, and so on. This is just the chain rule of probability. An autoregressive model represents every conditional with one network, a causal transformer, that outputs a distribution over the vocabulary. Take minus the logarithm and you recover the next-token loss from session six: training is maximum likelihood, with an exact likelihood. Large language models are this. So are SMILES generators for molecules, and Delphi-2M for disease histories. To generate, sample the first token, feed it back, sample the next.",
         band="Large language models, SMILES generators and event-sequence models are all this one formula.")
    S.eq("Sampling, and what a hallucination is", "Illustrative logits for the continuation of one sentence.", r"p_T(x_t = k) = \frac{\exp\left(\ell_k/T\right)}{\sum_{j}\exp\left(\ell_j/T\right)}",
         [(r"\ell_k", "The <b>logit</b> of candidate token k: the raw score from the network."), (r"T", "The sampling <b>temperature</b>. T below 1 concentrates on the top candidates; T above 1 flattens the distribution."),
          (None, f"Here the implausible “50 mg” has probability {PT[0.5][5] * 100:.2f} % at T = 0.5, {PT[1.0][5] * 100:.1f} % at T = 1 and {PT[1.5][5] * 100:.1f} % at T = 1.5.")],
         f"At generation time, the model gives a score, a logit, to every candidate token. We divide the logits by a temperature T and apply a softmax. The bars show an illustrative case: the continuation of the sentence reduce tacrolimus to. At low temperature almost all the mass is on the top candidates. At temperature one point five the implausible fifty milligrams receives about {PT[1.5][5] * 100:.0f} percent: one answer in fifty. This is the right way to think about hallucination. The model returns a plausible continuation under its learned distribution. Nothing in the objective checks the continuation against a source. Lower temperature reduces the rate; it does not make the model verify anything.",
         fig=fig_sampling(), band="A hallucination is not a malfunction: it is a sample.")
    S.sec("Latent-variable models: the variational autoencoder and its bound; adversarial networks.")
    S.eq("The variational autoencoder: the evidence lower bound", "The likelihood is intractable; we maximize a bound on it.", r"\log p_\theta(x) \geq \mathbb{E}_{q_\phi(z|x)}\left[\log p_\theta(x\,|\,z)\right] - D_{\mathrm{KL}}\left(q_\phi(z\,|\,x)\,\Vert\,p(z)\right)",
         [(r"z", "A <b>latent code</b>: a short vector meant to summarize x."), (r"p(z)", "The <b>prior</b> on codes, a standard Gaussian."), (r"q_\phi(z\,|\,x)", "The <b>encoder</b>: an approximate posterior, a Gaussian whose mean and variance are network outputs."),
          (r"\mathbb{E}\left[\log p_\theta(x\,|\,z)\right]", "<b>Reconstruction</b>: codes drawn from the encoder must decode back to x."), (r"D_{\mathrm{KL}}", "<b>Regularization</b>: the encoder's distribution must stay close to the prior, so that sampling from the prior gives usable codes.")],
         "The variational autoencoder assumes each data point is generated from a latent code z: draw z from a prior, then draw x from a decoder. The likelihood of x requires integrating over all codes, which is intractable. So we introduce an encoder, q, that proposes codes for a given x, and we maximize a lower bound on the log-likelihood: the evidence lower bound, or ELBO. It has two terms. Reconstruction: codes proposed by the encoder must decode back to x. And a Kullback-Leibler term that keeps the encoder's distribution close to the prior. Without it, the model is an ordinary autoencoder, and codes drawn from the prior decode to nonsense. The two terms pull in opposite directions.")
    S.eq("The reparameterization trick", "How to back-propagate through a random draw.", r"z = \mu_\phi(x) + \sigma_\phi(x)\odot\epsilon,\qquad \epsilon\sim\mathcal{N}(0,I)",
         [(r"\mu_\phi,\ \sigma_\phi", "Mean and standard deviation of the code, produced by the encoder."), (r"\epsilon", "Noise drawn independently of the parameters; ⊙ is the element-wise product."), (None, "The randomness is moved into ε, so z becomes a differentiable function of the encoder's outputs.")],
         "One technical point makes the whole thing trainable. The bound contains an expectation over codes sampled from the encoder, and you cannot differentiate through a sampling operation. The trick: write the sample as the mean plus the standard deviation times a noise variable epsilon drawn from a standard Gaussian. The randomness now sits in epsilon, which does not depend on the parameters, and z is a differentiable function of the encoder outputs. Why do chemists like these models? The latent space is smooth and continuous. One can take a molecule's code, move in the direction that improves a predicted property, and decode: optimization in a continuous space instead of a search over discrete structures.",
         fig=fig_vae(), figtop=True, band="A smooth latent space turns molecular design into continuous optimization.")
    S.eq("Adversarial networks, in one slide", "A two-player game instead of a likelihood.", r"\min_G\max_D\ \ \mathbb{E}_{x\sim p_{\mathrm{data}}}\left[\log D(x)\right] + \mathbb{E}_{z\sim p(z)}\left[\log\left(1-D(G(z))\right)\right]",
         [(r"G", "The <b>generator</b>: turns noise z into a sample."), (r"D", "The <b>discriminator</b>: outputs the probability that its input is real."),
          (None, "Strengths: sharp samples in one pass. Weaknesses: unstable training, and mode collapse, where the generator produces only a few kinds of sample. For images, diffusion models have largely replaced them.")],
         "Generative adversarial networks, briefly, because you will meet them in the literature. Two networks play a game. The generator turns noise into samples. The discriminator tries to tell real samples from generated ones. The generator is trained to fool the discriminator. There is no likelihood anywhere. The samples are sharp and generation takes a single pass. But training is unstable, and the generator may cover only part of the distribution, a failure called mode collapse, which is serious if you are generating virtual patients and the rare phenotypes are the ones that matter. For images, diffusion models have largely taken over since 2021.")
    S.sec("Diffusion and flow matching: forward noising, the denoising loss, guidance, straight paths.")
    S.wide("Diffusion: destroy, then learn to rebuild", "A fixed forward process and a learned reverse process.", fig_diff(),
           "The idea of diffusion fits in one picture. Start from data, on the left: here, points on a ring. Add a little Gaussian noise. Add a little more. After enough steps nothing of the structure remains: pure Gaussian noise, on the right. This forward process is fixed; it has no parameters. Now train a network to undo one step: given a noisy sample and the noise level, estimate the noise that was added. To generate, draw pure noise and apply the learned denoising step repeatedly, from right to left. A hard problem, generating structure from nothing, has been cut into many easy ones: removing a little noise.",
           band="One hard generation problem becomes many easy denoising problems.")
    S.eq("The forward process in closed form", "We can jump to any noise level in one step.", [r"q(x_t\,|\,x_0) = \mathcal{N}\left(x_t;\ \sqrt{\bar{\alpha}_t}\,x_0,\ (1-\bar{\alpha}_t)\,I\right)", r"x_t = \sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\ \epsilon,\qquad \epsilon\sim\mathcal{N}(0,I)"],
         [(r"x_0,\ x_t", "A clean data point, and its noised version at step t."), (r"\beta_t,\ \alpha_t = 1-\beta_t", "The variance of the noise added at step t, set by a fixed <b>schedule</b>, and its complement."),
          (r"\bar{\alpha}_t = \prod_{s=1}^{t}\alpha_s", "The fraction of signal that survives after t steps: it goes from 1 to 0."), (None, "The signal-to-noise ratio at step t is ᾱ / (1 − ᾱ).")],
         "Because sums of Gaussians are Gaussian, we do not need to simulate the steps one by one. The distribution of x t given the clean x zero is a Gaussian: its mean is x zero scaled by the square root of alpha bar t, its variance is one minus alpha bar t. Equivalently, second line: x t is a weighted mix of the clean data and a fresh Gaussian noise epsilon. Alpha bar t is the product of all the alphas up to step t. It starts near one, almost pure signal, and decreases to zero, pure noise. How fast it decreases is the noise schedule. This closed form is what makes training cheap: pick a random step t, and build x t directly.")
    S.eq("Training and sampling", "A regression loss; then an iterative sampler.", [r"\mathcal{L} = \mathbb{E}_{x_0,\,\epsilon,\,t}\left\Vert \epsilon - \epsilon_\theta(x_t,\,t)\right\Vert^2", r"x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\,\epsilon_\theta(x_t,\,t)\right) + \sigma_t\,z"],
         [(r"\epsilon_\theta(x_t,\,t)", "The network: given a noisy sample and the step, it predicts the noise that was added."), (r"\mathbb{E}_{x_0,\,\epsilon,\,t}", "Average over data points, noise draws and steps chosen at random."),
          (r"\sigma_t\,z", "Fresh Gaussian noise re-injected at each sampling step, except the last.")],
         "Training, first line. Take a data point, pick a step t at random, draw a noise epsilon, build x t with the closed form, and ask the network to predict epsilon. The loss is a mean squared error. That is all: a regression problem, stable to train, with no adversary and no posterior collapse. It can be derived as a weighted variational bound, but the simple form works best. Sampling, second line. Start from pure noise at step T. At each step, subtract the predicted noise, suitably scaled, and add a little fresh noise. Repeat down to step zero. The price is the number of network evaluations: hundreds originally, tens with modern samplers.",
         band="Training is plain regression. The cost is paid at sampling time.")
    S.eq("The score, and guidance", "Why predicting noise works, and how to steer generation.", [r"\epsilon_\theta(x_t,\,t) \approx -\sqrt{1-\bar{\alpha}_t}\ \nabla_{x_t}\log p_t(x_t)", r"\tilde{\epsilon} = (1+w)\,\epsilon_\theta(x_t,\,c) - w\,\epsilon_\theta(x_t,\,\varnothing)"],
         [(r"\nabla_{x_t}\log p_t(x_t)", "The <b>score</b>: the direction in which the density of noisy data increases fastest."), (r"c,\ \varnothing", "A condition (a text, a target, a phenotype), and the empty condition."), (r"w", "The <b>guidance weight</b>: larger values follow the condition more closely, at the cost of diversity.")],
         "Two more ideas. First line: the predicted noise is, up to a factor, the gradient of the log-density of the noisy data, called the score. So the network has learned which direction makes a sample more likely, and sampling is a guided walk uphill, with noise. This is the link with score-based models and stochastic differential equations. Second line: classifier-free guidance. Train one network both with a condition c and, some of the time, without it. At sampling time, extrapolate from the unconditional prediction toward the conditional one, with weight w. Large w follows the condition closely and loses diversity. This is how text-to-image models, and pocket-conditioned molecule generators, are steered.")
    S.eq("Flow matching", "Learn a velocity field that carries noise to data along straight paths.", [r"x_t = (1-t)\,x_0 + t\,x_1", r"\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t,\,x_0,\,x_1}\left\Vert v_\theta(x_t,\,t) - (x_1 - x_0)\right\Vert^2"],
         [(r"x_0,\ x_1", "A noise sample and a data sample."), (r"t", "A time between 0 and 1, drawn uniformly."), (r"v_\theta", "The network: a <b>velocity field</b>. The target velocity along a straight path is simply x₁ − x₀."),
          (None, "To sample: draw x₀ and integrate dx/dt = v(x, t) from t = 0 to 1.")],
         "Flow matching is the formulation most recent models use. Pair a noise sample x zero with a data sample x one, and draw a straight line between them. At time t, the point on the line is x t. Its velocity along the line is constant: x one minus x zero. Train a network to predict that velocity from x t and t. Again a regression. To generate, draw noise and integrate the ordinary differential equation defined by the learned velocity field, from time zero to time one. Because the target paths are straight, a few integration steps suffice. Diffusion and flow matching are close relatives: different choices of path between noise and data.",
         fig=fig_fm(), band="Straight paths: fewer sampling steps.")
    S.sec("Applications in the pharmaceutical sciences, evaluation, and a training step.")
    S.tbl("Generative models in the pharmaceutical sciences", "Which family, for which object.", ["Object", "Usual families", "Example"],
          [["Small molecules", "SMILES language models, VAEs, graph and 3D diffusion", "Continuous latent space for chemical design (Gómez-Bombarelli et al., 2018)"],
           ["Protein structures", "Diffusion over 3D coordinates", "AlphaFold 3 (Abramson et al., 2024); RFdiffusion (Watson et al., 2023)"],
           ["Health trajectories", "Autoregressive transformers over events", "Delphi-2M samples synthetic future trajectories (Shmatko et al., 2025)"],
           ["Medical images", "Latent diffusion", "Augmentation and counterfactuals; needs reader validation"],
           ["Virtual populations", "Mechanistic simulation with learned covariates", "See session 10"]],
          "Where are these models used in our field? For small molecules: language models over SMILES strings, variational autoencoders with a continuous latent space, and diffusion over molecular graphs or three-dimensional coordinates. For proteins: AlphaFold 3 uses a diffusion module to produce atomic coordinates, and RFdiffusion designs new protein backbones. For health trajectories: Delphi-2M, an autoregressive transformer, can sample synthetic futures for an individual. For medical images, latent diffusion. And for virtual populations, the mature technology remains mechanistic simulation; the interesting research is in combining it with learned components, which is session ten.",
          widths=[20, 36, 44], small=True)
    S.tbl("Evaluating a generative model", "No single number. Each object needs its own criteria.", ["Generated object", "What to measure", "The trap"],
          [["Text", "Perplexity; factual checks against sources", "Fluent is not correct"], ["Images", "Fréchet inception distance; expert reader study", "A good distance says nothing about clinical plausibility"],
           ["Molecules", "Validity, uniqueness, novelty, diversity; drug-likeness, synthetic accessibility; then assays", "Valid is not synthesizable, and synthesizable is not active"],
           ["Synthetic patients", "Fidelity; utility (train on synthetic, test on real); privacy (membership inference)", "High fidelity may mean memorized patients"]],
          "Evaluation is the weak point of the field. There is no single number. For text, perplexity measures fit, not truth. For images, the Fréchet inception distance compares feature statistics; it says nothing about clinical plausibility. For molecules, the standard quartet is validity, uniqueness, novelty and diversity, then drug-likeness and synthetic accessibility. But a valid molecule may be impossible to make, and a makeable one may be inactive: only an assay decides. For synthetic patients, three axes: fidelity to real distributions, utility, meaning a model trained on synthetic data works on real data, and privacy. Note the tension: perfect fidelity can simply mean the model memorized real patients.",
          widths=[20, 46, 34], small=True, band="The final judge is an experiment, or real held-out data.")
    S.code("A diffusion training step", "The whole objective in nine lines.", CODE,
           ["Draw a random step <b>t</b> for each example.", "Build <b>xt</b> with the closed-form forward process.", "The network sees <b>xt</b> and <b>t</b>, and must return the noise.", "Mean squared error. Nothing else is needed to train."],
           "The training step as code. For each example in the batch, draw a random step t. Look up alpha bar for that step. Draw the noise. Build x t with the closed form. Call the model on x t and t, and compare its output with the noise, using a mean squared error. Nine lines. The model itself is whatever suits the data: a U-Net for images, a transformer for sequences, an equivariant network for three-dimensional molecules. Everything difficult in diffusion is in the architecture, the noise schedule and the sampler, not in the loss.")
    S.ex("One noising step, and four design choices", ["A feature has clean value x₀ = 10. At step t, ᾱ = 0.64, and the noise drawn is ε = −0.5. Compute xₜ and the signal-to-noise ratio.", "The network predicts ε̂ = −0.3. What clean value does that imply?", "Which family would you try first for: (a) drug information leaflets; (b) 3D ligand poses in a binding pocket;", "(c) future event sequences for a patient; (d) a smooth space in which to optimize a molecular property?"],
         dict(time="8 minutes", mat="A calculator", out="Three numbers and four choices"),
         "Your turn. A feature has clean value ten. At step t, alpha bar is zero point six four, and the noise drawn is minus zero point five. Compute x t, and the signal-to-noise ratio. Then: the network predicts a noise of minus zero point three. What clean value does that prediction imply? Finally, four design choices. Which family would you try first for drug information leaflets, for three-dimensional ligand poses in a binding pocket, for future event sequences of a patient, and for a smooth space in which to optimize a molecular property? Eight minutes.")
    S.sol("One noising step, and four design choices", ["xₜ = √0.64 × 10 + √0.36 × (−0.5) = 8 − 0.3 = <b>7.7</b>. Signal-to-noise ratio: 0.64 / 0.36 = <b>1.78</b>.", "Implied clean value: (xₜ − √0.36 × ε̂) / √0.64 = (7.7 + 0.18) / 0.8 = <b>9.85</b>.", "<b>(a)</b> Autoregressive language model. <b>(b)</b> Diffusion or flow matching on 3D coordinates.", "<b>(c)</b> Autoregressive transformer over events. <b>(d)</b> Variational autoencoder."],
          "Solutions. The square root of zero point six four is zero point eight; of zero point three six, zero point six. So x t is eight minus zero point three: seven point seven. The signal-to-noise ratio is zero point six four over zero point three six, about one point eight. If the network predicts minus zero point three, invert the forward formula: seven point seven plus zero point one eight, divided by zero point eight, gives nine point eight five. A small error on the noise gives a small error on the clean value at this noise level; at high noise the same error would be amplified. For the families: leaflets are text, so autoregressive. Ligand poses are continuous coordinates, so diffusion or flow matching. Event sequences: autoregressive. A smooth space for optimization: a variational autoencoder.")
    S.quiz([("In the ELBO, the KL term:", ["Measures reconstruction quality", "Keeps the encoder's codes close to the prior", "Is the adversarial loss"], 1, "Without it, codes drawn from the prior would not decode to valid samples."),
            ("A diffusion model is trained to:", ["Fool a discriminator", "Predict the noise added to a data point", "Maximize an exact likelihood"], 1, "A regression on the noise, at a randomly chosen noise level."),
            ("Raising the sampling temperature of a language model:", ["Makes it check its sources", "Makes unlikely continuations more frequent", "Changes its weights"], 1, "The distribution flattens; nothing is verified.")],
           "Three questions. In the ELBO, the Kullback-Leibler term keeps the encoder's codes close to the prior. A diffusion model is trained to predict the noise added to a data point. And raising the sampling temperature makes unlikely continuations more frequent; it changes nothing about verification.")
    S.take(["A generative model learns a distribution; design means sampling from a conditional one.", "Discrete sequences: autoregressive models, trained by exact maximum likelihood.", "VAEs maximize a bound: reconstruction against closeness to the prior.", "Diffusion and flow matching turn generation into regression, at the price of iterative sampling.", "Evaluation is object-specific; the final judge is an experiment or real held-out data."],
           "Five takeaways. A generative model learns a distribution, and design means sampling from a conditional one. For discrete sequences, autoregressive models, trained by exact maximum likelihood. Variational autoencoders maximize a bound that trades reconstruction against closeness to the prior. Diffusion and flow matching turn generation into regression, at the price of iterative sampling. And evaluation is specific to the object generated; the final judge is an experiment or real held-out data.")
    S.refs(["D. P. Kingma, M. Welling, “Auto-Encoding Variational Bayes”, <i>ICLR</i>, 2014.", "I. Goodfellow et al., “Generative Adversarial Nets”, <i>NeurIPS</i>, 2014.", "J. Ho, A. Jain, P. Abbeel, “Denoising Diffusion Probabilistic Models”, <i>NeurIPS</i>, 2020.",
            "Y. Song et al., “Score-Based Generative Modeling through Stochastic Differential Equations”, <i>ICLR</i>, 2021.", "J. Ho, T. Salimans, “Classifier-Free Diffusion Guidance”, arXiv:2207.12598, 2022.", "Y. Lipman et al., “Flow Matching for Generative Modeling”, <i>ICLR</i>, 2023.",
            "R. Gómez-Bombarelli et al., “Automatic Chemical Design Using a Data-Driven Continuous Representation of Molecules”, <i>ACS Cent Sci</i>, 2018; 4(2): 268–276.", "J. Abramson et al., “Accurate structure prediction of biomolecular interactions with AlphaFold 3”, <i>Nature</i>, 2024; 630: 493–500.",
            "J. L. Watson et al., “De novo design of protein structure and function with RFdiffusion”, <i>Nature</i>, 2023; 620: 1089–1100."],
           "References: the founding papers for variational autoencoders, adversarial networks, diffusion, score-based models, guidance and flow matching; then three applications: chemical design in a continuous latent space, AlphaFold 3, and RFdiffusion.")
    S.end("Session 9 · Foundation models and adaptation", "That is the end of session eight. We can now encode and generate. Next session: what happens when these objectives are applied at very large scale, and how to adapt the resulting foundation models to a small clinical dataset.")
    return S
