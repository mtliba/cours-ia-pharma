const WIDGETS = {};
const C = { ink: '#101B3F', mute: '#5A6379', rule: '#D9DDE6', blue: '#2A46C8', red: '#D22B3A', amber: '#C77700', grey: '#7F88A0', pale: '#E9EDFB' };
let UID = 0;
function el(h) { const t = document.createElement('template'); t.innerHTML = h.trim(); return t.content.firstElementChild; }
function slider(host, label, min, max, step, val, fmt) {
  const id = 'ctl' + (++UID), f = fmt || (v => v);
  const l = el(`<label for="${id}">${label}<input type="range" id="${id}" min="${min}" max="${max}" step="${step}" value="${val}"><output for="${id}"></output></label>`);
  host.appendChild(l); const i = l.querySelector('input'), o = l.querySelector('output');
  const upd = () => { o.textContent = f(+i.value); }; i.addEventListener('input', upd); upd(); return i;
}
function frame(w, label) {
  const ctl = el('<div class="ctl"></div>'), cv = el('<canvas role="img"></canvas>'), read = el('<p class="read" aria-live="polite"></p>');
  cv.setAttribute('aria-label', label || 'Interactive figure'); w.append(ctl, cv, read); return { ctl, cv, read };
}
function plot(cv, o) {
  const dpr = window.devicePixelRatio || 1, W = cv.clientWidth || 600, H = cv.clientHeight || 300;
  cv.width = W * dpr; cv.height = H * dpr; const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  const L = 60, R = 14, T = 24, B = o.xl ? 48 : 30;
  const X = v => L + (v - o.xr[0]) / (o.xr[1] - o.xr[0]) * (W - L - R), Y = v => H - B - (v - o.yr[0]) / (o.yr[1] - o.yr[0]) * (H - T - B);
  c.font = '14px "Source Sans 3", Arial, sans-serif'; c.lineWidth = 1; c.strokeStyle = C.rule; c.fillStyle = C.mute;
  (o.yt || []).forEach(v => { c.beginPath(); c.moveTo(L, Y(v)); c.lineTo(W - R, Y(v)); c.stroke(); c.textAlign = 'right'; c.textBaseline = 'middle'; c.fillText(o.yf ? o.yf(v) : v, L - 8, Y(v)); });
  (o.xt || []).forEach(v => { if (o.xgrid !== false) { c.beginPath(); c.moveTo(X(v), T); c.lineTo(X(v), H - B); c.stroke(); } c.textAlign = 'center'; c.textBaseline = 'top'; c.fillText(o.xf ? o.xf(v) : v, X(v), H - B + 6); });
  c.strokeStyle = C.mute; c.lineWidth = 1.5; c.beginPath(); c.moveTo(L, T); c.lineTo(L, H - B); c.lineTo(W - R, H - B); c.stroke();
  c.fillStyle = C.ink; c.font = '600 14px "Source Sans 3", Arial, sans-serif';
  if (o.xl) { c.textAlign = 'center'; c.textBaseline = 'bottom'; c.fillText(o.xl, (L + W - R) / 2, H - 4); }
  if (o.yl) { c.textAlign = 'left'; c.textBaseline = 'top'; c.fillText(o.yl, L, 2); }
  c.save(); c.beginPath(); c.rect(L, T, W - L - R, H - T - B); c.clip(); o.draw(c, X, Y); c.restore();
}
function line(c, X, Y, xs, ys, col, lw, dash) { c.strokeStyle = col; c.lineWidth = lw || 2.5; c.setLineDash(dash || []); c.beginPath(); xs.forEach((x, i) => { i ? c.lineTo(X(x), Y(ys[i])) : c.moveTo(X(x), Y(ys[i])); }); c.stroke(); c.setLineDash([]); }
function dots(c, X, Y, xs, ys, col, r) { xs.forEach((x, i) => { c.fillStyle = col; c.beginPath(); c.arc(X(x), Y(ys[i]), r || 5, 0, 7); c.fill(); c.strokeStyle = '#fff'; c.lineWidth = 1.5; c.stroke(); }); }
function barchart(cv, labels, vals, cols, yl) {
  plot(cv, { xr: [0, labels.length], yr: [0, 1], yt: [0, 0.25, 0.5, 0.75, 1], xt: labels.map((_, k) => k + 0.5), xf: v => labels[Math.floor(v)], xgrid: false, yl,
    draw(c, X, Y) { vals.forEach((v, k) => { if (v == null) return; c.fillStyle = cols[k]; c.fillRect(X(k + 0.18), Y(v), X(k + 0.82) - X(k + 0.18), Y(0) - Y(v)); c.fillStyle = C.ink; c.font = '600 13px "Source Sans 3", Arial'; c.textAlign = 'center'; c.textBaseline = 'bottom'; c.fillText(v.toFixed(2), X(k + 0.5), Y(v) - 3); }); } });
}
const fr = (v, n) => v.toFixed(n).replace('.', ',').replace('-', '−');
const softmax = a => { const m = Math.max(...a), e = a.map(v => Math.exp(v - m)), s = e.reduce((p, q) => p + q, 0); return e.map(v => v / s); };

WIDGETS.fitline = function (w) {
  const d = DATA.a1, f = frame(w, 'Droite ajustable sur douze patients');
  const sw = slider(f.ctl, 'Pente w', 0, 2, 0.01, 0.4, v => fr(v, 2)), sb = slider(f.ctl, 'Décalage b', -2, 8, 0.1, 3, v => fr(v, 1));
  const b1 = el('<button type="button" class="btn ghost">10 pas de descente</button>'), b2 = el('<button type="button" class="btn ghost">Meilleure droite</button>'); f.ctl.append(b1, b2);
  const mse = (W, B) => d.x.reduce((s, x, i) => s + (d.y[i] - (W * x + B)) ** 2, 0) / d.x.length;
  function draw() {
    const W = +sw.value, B = +sb.value;
    plot(f.cv, { xr: [0, 12], yr: [0, 16], xt: [0, 2, 4, 6, 8, 10, 12], yt: [0, 4, 8, 12, 16], xl: 'Dose (mg/jour)', yl: 'Concentration (ng/mL)',
      draw(c, X, Y) { d.x.forEach((x, i) => { c.strokeStyle = C.red; c.lineWidth = 2; c.beginPath(); c.moveTo(X(x), Y(d.y[i])); c.lineTo(X(x), Y(W * x + B)); c.stroke(); }); line(c, X, Y, [0, 12], [B, 12 * W + B], C.blue, 3); dots(c, X, Y, d.x, d.y, C.ink); } });
    f.read.innerHTML = `Erreur moyenne : <b>${fr(mse(W, B), 2)}</b> · minimum possible : ${fr(mse(d.w, d.b), 2)}. Les segments rouges sont les écarts.`;
  }
  const set = (W, B) => { sw.value = W; sb.value = B; sw.dispatchEvent(new Event('input')); sb.dispatchEvent(new Event('input')); };
  b1.onclick = () => { let W = +sw.value, B = +sb.value; for (let k = 0; k < 10; k++) { let gw = 0, gb = 0; d.x.forEach((x, i) => { const e = W * x + B - d.y[i]; gw += 2 * e * x / d.x.length; gb += 2 * e / d.x.length; }); W -= 0.008 * gw; B -= 0.008 * gb; } set(W, B); };
  b2.onclick = () => set(d.w, d.b); sw.addEventListener('input', draw); sb.addEventListener('input', draw); w._draw = draw; draw();
};

WIDGETS.logistic = function (w) {
  const d = DATA.a2, f = frame(w, 'Courbe logistique ajustable'), sig = z => 1 / (1 + Math.exp(-z));
  const sw = slider(f.ctl, 'Poids w', 0, 3, 0.01, d.w, v => fr(v, 2)), sb = slider(f.ctl, 'Biais b', -20, 0, 0.1, d.b, v => fr(v, 1));
  function draw() {
    const W = +sw.value, B = +sb.value, xs = Array.from({ length: 121 }, (_, i) => i / 10);
    plot(f.cv, { xr: [0, 12], yr: [-0.06, 1.06], xt: [0, 2, 4, 6, 8, 10, 12], yt: [0, 0.25, 0.5, 0.75, 1], yf: v => Math.round(v * 100) + ' %', xl: 'Dose (mg/jour)', yl: 'Probabilité de surexposition',
      draw(c, X, Y) { line(c, X, Y, [0, 12], [0.5, 0.5], C.red, 1.5, [6, 5]); line(c, X, Y, xs, xs.map(x => sig(W * x + B)), C.blue, 3); d.x.forEach((x, i) => dots(c, X, Y, [x], [d.y[i]], d.y[i] ? C.red : C.ink, 4.5)); } });
    const ll = -d.x.reduce((s, x, i) => { const p = Math.min(1 - 1e-9, Math.max(1e-9, sig(W * x + B))); return s + (d.y[i] ? Math.log(p) : Math.log(1 - p)); }, 0) / d.x.length;
    f.read.innerHTML = `Risque annoncé à 8 mg/jour : <b>${Math.round(sig(W * 8 + B) * 100)} %</b> · coût du modèle sur ces 30 visites : <b>${fr(ll, 3)}</b> (plus petit = mieux).`;
  }
  sw.addEventListener('input', draw); sb.addEventListener('input', draw); w._draw = draw; draw();
};

WIDGETS.overfit = function (w) {
  const d = DATA.a3, f = frame(w, 'Polynôme de degré réglable sur dix mesures');
  const sd = slider(f.ctl, 'Souplesse (degré du polynôme)', 1, 9, 1, 3);
  function draw() {
    const g = +sd.value;
    plot(f.cv, { xr: [0, 24], yr: [0, 120], xt: [0, 6, 12, 18, 24], yt: [0, 30, 60, 90, 120], xl: 'Concentration (ng/mL)', yl: 'Effet mesuré (%)',
      draw(c, X, Y) { line(c, X, Y, d.xs, d.fits[g], g >= 7 ? C.red : C.blue, 3); dots(c, X, Y, d.x, d.y, C.ink); } });
    const msg = g <= 1 ? 'trop simple : sous-apprentissage' : g >= 7 ? '<span class="warn">trop souple : le modèle suit le bruit</span>' : 'compromis raisonnable';
    f.read.innerHTML = `Erreur d’entraînement : <b>${fr(d.tr[g], 1)}</b> · erreur de test (300 nouvelles mesures) : <b>${fr(d.te[g], 1)}</b> · ${msg}.`;
  }
  sd.addEventListener('input', draw); w._draw = draw; draw();
};

WIDGETS.neuron = function (w) {
  const f = frame(w, 'Sortie d’un neurone ReLU'), wt = [0.8, 1.2, -0.5], b = 0.1; f.cv.style.height = '220px';
  const s = [1, -0.5, 2].map((v, i) => slider(f.ctl, 'x' + '₁₂₃'[i], -2, 2, 0.1, v, x => fr(x, 1)));
  function draw() {
    const x = s.map(i => +i.value), z = x.reduce((p, v, i) => p + v * wt[i], b), a = Math.max(0, z), xs = [-4, 0, 4];
    plot(f.cv, { xr: [-4, 4], yr: [-0.5, 4], xt: [-4, -2, 0, 2, 4], yt: [0, 2, 4], xl: 'Somme pondérée z', yl: 'Sortie a = ReLU(z)',
      draw(c, X, Y) { line(c, X, Y, xs, xs.map(v => Math.max(0, v)), C.blue, 3); dots(c, X, Y, [z], [a], C.red, 7); } });
    f.read.innerHTML = `z = 0,8 × ${fr(x[0], 1)} + 1,2 × ${fr(x[1], 1)} − 0,5 × ${fr(x[2], 1)} + 0,1 = <b>${fr(z, 2)}</b> · sortie a = <b>${fr(a, 2)}</b>${z <= 0 ? ' · neurone éteint' : ''}.`;
  }
  s.forEach(i => i.addEventListener('input', draw)); w._draw = draw; draw();
};

WIDGETS.lr = function (w) {
  const f = frame(w, 'Loss curve of gradient descent for an adjustable learning rate');
  const se = slider(f.ctl, 'Learning rate η', 0.002, 0.12, 0.001, 0.09, v => v.toFixed(3));
  const id = 'ctl' + (++UID), cb = el(`<label for="${id}"><input type="checkbox" id="${id}"> momentum 0.9</label>`); f.ctl.append(cb);
  function run(eta, mu) { const lam = [1, 20]; let x = [-9, 1.6], v = [0, 0]; const L = [0.5 * (81 + 20 * 2.56)]; for (let k = 0; k < 60; k++) { for (let j = 0; j < 2; j++) { v[j] = mu * v[j] + lam[j] * x[j]; x[j] -= eta * v[j]; } L.push(0.5 * (x[0] * x[0] + 20 * x[1] * x[1])); } return L; }
  function draw() {
    const eta = +se.value, mu = cb.querySelector('input').checked ? 0.9 : 0, L = run(eta, mu), lg = L.map(v => Math.max(-6, Math.min(8, Math.log10(Math.max(v, 1e-12)))));
    plot(f.cv, { xr: [0, 60], yr: [-6, 8], xt: [0, 20, 40, 60], yt: [-6, -3, 0, 3, 6], yf: v => '10^' + v, xl: 'Training step', yl: 'Loss (log scale)', draw(c, X, Y) { line(c, X, Y, L.map((_, i) => i), lg, L[60] > L[0] ? C.red : C.blue, 3); } });
    const st = L[60] > L[0] ? '<span class="warn">diverges</span>' : L[60] > 1 ? 'slow' : 'converges';
    f.read.innerHTML = `Loss after 60 steps: <b>${L[60].toExponential(1)}</b> · ${st}. Curvatures 1 and 20: plain gradient descent is stable only below η = 2 / 20 = 0.1.`;
  }
  se.addEventListener('input', draw); cb.querySelector('input').addEventListener('change', draw); w._draw = draw; draw();
};

WIDGETS.attention = function (w) {
  const d = DATA.b2, toks = el('<div class="toks" role="group" aria-label="Token being updated"></div>'); w.append(toks);
  const f = frame(w, 'Attention weights of the selected token'); let q = 5;
  const bs = d.tok.map((t, i) => { const b = el(`<button type="button">${t}</button>`); b.onclick = () => { q = i; draw(); }; toks.appendChild(b); return b; });
  const st = slider(f.ctl, 'Divide the scores by', 0.3, 3, 0.1, 1, v => v.toFixed(1));
  function draw() {
    bs.forEach((b, i) => b.classList.toggle('on', i === q));
    const T = +st.value, p = softmax(d.sc[q].slice(0, q + 1).map(v => v / T)), vals = d.tok.map((_, j) => j <= q ? p[j] : null);
    barchart(f.cv, d.tok, vals, d.tok.map((_, j) => j === q ? C.grey : C.blue), 'Attention weight');
    const best = p.indexOf(Math.max(...p));
    f.read.innerHTML = `“${d.tok[q]}” puts most weight on <b>“${d.tok[best]}”</b> (${p[best].toFixed(2)}). Later events are masked. Illustrative scores, not a trained model.`;
  }
  st.addEventListener('input', draw); w._draw = draw; draw();
};

WIDGETS.temperature = function (w) {
  const s = DATA.b3.sims, f = frame(w, 'Softmax over one positive and five negatives for an adjustable temperature');
  const st = slider(f.ctl, 'Temperature τ', 0.02, 1, 0.01, 0.2, v => v.toFixed(2)), labels = ['0.9 positive', '0.7 hard', '0.3', '0.0', '−0.2', '−0.5'];
  function draw() {
    const p = softmax(s.map(v => v / +st.value));
    barchart(f.cv, labels, p, labels.map((_, k) => k ? C.grey : C.blue), 'Probability');
    f.read.innerHTML = `Probability of the positive: <b>${p[0].toFixed(3)}</b> · loss −log p = <b>${(-Math.log(p[0])).toFixed(3)}</b> · share of the negatives' mass on the hardest one: <b>${(100 * p[1] / (1 - p[0] + 1e-12)).toFixed(0)} %</b>.`;
  }
  st.addEventListener('input', draw); w._draw = draw; draw();
};

WIDGETS.diffusion = function (w) {
  const d = DATA.b4, f = frame(w, 'A ring of points progressively replaced by Gaussian noise');
  const sa = slider(f.ctl, 'Signal kept ᾱ (drag left to add noise)', 0, 1, 0.01, 1, v => v.toFixed(2));
  function draw() {
    const ab = +sa.value, cv = f.cv, dpr = window.devicePixelRatio || 1, W = cv.clientWidth || 600, H = cv.clientHeight || 300;
    cv.width = W * dpr; cv.height = H * dpr; const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
    const k = Math.min(W, H) / 6.4; c.fillStyle = '#F2F4F8'; c.fillRect(W / 2 - 3.1 * k, H / 2 - 3.1 * k, 6.2 * k, 6.2 * k);
    d.ring.forEach((p, i) => { const x = Math.sqrt(ab) * p[0] + Math.sqrt(1 - ab) * d.eps[i][0], y = Math.sqrt(ab) * p[1] + Math.sqrt(1 - ab) * d.eps[i][1]; c.fillStyle = ab > 0.02 ? C.blue : C.grey; c.beginPath(); c.arc(W / 2 + Math.max(-3, Math.min(3, x)) * k, H / 2 - Math.max(-3, Math.min(3, y)) * k, 4, 0, 7); c.fill(); });
    f.read.innerHTML = `x_t = √ᾱ · x₀ + √(1 − ᾱ) · ε, with ᾱ = <b>${ab.toFixed(2)}</b> · signal-to-noise ratio: <b>${ab >= 1 ? '∞' : (ab / (1 - ab)).toFixed(2)}</b>. The reverse process is what the network learns.`;
  }
  sa.addEventListener('input', draw); w._draw = draw; draw();
};

WIDGETS.lora = function (w) {
  const ctl = el('<div class="ctl"></div>'), read = el('<p class="read" aria-live="polite"></p>'); w.append(ctl, read);
  const mk = (label, v) => { const id = 'ctl' + (++UID), l = el(`<label for="${id}">${label}<input type="number" id="${id}" min="1" max="100000" step="1" value="${v}"></label>`); ctl.append(l); return l.querySelector('input'); };
  const d = mk('d', 4096), k = mk('k', 4096), r = mk('rank r', 8);
  function draw() {
    const D = Math.max(1, +d.value || 1), K = Math.max(1, +k.value || 1), R = Math.max(1, Math.min(+r.value || 1, Math.min(D, K))), full = D * K, lo = R * (D + K);
    read.innerHTML = `Full matrix: <b>${full.toLocaleString('en-US')}</b> weights · LoRA update: <b>${lo.toLocaleString('en-US')}</b> weights · <b>${(100 * lo / full).toFixed(2)} %</b> of the matrix.`;
  }
  [d, k, r].forEach(i => i.addEventListener('input', draw)); draw();
};

WIDGETS.pk = function (w) {
  const f = frame(w, 'Simulated concentration over three days for adjustable dose, clearance and volume');
  const sd = slider(f.ctl, 'Dose (mg)', 1, 6, 0.5, 3, v => v.toFixed(1)), sc = slider(f.ctl, 'Clearance CL (L/h)', 5, 40, 0.5, 17.5, v => v.toFixed(1)), sv = slider(f.ctl, 'Volume V (L)', 100, 500, 10, 250);
  const id = 'ctl' + (++UID), sel = el(`<label for="${id}">Interval<select id="${id}"><option value="12">12 h</option><option value="24">24 h</option></select></label>`); f.ctl.append(sel);
  function draw() {
    const D = +sd.value, CL = +sc.value, V = +sv.value, tau = +sel.querySelector('select').value, ke = CL / V, ka = 1.5, ts = [], cs = [];
    const conc = t => { let s = 0; for (let k = 0; k * tau <= t; k++) { const u = t - k * tau; s += D * 1000 / V * ka / (ka - ke) * (Math.exp(-ke * u) - Math.exp(-ka * u)); } return s; };
    for (let t = 0; t <= 72; t += 0.2) { ts.push(t); cs.push(conc(t)); }
    const tr = []; for (let t = tau; t <= 72; t += tau) tr.push(t);
    plot(f.cv, { xr: [0, 72], yr: [0, 40], xt: [0, 12, 24, 36, 48, 60, 72], yt: [0, 10, 20, 30, 40], xl: 'Time (hours)', yl: 'Concentration (ng/mL)',
      draw(c, X, Y) { c.fillStyle = C.pale; c.fillRect(X(0), Y(10), X(72) - X(0), Y(5) - Y(10)); line(c, X, Y, ts, cs, C.blue, 3); dots(c, X, Y, tr, tr.map(t => conc(t - 0.01)), C.red, 5); } });
    f.read.innerHTML = `Last trough: <b>${conc(72 - 0.01).toFixed(1)} ng/mL</b> · peak: <b>${Math.max(...cs).toFixed(1)} ng/mL</b> · half-life: <b>${(Math.log(2) / ke).toFixed(1)} h</b>. Illustrative parameters and target band (5 to 10 ng/mL); not dosing advice.`;
  }
  [sd, sc, sv].forEach(i => i.addEventListener('input', draw)); sel.querySelector('select').addEventListener('change', draw); w._draw = draw; draw();
};
