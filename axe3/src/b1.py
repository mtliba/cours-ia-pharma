from lib import *
import numpy as np

def fig_graph():
    f = Fig(1500, 250, "Computation graph of a two-layer network: forward pass left to right, backward pass right to left")
    names = ["<b>x</b>", "<b>z</b> = W₁ x", "<b>h</b> = ReLU(z)", "<b>ŷ</b> = W₂ h", "<b>L</b>(ŷ, y)"]
    xs = [0, 250, 560, 880, 1200]; ws = [150, 220, 230, 230, 200]
    for i, (x, w, t) in enumerate(zip(xs, ws, names)):
        f.box(x, 70, w, 100, t, PALE if 0 < i < 4 else WHITE, BLUE if 0 < i < 4 else INK, "axw")
        if i < 4:
            f.arrow(x + w + 6, 100, xs[i + 1] - 6, 100, INK, 4, 14)
            f.arrow(xs[i + 1] - 6, 142, x + w + 6, 142, RED, 4, 14)
    f.lab(0, 4, "forward pass: compute and store each value", 800, "left", "axh", INK)
    f.lab(0, 196, "backward pass: multiply local derivatives, from the loss back to the input", 1400, "left", "axh", RED)
    return f

def gd(eta, steps=60, lam=(1.0, 20.0), x0=(-9.0, 1.6), mu=0.0):
    x = np.array(x0); v = np.zeros(2); lam = np.array(lam); path = [x.copy()]; loss = [0.5 * float(lam @ x ** 2)]
    for _ in range(steps):
        g = lam * x; v = mu * v + g; x = x - eta * v
        path.append(x.copy()); loss.append(0.5 * float(lam @ x ** 2))
    return np.array(path), np.array(loss)

def fig_lr():
    f = Fig(800, 600, "Loss against training step for three learning rates: too small, well chosen, too large")
    f.axes(130, 70, 760, 500, (0, 60), (-4, 6), [0, 20, 40, 60], [-4, -2, 0, 2, 4, 6], "Training step", "Loss (log scale)", fmty=lambda v: {-4: "10⁻⁴", -2: "10⁻²", 0: "1", 2: "10²", 4: "10⁴", 6: "10⁶"}.get(v, str(v)))
    for eta, c, dash in [(0.004, GREY, "10 9"), (0.09, BLUE, None), (0.104, RED, None)]:
        _, l = gd(eta); y = np.clip(np.log10(np.maximum(l, 1e-12)), -4, 6)
        pts = [(i, v) for i, v in enumerate(y) if -4 < v < 6 or i == 0]
        f.curve([a for a, b in pts], [b for a, b in pts], c, 5, dash)
    f.lab(f.X(36), f.Y(1.5) + 10, "too small: slow", 250, cls="axh", color=GREY)
    f.lab(f.X(6), f.Y(-1.6), "well chosen", 220, cls="axh")
    f.lab(f.X(8), f.Y(5.6), "too large: diverges", 330, cls="axh", color=RED)
    return f

def fig_contour():
    f = Fig(800, 600, "Gradient descent on an elongated quadratic bowl: zigzag without momentum, smooth path with momentum")
    f.ax = (60, 60, 760, 540, (-10, 2), (-2.4, 2.4))
    f.rect(60, 60, 700, 480, "#F2F4F8", None)
    for lev in [2, 8, 20, 36, 52]:
        rx = (f.X(np.sqrt(2 * lev / 1.0)) - f.X(0)); ry = (f.Y(0) - f.Y(np.sqrt(2 * lev / 20.0)))
        f.sv.append(f'<ellipse cx="{f.X(0):.1f}" cy="{f.Y(0):.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#AEB5C6" stroke-width="2"/>')
    p1, _ = gd(0.094, 26); p2, _ = gd(0.012, 60, mu=0.86)
    f.curve(p1[:, 0], p1[:, 1], RED, 4); f.curve(p2[:, 0], p2[:, 1], BLUE, 5)
    f.circle(f.X(0), f.Y(0), 10, INK); f.circle(f.X(-9), f.Y(1.6), 10, WHITE, INK, 4)
    f.rect(0, 0, 60, 600, WHITE, None); f.rect(760, 0, 40, 600, WHITE, None); f.rect(0, 0, 800, 60, WHITE, None); f.rect(0, 540, 800, 60, WHITE, None)
    f.lab(70, 8, "plain gradient descent: zigzag", 500, cls="axh", color=RED)
    f.lab(70, 548, "with momentum: smooth and faster", 700, cls="axh")
    f.lab(f.X(0) - 40, f.Y(0) + 16, "minimum", 140, "center", "ax ax-b")
    return f

def fig_sched():
    f = Fig(800, 500, "Learning-rate schedule: linear warm-up followed by cosine decay")
    T, Tw = 100, 8; t = np.arange(0, T + 1)
    lr = np.where(t < Tw, t / Tw, 0.5 * (1 + np.cos(np.pi * (t - Tw) / (T - Tw))))
    f.axes(130, 70, 760, 400, (0, 100), (0, 1.1), [0, 25, 50, 75, 100], [0, 0.5, 1.0], "Training progress (%)", "Learning rate (fraction of the peak)", fmt=lambda v: str(v))
    f.rect(f.X(0), 70, f.X(Tw) - f.X(0), 330, PINK, None, op=0.8)
    f.curve(t, lr, BLUE, 6)
    f.lab(f.X(Tw) + 14, f.Y(0.3), "warm-up", 180, cls="axh", color=RED)
    f.lab(f.X(46), f.Y(0.78), "cosine decay", 240, cls="axh")
    return f

def fig_dd():
    f = Fig(800, 600, "Schematic double-descent curve: test risk falls, peaks at the interpolation threshold, then falls again")
    f.axes(130, 70, 760, 500, (0, 10), (0, 1), [], [], "Model capacity", "Risk", grid=False)
    c = np.linspace(0.2, 9.8, 200)
    train = np.where(c < 4, 0.75 * np.exp(-c / 1.3) * np.clip(1 - c / 4, 0, 1) ** 0.6, 0)
    test = np.where(c < 4, 0.35 + 0.35 * (c - 1.8) ** 2 / 4.84 * (c > 1.8) + 0.4 * np.exp(-c / 0.6) + 0.42 * np.exp(-((c - 4) / 0.45) ** 2),
                    0.26 + 0.86 * np.exp(-(c - 4) / 1.5) * 0.6 + 0.0)
    test = np.clip(test, 0, 0.98)
    f.rect(f.X(4), 70, f.X(10) - f.X(4), 430, PALE, None, op=0.6)
    f.line(f.X(4), 70, f.X(4), 500, BLUE, 3, "10 9")
    f.curve(c, train, INK, 5, "12 9"); f.curve(c, test, RED, 6)
    f.lab(f.X(4) + 14, 80, "interpolation threshold", 380, cls="axh")
    f.lab(130, 508, "classical regime", f.X(4) - 130, "center", "ax ax-b")
    f.lab(f.X(4), 508, "over-parameterized regime", f.X(10) - f.X(4), "center", "ax ax-b")
    f.lab(f.X(6.3), f.Y(0.52), "test risk", 180, cls="axh", color=RED)
    f.lab(f.X(1.75), f.Y(0.26), "training risk", 230, cls="axh", color=INK)
    return f

CODE = '''model = Net().to(device)
opt = torch.optim.AdamW(model.parameters(),
                        lr=3e-4, weight_decay=0.05)
sched = torch.optim.lr_scheduler.OneCycleLR(
    opt, max_lr=3e-4, total_steps=T, pct_start=0.05)

for x, y in loader:                 # one minibatch
    loss = loss_fn(model(x), y)     # forward pass
    opt.zero_grad(set_to_none=True)
    loss.backward()                 # backpropagation
    nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()                      # AdamW update
    sched.step()                    # warm-up, then cosine'''

def build():
    S = Session(5, "en", "Part II · Advanced track", "Optimization and generalization in deep networks", "How deep networks are trained, why training fails, and why very large models still generalize.")
    S.sec("Opening: a training run that fails in three different ways.")
    S.cover("Welcome to the second part of the course. Part one, in French, gave the vocabulary: data, model, loss, generalization. Part two is for people who will build and publish models: master's students in research tracks, PhD students, and researchers. Each session follows the same pattern: the mathematical object, every symbol explained, a figure, a few lines of code, an exercise. We start with the engine room: optimization. Everything later in the course, transformers, self-supervision, diffusion, is trained with the tools of this session.")
    S.sit("Three runs, three failures", "You train a transformer on 5,000 patient trajectories.<br><br><b>Run 1:</b> the training loss reaches zero, but the validation loss rises after epoch 12.<br><br><b>Run 2:</b> the same code with another seed diverges to NaN at step 400.<br><br><b>Run 3:</b> with a smaller learning rate, nothing happens for hours.",
          "What actually controls whether a deep network trains, and whether it generalizes?",
          "Here is a situation most of you will meet in your first month. You train a transformer on five thousand patient trajectories. In the first run, the training loss goes to zero but the validation loss starts rising after epoch twelve. In the second run, same code, different random seed, the loss becomes not-a-number at step four hundred. In the third, with a smaller learning rate, the loss barely moves for hours. Three different failures. By the end of this session you should be able to name the cause of each one and know what to change first.")
    S.obj(["Write learning as regularized empirical risk minimization, and derive the usual losses from likelihoods.", "Explain backpropagation as reverse-mode automatic differentiation.", "Choose and tune an optimizer, a learning-rate schedule and a regularizer.", "Diagnose a failed run from its learning curves."],
          "Four objectives. First, write the learning problem formally, and see that the usual losses are negative log-likelihoods. Second, explain backpropagation as reverse-mode automatic differentiation, which is what your framework does when you call backward. Third, choose and tune an optimizer, a schedule and a regularizer with reasons rather than habits. Fourth, read learning curves and diagnose a failed run.")
    S.plan([("The objective", "Empirical risk, likelihood, and the noise model behind a loss"), ("Gradients", "Backpropagation as the chain rule on a graph"), ("Optimizers and schedules", "SGD, momentum, Adam, AdamW, warm-up and decay"), ("Trainability and regularization", "Initialization, normalization, residual paths, weight decay"), ("Generalization and debugging", "Double descent, and a routine for failed runs")],
           "The session has five parts. We define what we minimize. We see how gradients are computed. We go through the optimizers you will actually use, and the learning-rate schedule. We look at what makes deep networks trainable at all, and how they are regularized. We end with generalization in the over-parameterized regime, and a debugging routine.")
    S.sec("The objective: empirical risk minimization, and losses as negative log-likelihoods.")
    S.eq("Learning as empirical risk minimization", "The one formula behind every model in this course.", r"\hat{\theta} = \arg\min_{\theta}\ \frac{1}{n}\sum_{i=1}^{n}\ell\left(f_\theta(x_i),\,y_i\right) + \lambda\,\Omega(\theta)",
         [(r"f_\theta", "The <b>network</b>, a function with parameters θ (all weights and biases)."), (r"\ell", "The <b>per-example loss</b>: how wrong the prediction is for example i."),
          (r"\frac{1}{n}\sum_{i=1}^{n}", "The <b>empirical risk</b>: the average loss over the n training examples. It estimates the expected loss on the whole population."),
          (r"\lambda\,\Omega(\theta)", "The <b>regularizer</b>, for instance the squared norm of the weights, with strength λ."), (r"\hat{\theta}", "The parameters we keep: an approximate minimizer found by gradient descent.")],
         "This is the formula behind every model in the course. Theta denotes all the parameters. f theta is the network. The loss, written ell, measures how wrong the prediction is for one example. We average it over the n training examples: that average is the empirical risk. It is only an estimate of what we really care about, the expected loss over the whole population of future patients. The last term is a regularizer, with strength lambda. Theta hat is what we keep. Two honest remarks: the problem is non-convex, so we find a good solution rather than the minimum; and the gap between empirical and population risk is exactly the generalization gap from session three.",
         band="We minimize the empirical risk, but we care about the population risk.")
    S.eq("A loss is a negative log-likelihood", "Mean squared error and cross-entropy are two cases of the same principle.",
         [r"-\log \mathcal{N}\left(y;\ f_\theta(x),\ \sigma^2\right) = \frac{\left(y - f_\theta(x)\right)^2}{2\sigma^2} + \mathrm{const}", r"-\log \mathrm{Cat}\left(y;\ \mathrm{softmax}(f_\theta(x))\right) = -\sum_{c} y_c \log p_\theta(c\,|\,x)"],
         [(r"\mathcal{N}(y;\,\mu,\,\sigma^2)", "A <b>Gaussian</b> density for the target, centred on the network output. Its negative log is the squared error: MSE assumes additive noise of constant variance."),
          (r"\mathrm{Cat}", "A <b>categorical</b> distribution over classes. Its negative log is the cross-entropy."),
          (r"\mathrm{softmax}", "Turns the network outputs (logits) into probabilities that sum to one."), (r"y_c", "1 for the true class c, 0 otherwise (one-hot target).")],
         "Where do losses come from? From likelihoods. Assume the target is the network output plus Gaussian noise of constant variance. The negative log-density is the squared error divided by two sigma squared, plus a constant: minimizing the mean squared error is maximum likelihood under that noise model. Assume instead a categorical distribution over classes, with probabilities given by a softmax of the network outputs. The negative log-likelihood is the cross-entropy. This is practical. Drug concentrations usually have proportional error, larger at high concentrations. Plain MSE is then the wrong noise model: train on log-concentrations, or let the network predict the variance as well.",
         band="Choosing a loss is choosing a noise model. For concentrations, think proportional error.")
    S.sec("Gradients: backpropagation as the chain rule on a computation graph.")
    S.eq("Backpropagation is the chain rule, run backwards", "Two layers, one loss.", r"\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial \hat{y}}\cdot\frac{\partial \hat{y}}{\partial h}\cdot\frac{\partial h}{\partial z}\cdot\frac{\partial z}{\partial W_1}",
         [(r"\frac{\partial L}{\partial \hat{y}}", "How the loss changes with the prediction: the starting signal of the backward pass."), (r"\frac{\partial h}{\partial z}", "A <b>local derivative</b>; for ReLU it is 1 where z is positive and 0 elsewhere. One backward pass costs about one forward pass and yields the gradient for every weight.")],
         "How do we get the gradient with respect to millions of weights? With the chain rule, organized cleverly. Take a two-layer network: z equals W one x, h is ReLU of z, y hat equals W two h, then the loss. The forward pass computes and stores each intermediate value. The backward pass starts from the derivative of the loss with respect to the prediction and multiplies by the local derivative of each operation, going right to left. One backward pass yields the gradient for every weight, at roughly the cost of one forward pass. This is reverse-mode automatic differentiation. Note the ReLU factor: where z is negative, the gradient is exactly zero, which is how units die.",
         fig=fig_graph(), figtop=True)
    S.sec("Optimizers and schedules: SGD with momentum, Adam and AdamW, warm-up and cosine decay.")
    S.eq("Stochastic gradient descent with momentum", "A noisy gradient from a minibatch, averaged over time.",
         [r"g_t = \frac{1}{|B_t|}\sum_{i\in B_t}\nabla_\theta\,\ell\left(f_{\theta_t}(x_i),\,y_i\right)", r"v_{t+1} = \mu\,v_t + g_t\qquad\qquad \theta_{t+1} = \theta_t - \eta\,v_{t+1}"],
         [(r"B_t", "The <b>minibatch</b> drawn at step t: a few dozen to a few thousand examples."), (r"g_t", "The minibatch gradient: an unbiased but <b>noisy</b> estimate of the full gradient."),
          (r"\eta", "The <b>learning rate</b>: the step size."), (r"\mu,\ v_t", "The <b>momentum</b> coefficient (typically 0.9) and the velocity: a running sum of past gradients.")],
         "Computing the gradient on the whole dataset at each step is too expensive. We draw a minibatch, B t, and average the gradients over it. That gives g t: unbiased, but noisy. The noise is useful, it helps escape sharp regions, and its scale grows with the ratio of learning rate to batch size. That is why, when you multiply the batch size by k, you usually multiply the learning rate by about k as well. Second line: momentum. We keep a velocity v, a running sum of past gradients with decay mu, typically zero point nine, and we step along the velocity. Directions that agree across steps accumulate; directions that oscillate cancel out.",
         band="Gradient noise scales with η / |B|: change the batch size and the learning rate together.")
    S.eq("Adam and AdamW", "A separate step size for each parameter.",
         [r"m_t = \beta_1 m_{t-1} + (1-\beta_1)\,g_t\qquad\quad v_t = \beta_2 v_{t-1} + (1-\beta_2)\,g_t^2", r"\theta_{t+1} = \theta_t - \eta\left(\frac{\hat{m}_t}{\sqrt{\hat{v}_t}+\epsilon} + \lambda\,\theta_t\right)"],
         [(r"m_t", "Running mean of the gradient: momentum. Default β₁ = 0.9."), (r"v_t", "Running mean of the <b>squared</b> gradient, element by element. Default β₂ = 0.999."),
          (r"\hat{m}_t,\ \hat{v}_t", "Bias-corrected versions, m divided by (1 − β₁ᵗ): they compensate for starting at zero."), (r"\epsilon", "A small constant (10⁻⁸) that avoids division by zero."),
          (r"\lambda\,\theta_t", "<b>Decoupled weight decay</b>: shrinks the weights directly. This term is what makes it AdamW.")],
         "Adam keeps two running averages for every parameter. m is the average gradient, as in momentum. v is the average squared gradient. The update divides m by the square root of v: parameters with consistently large gradients take smaller steps, parameters with small gradients take larger ones. In effect each parameter gets its own learning rate. The hats are bias corrections for the first steps, when the averages are still close to their zero initialization. The last term is weight decay applied directly to the weights, outside the adaptive rescaling: that is AdamW. In the original Adam, the decay was added to the gradient and then rescaled, which made the regularization uneven.",
         band="Default for transformers: AdamW with warm-up and cosine decay.")
    S.pts("The learning rate decides everything", "Same model, same data, three step sizes.",
          ["<b>Too small</b>: the loss decreases, but you will not live to see the end.", "<b>Too large</b>: on a quadratic bowl, gradient descent diverges as soon as η exceeds 2 / λ_max, the largest curvature.", "<b>Well chosen</b>: just below the stability limit.", "In practice: sweep on a log grid, three values per decade, before touching anything else."],
          "If you tune one hyperparameter, tune the learning rate. The figure is computed on a simple quadratic bowl with two curvatures, one and twenty. In grey, a learning rate that is too small: the loss goes down, slowly. In blue, a well-chosen value: fast convergence. In red, a value two percent above the stability limit: the loss explodes. For a quadratic, the limit is exactly two divided by the largest eigenvalue of the Hessian, the largest curvature. Deep networks are not quadratic, but the picture holds locally. This is run two of our opening: a seed that happens to visit a region of high curvature, with a learning rate at the edge. The remedy is a sweep on a logarithmic grid.",
          fig=fig_lr(), widget="lr")
    S.pts("Ill-conditioning, and what momentum buys", "Level curves of a loss that is 20 times steeper in one direction than in the other.",
          ["The <b>condition number</b> κ = λ_max / λ_min measures how elongated the valley is.", "Plain gradient descent oscillates across the valley and crawls along it.", "Momentum cancels the oscillations and accumulates speed along the valley.", "Adam rescales each coordinate; normalization layers reshape the valley itself."],
          "Why is optimization hard even on a bowl? Because of conditioning. Here the loss is twenty times steeper vertically than horizontally. The learning rate must be small enough for the steep direction, and is then far too small for the flat one. In red, plain gradient descent: it bounces across the valley and makes slow progress along it. In blue, the same problem with momentum: the vertical oscillations cancel, the horizontal steps add up. Adam attacks the same problem differently, by rescaling each coordinate. Normalization layers and residual connections act on the landscape itself: they make it better conditioned.",
          fig=fig_contour())
    S.eq("Warm-up, then decay", "The learning rate is a function of time, not a constant.", r"\eta_t = \frac{\eta_{\max}}{2}\left(1+\cos\left(\pi\,\frac{t-T_w}{T-T_w}\right)\right)\quad \mathrm{for}\ t \geq T_w",
         [(r"T_w", "<b>Warm-up</b> length: before it, the rate rises linearly from 0 to its peak. Typically 1 to 10 % of training."), (r"T", "Total number of training steps."), (r"\eta_{\max}", "Peak learning rate: the value you sweep.")],
         "In modern training the learning rate is a function of time. First a warm-up: the rate rises linearly from zero to its peak over the first few percent of training. Two reasons. At initialization the curvature is high and large steps are unstable. And Adam's second-moment estimates are unreliable during the first steps. Then a decay, here a half cosine from the peak down to zero. Large steps early explore; small steps late settle into a minimum. If your run diverges right when warm-up ends, the peak is too high. This was the detail in run two.",
         fig=fig_sched())
    S.sec("Trainability and regularization: initialization, normalization, residual paths, and the regularization toolbox.")
    S.cols("Three ideas that made depth trainable", "Without them, signals and gradients vanish or explode across layers.",
           [("Initialization", "Draw weights with variance about 2 / fan-in (He) or 1 / fan-in (Xavier), so that activations and gradients keep the same scale from layer to layer."),
            ("Normalization", "BatchNorm standardizes each feature over the batch; LayerNorm standardizes each example over its features. Both keep activations in a stable range. LayerNorm does not depend on the batch: it is the choice for transformers and small batches."),
            ("Residual connections", "Each block computes a correction that is <b>added</b> to its input. The identity path carries the gradient straight to early layers.")],
           "Thirty layers of plain fully connected units do not train: the signal either dies or explodes on the way. Three ideas fixed this. Initialization: choose the variance of the initial weights so that activations and gradients keep the same scale from layer to layer. For ReLU, that is variance two over fan-in, the He initialization. Normalization: standardize activations inside the network. BatchNorm does it across the batch, LayerNorm across the features of each example. LayerNorm does not depend on batch statistics, which is why transformers use it, and why it is safer with small clinical batches. Residual connections are the third idea, on the next slide.")
    S.eq("The residual block", "The unit of every modern architecture.", [r"x_{l+1} = x_l + F_l\left(\mathrm{Norm}(x_l)\right)", r"\frac{\partial x_L}{\partial x_l} = I + \frac{\partial}{\partial x_l}\sum_{k=l}^{L-1} F_k\left(\mathrm{Norm}(x_k)\right)"],
         [(r"x_l", "The representation entering block l."), (r"F_l", "What the block learns: a <b>correction</b> (attention, convolution or MLP)."), (r"\mathrm{Norm}", "Normalization applied before the block: the <b>pre-norm</b> arrangement used in current transformers."),
          (r"I", "The identity term: whatever F does, a gradient path of gain 1 reaches every earlier layer.")],
         "A residual block adds a learned correction to its input. First line: x of layer l plus one equals x of layer l, plus F of the normalized input. Unroll this across layers and differentiate: second line. The derivative of the last representation with respect to an early one is the identity plus other terms. So whatever the blocks do, there is a path of gain one from the loss to every layer. Gradients cannot vanish through that path. That is why we can train networks with hundreds of layers, and why every architecture in the next sessions, transformers included, is a stack of residual blocks.",
         band="Stacks of pre-norm residual blocks: that is what a transformer is.")
    S.tbl("The regularization toolbox", "They combine; none replaces a clean validation split.", ["Technique", "What it does", "Typical setting"],
          [["Weight decay", "Shrinks weights toward zero at every step", "0.01 to 0.1 with AdamW"], ["Dropout", "Zeroes random activations during training; averaged at test time", "0.1 in transformers"],
           ["Data augmentation", "Shows transformed copies that keep the label", "Domain-specific: the hard part"], ["Early stopping", "Keeps the checkpoint with the best validation loss", "Patience of a few evaluations"],
           ["Label smoothing", "Softens one-hot targets", "0.1; improves calibration"]],
          "Regularization is anything that reduces the generalization gap without touching the data split. Weight decay shrinks the weights at every step. Dropout zeroes random activations during training, which prevents units from co-adapting; remember to switch to evaluation mode at test time. Data augmentation shows transformed copies of the inputs that keep the label. It is the most powerful of the five, and the most domain-specific: what is a label-preserving transformation of a patient trajectory? We come back to that question in session seven. Early stopping keeps the best checkpoint on validation. Label smoothing softens the targets and improves calibration.",
          widths=[22, 46, 32], small=True)
    S.sec("Generalization in the over-parameterized regime, a training loop, and a debugging routine.")
    S.pts("Double descent", "A schematic of test risk against model capacity (after Belkin et al., 2019).",
          ["<b>Classical regime</b>: the U-shaped curve of session 3.", "<b>Interpolation threshold</b>: the model just manages to fit the training set, and test risk peaks.", "<b>Beyond it</b>: bigger models fit the data in smoother ways, and test risk falls again.", "Consequence: do not fear size; validate, and regularize."],
          "Session three showed a U-shaped test error. Yet the networks we train have far more parameters than data points, fit the training set perfectly, and generalize. Both are true; this schematic reconciles them. On the left, the classical regime with its U. At the interpolation threshold, where the model has just enough capacity to fit the training set exactly, the test risk peaks: there is essentially one way to fit the data, and it is a contorted one. Beyond the threshold there are many solutions that fit the data, and gradient descent with weight decay tends to find smooth ones. Test risk falls again. The practical message: a larger model is not automatically a more over-fitted model. The curve is a schematic, not measured data.",
          fig=fig_dd())
    S.code("A training loop you can defend", "Twelve lines, each of which you can now explain.", CODE,
           ["<b>AdamW</b> with decoupled weight decay.", "<b>OneCycleLR</b>: 5 % warm-up, then cosine decay to zero.", "<b>zero_grad</b> before <b>backward</b>: gradients accumulate otherwise.", "<b>Gradient clipping</b> at norm 1.0: cheap insurance against a rare exploding batch."],
           "Here is the whole session in twelve lines of PyTorch. AdamW with a peak learning rate of three ten to the minus four and weight decay zero point zero five. A one-cycle schedule with five percent warm-up and cosine decay. In the loop: forward pass, zero the gradients, backward pass, clip the gradient norm at one, optimizer step, scheduler step. Three classic bugs live here. Forgetting zero grad, so gradients accumulate across steps. Calling the scheduler once per epoch when it expects one call per step. And evaluating without switching the model to evaluation mode, which leaves dropout active.")
    S.tbl("A debugging routine", "Read the curves before changing the model.", ["Symptom", "Likely cause", "First thing to try"],
          [["Loss becomes NaN or explodes", "Learning rate too high; log of zero; exploding gradients", "Divide the rate by 10; clip gradients; check inputs for NaN"],
           ["Training loss does not move", "Rate too low; labels misaligned; dead units", "Overfit a single batch first"],
           ["Training falls, validation rises", "Over-fitting, or a shift between splits", "Regularize, early-stop; audit the split"],
           ["Validation better than training", "Dropout or augmentation in training only; or leakage", "Evaluate the training set in eval mode; audit the split"],
           ["Results change with the seed", "Small data, unstable optimization", "Report mean and standard deviation over at least 5 seeds"]],
          "A routine for failed runs. If the loss is not-a-number: the learning rate first, then gradient clipping, then look for a logarithm of zero or a missing value in the inputs. If the training loss does not move: before anything else, try to overfit a single batch. If the model cannot memorize thirty-two examples, there is a bug, usually in the data pipeline or the labels. If training falls while validation rises: over-fitting, or a shift between your splits. If validation is better than training: often just dropout, but check for leakage. And if results change with the seed, which is the rule with small clinical datasets, report the mean and standard deviation over several seeds.",
          widths=[26, 36, 38], small=True, band="First test of any new pipeline: can the model overfit one batch?")
    S.ex("Diagnose three runs", ["Run A, 10 classes: the training loss stays at 2.30 for 5 epochs.", "Run B: training loss 0.02; validation loss 1.4 and rising; validation accuracy fell from 81 % to 74 %.", "Run C: loss 0.9, 0.7, 4.1, 37, NaN, right after warm-up ends.", "For each run: one diagnosis and two actions. Then: you move from batch size 64 to 512 without changing the learning rate. What happens to the gradient noise, and what do you change?"],
         dict(time="8 minutes", mat="Paper; a calculator for ln 10", out="Three diagnoses, six actions, one scaling rule"),
         "Your turn. Three runs. Run A is a ten-class problem and the training loss stays at two point three for five epochs. Run B has training loss zero point zero two, validation loss one point four and rising, and validation accuracy falling from eighty-one to seventy-four percent. Run C prints zero point nine, zero point seven, four point one, thirty-seven, then not-a-number, just after warm-up ends. For each, give one diagnosis and two actions. Last question: you go from batch size sixty-four to five hundred and twelve without changing the learning rate. What happens to the gradient noise, and what do you change? Eight minutes.")
    S.sol("Diagnose three runs", ["<b>A</b>: ln 10 = 2.30, the loss of uniform guessing. The model learns nothing: overfit one batch, check labels and learning rate.", "<b>B</b>: over-fitting. Early-stop near the best validation loss; add weight decay, dropout or augmentation; get more data.", "<b>C</b>: peak learning rate too high. Lower it, lengthen warm-up, clip gradients.", "<b>Batch ×8</b>: noise scale η / |B| falls 8-fold and there are 8 times fewer updates per epoch. Raise η (up to ×8, with warm-up) or train longer."],
          "Solutions. Run A: two point three is the natural logarithm of ten, the cross-entropy of a uniform guess over ten classes. The model outputs equal probabilities and learns nothing. Overfit a single batch, check that labels are aligned with inputs, and check the learning rate. Run B is over-fitting: early-stop, regularize, or get more data. Run C diverges when the learning rate reaches its peak: lower the peak, lengthen the warm-up, clip gradients. For the batch size: the noise scale is the learning rate over the batch size, so it falls eight-fold, and you take eight times fewer steps per epoch. The linear scaling rule says: multiply the learning rate by up to eight, with warm-up, and check stability.")
    S.quiz([("Minimizing mean squared error is maximum likelihood under:", ["Laplace noise", "Gaussian noise of constant variance", "Bernoulli outcomes"], 1, "The negative log of a Gaussian density is the squared error, up to constants."),
            ("In AdamW, weight decay is:", ["Added to the gradient, then rescaled", "Applied directly to the weights", "Another name for dropout"], 1, "Decoupling the decay from the adaptive rescaling is the point of AdamW."),
            ("Why do residual connections help very deep networks train?", ["They add parameters", "They provide an identity path for gradients", "They remove the need for data"], 1, "The Jacobian contains an identity term, so gradients reach early layers undiminished.")],
           "Three questions. Mean squared error corresponds to Gaussian noise of constant variance. In AdamW, the decay is applied directly to the weights, outside the adaptive rescaling. Residual connections help because the identity path carries gradients to early layers.")
    S.take(["Training is regularized empirical risk minimization; the loss encodes a noise model.", "Backpropagation gives all gradients at the cost of about one forward pass.", "AdamW with warm-up and cosine decay is a sound default; the learning rate is the first thing to tune.", "Normalization and residual paths make depth trainable.", "Large models can generalize: validate and regularize, and debug from the curves."],
           "Five takeaways. Training is regularized empirical risk minimization, and the loss encodes a noise model. Backpropagation gives all gradients for about the cost of one forward pass. AdamW with warm-up and cosine decay is a sound default, and the learning rate is the first thing to tune. Normalization and residual paths make depth trainable. Large models can generalize: validate, regularize, and debug from the curves, not from intuition.")
    S.refs(["I. Goodfellow, Y. Bengio, A. Courville, <i>Deep Learning</i>, MIT Press, 2016 (chapters 6 to 8).", "S. J. D. Prince, <i>Understanding Deep Learning</i>, MIT Press, 2023 (chapters 6 to 9; udlbook.com).",
            "D. P. Kingma, J. Ba, “Adam: A Method for Stochastic Optimization”, <i>ICLR</i>, 2015.", "I. Loshchilov, F. Hutter, “Decoupled Weight Decay Regularization”, <i>ICLR</i>, 2019.",
            "K. He, X. Zhang, S. Ren, J. Sun, “Deep Residual Learning for Image Recognition”, <i>CVPR</i>, 2016.", "M. Belkin, D. Hsu, S. Ma, S. Mandal, “Reconciling modern machine-learning practice and the classical bias–variance trade-off”, <i>PNAS</i>, 2019; 116(32): 15849–15854."],
           "References. Two textbooks: Goodfellow, Bengio and Courville for the classical view, and Prince for a recent, very visual treatment that is free online. Then the original papers for Adam, AdamW, residual networks and double descent.")
    S.end("Session 6 · Attention and transformers", "That is the end of session five. You now have the training machinery. Next session we build the architecture that this machinery is most often applied to today: attention and the transformer.")
    return S
