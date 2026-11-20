/* Lecteur du cours : navigation, deux modes d'affichage, questions, code, figures interactives. */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const NS = 'http://www.w3.org/2000/svg';
const S = (tag, a = {}, parent) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); if (parent) parent.appendChild(e); return e; };
const H = html => { const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstChild; };
const fr = (v, d = 1) => v.toFixed(d).replace('.', ',');
const store = { get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} } };
const C1 = '#0A9087', C2 = '#D9741A', INK = '#10283B';
const DESC = ['Notebook, variables, listes, conditions, boucles, fonctions. On écrit un calcul de clairance et on le vérifie à la main.',
  'Lire un fichier CSV, repérer doublons, valeurs manquantes et valeurs impossibles, tenir un journal de nettoyage, résumer par groupe.',
  'Histogramme, boîtes, nuage de points, courbes. On manipule les figures et on apprend à reconnaître celles qui trompent.',
  'Organiser un projet, tester un code proposé par une IA, protéger les données de santé. Mini-projet final.'];
let DATA, ROWS, cur = { n: 0, i: 0 }, mode, su = 1;
const deck = $('#deck'), secs = () => $$('section', deck);

/* ---------- graphiques ---------- */
function plot(host, o) {
  const w = o.w || 856, h = o.h || 520, m = { l: 84, r: 20, t: 20, b: 78 };
  host.innerHTML = '';
  const svg = S('svg', { viewBox: `0 0 ${w} ${h}`, role: 'img', 'aria-label': o.label }, host);
  const X = v => m.l + (v - o.x[0]) / (o.x[1] - o.x[0]) * (w - m.l - m.r), Y = v => h - m.b - (v - o.y[0]) / (o.y[1] - o.y[0]) * (h - m.t - m.b);
  for (const t of o.yt) { S('line', { x1: m.l, x2: w - m.r, y1: Y(t), y2: Y(t), stroke: '#E1E7E8', 'stroke-width': 1.5 }, svg); S('text', { x: m.l - 12, y: Y(t) + 7, 'text-anchor': 'end', 'font-size': 20 }, svg).textContent = fr(t, o.yd || 0); }
  for (const t of o.xt) S('text', { x: X(t.v ?? t), y: h - m.b + 30, 'text-anchor': 'middle', 'font-size': 20 }, svg).textContent = t.l ?? t;
  S('line', { x1: m.l, x2: w - m.r, y1: Y(o.y[0]), y2: Y(o.y[0]), stroke: '#5A6770', 'stroke-width': 2 }, svg);
  S('text', { x: (m.l + w - m.r) / 2, y: h - 14, 'text-anchor': 'middle', 'font-size': 22, 'font-weight': 600 }, svg).textContent = o.xl;
  S('text', { x: 24, y: (m.t + h - m.b) / 2, 'text-anchor': 'middle', 'font-size': 22, 'font-weight': 600, transform: `rotate(-90 24 ${(m.t + h - m.b) / 2})` }, svg).textContent = o.yl;
  return { svg, X, Y, w, h, m };
}
function band(p, a = 5, b = 10, horizontal = true) {
  const r = horizontal ? { x: p.m.l, width: p.w - p.m.l - p.m.r, y: p.Y(b), height: p.Y(a) - p.Y(b) } : { x: p.X(a), width: p.X(b) - p.X(a), y: p.m.t, height: p.h - p.m.t - p.m.b };
  S('rect', Object.assign({ fill: C2, opacity: .18 }, r), p.svg);
  S('text', { x: horizontal ? p.w - p.m.r - 8 : (p.X(a) + p.X(b)) / 2, y: horizontal ? p.Y(b) + 24 : p.m.t + 24, 'text-anchor': horizontal ? 'end' : 'middle', 'font-size': 19 }, p.svg).textContent = 'cible';
}
function tipOn(host, el, text) {
  const tip = $('.tip', host);
  el.addEventListener('pointermove', e => { const r = host.getBoundingClientRect(); tip.hidden = false; tip.textContent = text; tip.style.left = Math.min(e.clientX - r.left + 12, r.width - tip.offsetWidth - 4) + 'px'; tip.style.top = (e.clientY - r.top - 34) + 'px'; });
  el.addEventListener('pointerleave', () => { tip.hidden = true; });
}
function frame(el, w, ctrl) {
  const d = H(`<div class="wg" style="width:calc(${w} * var(--u))">${ctrl ? `<div class="wg-c">${ctrl}</div>` : ''}<div class="wg-p"></div><div class="tip" hidden></div></div>`);
  el.replaceWith(d); return d;
}
const median = a => { const s = [...a].sort((x, y) => x - y), n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };
const byVisit = () => [7, 14, 30, 60, 90, 180].map(j => ({ j, m: median(ROWS.filter(r => r.j === j).map(r => r.c)) }));

function spag(host, o = {}) {
  const p = plot($('.wg-p', host), { h: o.h, x: [0, 186], y: [0, 26], xt: [7, 30, 60, 90, 180].map(v => ({ v, l: 'J' + v })), yt: [0, 5, 10, 15, 20, 25], xl: 'Jours après la greffe', yl: 'C0 (ng/mL)', label: 'Concentration résiduelle de chaque patient au cours du suivi' });
  band(p);
  const ids = [...new Set(ROWS.map(r => r.p))];
  ids.forEach((id, k) => {
    const d = ROWS.filter(r => r.p === id).map((r, i) => (i ? 'L' : 'M') + p.X(r.j).toFixed(1) + ' ' + p.Y(r.c).toFixed(1)).join('');
    const line = S('path', { d, fill: 'none', stroke: C1, 'stroke-width': 2.5, opacity: .32, pathLength: 1 }, p.svg);
    if (o.animate) { line.classList.add('draw'); line.style.animationDelay = k * 28 + 'ms'; }
    const hit = S('path', { d, fill: 'none', stroke: 'transparent', 'stroke-width': 14 }, p.svg);
    hit.addEventListener('pointerenter', () => { line.setAttribute('opacity', 1); line.setAttribute('stroke-width', 5); });
    hit.addEventListener('pointerleave', () => { line.setAttribute('opacity', .32); line.setAttribute('stroke-width', 2.5); });
    tipOn(host, hit, 'Patient ' + id);
  });
  if (o.median !== false) S('path', { d: byVisit().map((v, i) => (i ? 'L' : 'M') + p.X(v.j) + ' ' + p.Y(v.m)).join(''), fill: 'none', stroke: INK, 'stroke-width': 5, 'stroke-linecap': 'round', 'pointer-events': 'none' }, p.svg);
}

const W = {
  courbes(el) {
    const d = frame(el, 856, '<label><input type="checkbox" checked> Afficher la médiane</label><span class="key"><i style="background:#0A9087"></i>un patient</span><span class="key"><i style="background:#10283B"></i>médiane</span>');
    const cb = $('input', d), draw = () => spag(d, { median: cb.checked, h: 500 }); cb.oninput = draw; draw();
  },
  hist(el) {
    const d = frame(el, 856, '<label>Nombre de classes <input type="range" min="4" max="42" value="20"><output>20</output></label><label><input type="checkbox" checked> Afficher la cible</label>');
    const [rg, cb] = $$('input', d), out = $('output', d), vals = ROWS.map(r => r.c);
    const draw = () => {
      const n = +rg.value, a = 4, b = 25, step = (b - a) / n, cnt = Array(n).fill(0); out.textContent = n;
      vals.forEach(v => cnt[Math.min(n - 1, Math.floor((v - a) / step))]++);
      const top = Math.ceil(Math.max(...cnt) / 10) * 10, yt = []; for (let t = 0; t <= top; t += top > 40 ? 20 : 10) yt.push(t);
      const p = plot($('.wg-p', d), { h: 500, x: [a, b], y: [0, top], xt: [5, 10, 15, 20, 25], yt, xl: 'C0 (ng/mL)', yl: 'Nombre de dosages', label: 'Histogramme des concentrations résiduelles' });
      if (cb.checked) band(p, 5, 10, false);
      cnt.forEach((c, i) => { if (!c) return; const x = p.X(a + i * step) + 1, r = S('rect', { x, width: Math.max(1, p.X(a + (i + 1) * step) - x - 1), y: p.Y(c), height: p.Y(0) - p.Y(c), fill: C1, rx: 3 }, p.svg); tipOn(d, r, `${fr(a + i * step)} à ${fr(a + (i + 1) * step)} ng/mL : ${c} dosages`); });
    };
    rg.oninput = cb.oninput = draw; draw();
  },
  nuage(el) {
    const d = frame(el, 856, '<label><input type="checkbox"> Colorer selon le CYP3A5</label><span class="key"><i style="background:#0A9087"></i>expresseur</span><span class="key"><i style="background:#D9741A"></i>non-expresseur</span>');
    const cb = $('input', d), keys = $$('.key', d);
    const draw = () => {
      keys.forEach(k => k.hidden = !cb.checked);
      const p = plot($('.wg-p', d), { h: 500, x: [0, 18], y: [0, 26], xt: [2, 4, 6, 8, 10, 12, 14, 16], yt: [0, 5, 10, 15, 20, 25], xl: 'Dose (mg/j)', yl: 'C0 (ng/mL)', label: 'Nuage de points de la dose et de la concentration' });
      ROWS.forEach(r => { const c = S('circle', { cx: p.X(r.d), cy: p.Y(r.c), r: 7, fill: !cb.checked ? '#5A6770' : r.g === 'expresseur' ? C1 : C2, stroke: '#fff', 'stroke-width': 2, opacity: .85 }, p.svg); tipOn(d, c, `${r.p}, J${r.j} : ${fr(r.d)} mg/j, ${fr(r.c)} ng/mL${cb.checked ? ', ' + r.g : ''}`); });
    };
    cb.oninput = draw; draw();
  },
  tronque(el) {
    const d = frame(el, 1060, '<label>L’axe vertical commence à <input type="range" min="0" max="7" step="0.5" value="7"><output>7</output></label><span class="say"></span>');
    const rg = $('input', d), out = $('output', d), say = $('.say', d), v = byVisit(), a = v[2].m, b = v[5].m;
    const draw = () => {
      const y0 = +rg.value; out.textContent = fr(y0);
      const yt = []; for (let t = Math.ceil(y0); t <= 10; t += y0 > 3 ? 1 : 2) yt.push(t);
      const p = plot($('.wg-p', d), { w: 1060, h: 500, x: [0, 2], y: [y0, 10.5], xt: [{ v: .5, l: 'J30' }, { v: 1.5, l: 'J180' }], yt, xl: 'Visite', yl: 'C0 médiane (ng/mL)', label: 'Deux barres dont la hauteur dépend du début de l’axe' });
      [[.5, a, C1], [1.5, b, C2]].forEach(([x, val, col]) => { S('rect', { x: p.X(x) - 110, width: 220, y: p.Y(val), height: p.Y(y0) - p.Y(val), fill: col, rx: 4 }, p.svg); S('text', { x: p.X(x), y: p.Y(val) - 10, 'text-anchor': 'middle', 'font-size': 24, 'font-weight': 700 }, p.svg).textContent = fr(val); });
      say.textContent = `À l’écran, la barre J180 mesure ${Math.round((b - y0) / (a - y0) * 100)} % de la barre J30. Les valeurs sont dans un rapport de ${Math.round(b / a * 100)} %.`;
    };
    rg.oninput = draw; draw();
  },
  superpose(el) {
    const d = frame(el, 1060, '<label>Décalage horizontal <input type="range" min="0" max="0.32" step="0.02" value="0"></label><label>Opacité <input type="range" min="0.15" max="1" step="0.05" value="1"></label>');
    const [j, o] = $$('input', d), off = ROWS.map((r, i) => ((i * 9301 + 49297) % 233280) / 116640 - 1), vis = [7, 14, 30, 60, 90, 180];
    const draw = () => {
      const p = plot($('.wg-p', d), { w: 1060, h: 500, x: [-.5, 5.5], y: [0, 26], xt: vis.map((v, i) => ({ v: i, l: 'J' + v })), yt: [0, 5, 10, 15, 20, 25], xl: 'Visite', yl: 'C0 (ng/mL)', label: 'Tous les dosages, visite par visite' });
      band(p);
      ROWS.forEach((r, i) => S('circle', { cx: p.X(vis.indexOf(r.j) + off[i] * j.value), cy: p.Y(r.c), r: 8, fill: C1, opacity: o.value }, p.svg));
    };
    j.oninput = o.oninput = draw; draw();
  },
  fonction(el) {
    const d = H(`<div class="wg cg" style="width:calc(1060 * var(--u))"><div>
      <label>Âge <span><input id="cg-a" type="range" min="18" max="95" value="60"> <output></output> ans</span></label>
      <label>Poids <span><input id="cg-p" type="range" min="40" max="130" value="70"> <output></output> kg</span></label>
      <label>Créatininémie <span><input id="cg-c" type="range" min="40" max="400" step="5" value="90"> <output></output> µmol/L</span></label>
      <label>Sexe <span class="seg2"><button aria-pressed="true">Homme</button><button aria-pressed="false">Femme</button></span></label></div>
      <div class="cg-f"><p class="m">cockcroft_gault</p><p class="x"></p><p class="x">k = 1,23 (homme) ou 1,04 (femme)</p></div>
      <div class="cg-o"><p>Clairance estimée</p><p class="big"></p><p>mL/min</p></div></div>`);
    el.replaceWith(d);
    const rs = $$('input', d), os = $$('output', d), bs = $$('button', d);
    const draw = () => { const [a, p, c] = rs.map(r => +r.value), k = bs[0].getAttribute('aria-pressed') === 'true' ? 1.23 : 1.04; rs.forEach((r, i) => os[i].textContent = r.value); $$('.x', d)[0].textContent = `(140 − ${a}) × ${p} × ${fr(k, 2)} ÷ ${c}`; $('.big', d).textContent = fr((140 - a) * p * k / c); };
    rs.forEach(r => r.oninput = draw); bs.forEach(b => b.onclick = () => { bs.forEach(x => x.setAttribute('aria-pressed', x === b)); draw(); }); draw();
  },
  cible(el) {
    const d = frame(el, 560, '<label>c0 = <input type="range" min="0" max="15" step="0.1" value="12.4"><output></output></label>');
    d.appendChild(H('<p class="say"></p>'));
    const rg = $('input', d), out = $('output', d), say = $('.say', d), host = $('.wg-p', d);
    const svg = S('svg', { viewBox: '0 0 560 150', role: 'img', 'aria-label': 'Position de la concentration par rapport à la cible' }, host), u = 520 / 15;
    [[0, 5, '#FBE9D7', 'sous la cible'], [5, 10, '#DDEBE9', 'dans la cible'], [10, 15, '#F6E6E0', 'au-dessus']].forEach(([a, b, f, t]) => { S('rect', { x: 20 + a * u + 3, y: 40, width: (b - a) * u - 6, height: 64, rx: 10, fill: f }, svg); S('text', { x: 20 + (a + b) / 2 * u, y: 79, 'text-anchor': 'middle', 'font-size': 20, 'font-weight': 600 }, svg).textContent = t; });
    [0, 5, 10, 15].forEach(v => S('text', { x: 20 + v * u, y: 130, 'text-anchor': 'middle', 'font-size': 19 }, svg).textContent = v);
    const mk = S('g', {}, svg); S('line', { y1: 14, y2: 104, stroke: INK, 'stroke-width': 4 }, mk); S('circle', { cy: 14, r: 9, fill: INK }, mk);
    const draw = () => { const v = +rg.value; out.textContent = v.toFixed(1); mk.setAttribute('transform', `translate(${20 + v * u} 0)`); say.textContent = 'statut : « ' + (v < 5 ? 'sous la cible' : v <= 10 ? 'dans la cible' : 'au-dessus de la cible') + ' »'; };
    rg.oninput = draw; draw();
  },
  unite(el) {
    const d = frame(el, 560, '<label>Créatininémie <input type="range" min="50" max="300" step="5" value="90"><output></output> µmol/L</label>');
    const rg = $('input', d), out = $('output', d), host = $('.wg-p', d);
    const draw = () => { const c = +rg.value, ok = 80 * 70 * 1.23 / c, ko = 80 * 70 / (72 * c); out.textContent = c;
      host.innerHTML = `<div class="bars"><span>Formule prévue pour des µmol/L : <b>${fr(ok)} mL/min</b></span><div class="b" style="background:${C1};width:${Math.min(100, ok / 1.4)}%"></div><span>Code de l’assistant, prévu pour des mg/dL : <b>${fr(ko)} mL/min</b></span><div class="b" style="background:#9B2C1F;width:${Math.min(100, ko / 1.4)}%"></div></div>`; };
    rg.oninput = draw; draw();
  },
  filtre(el) {
    const vis = [7, 14, 30, 60, 90, 180];
    const d = frame(el, 560, `<label>jour <span class="seg2">${vis.map(v => `<button aria-pressed="${v === 30}">${v}</button>`).join('')}</span></label><label>C0 supérieure à <input type="range" min="0" max="20" step="1" value="10"><output></output></label>`);
    const bs = $$('button', d), rg = $('input', d), out = $('output', d), host = $('.wg-p', d);
    const draw = () => { const j = +bs.find(b => b.getAttribute('aria-pressed') === 'true').textContent, s = +rg.value, keep = ROWS.filter(r => r.j === j && r.c > s); out.textContent = s;
      host.innerHTML = `<p class="codeline">df[(df["jour"] == ${j}) & (df["c0_ng_ml"] > ${s})]</p><p class="say">${keep.length} lignes gardées sur ${ROWS.length}</p><table class="mini"><tr><th>patient_id</th><th>jour</th><th>c0_ng_ml</th></tr>${keep.slice(0, 3).map(r => `<tr><td>${r.p}</td><td>${r.j}</td><td>${r.c.toFixed(1)}</td></tr>`).join('')}</table>`; };
    bs.forEach(b => b.onclick = () => { bs.forEach(x => x.setAttribute('aria-pressed', x === b)); draw(); }); rg.oninput = draw; draw();
  },
};

/* ---------- diapositives ---------- */
function enhance() {
  $$('.pg', deck).forEach((p, i) => p.dataset.n = i + 1);
  $$('[data-fig]', deck).forEach(el => { const f = W[el.dataset.fig]; if (f) f(el); });
  $$('.dgs', deck).forEach(svg => [...svg.children].forEach((c, i) => c.style.setProperty('--i', Math.min(i, 30))));
  $$('.codebox', deck).forEach(box => { const out = box.nextElementSibling; if (!out || !out.classList.contains('outbox')) return; const b = H('<button class="run">Exécuter</button>'); b.onclick = () => { out.classList.add('shown'); b.classList.add('done'); }; box.appendChild(b); });
  $$('.cards[data-answer]', deck).forEach(g => $$('.card', g).forEach(card => {
    card.tabIndex = 0; card.setAttribute('role', 'button');
    const pick = () => { if (card.querySelector('.verdict')) return; const good = $('.num', card).textContent.trim() === g.dataset.answer; card.classList.add(good ? 'ok' : 'ko'); card.appendChild(H(`<p class="verdict">${good ? 'Bonne réponse' : 'Ce n’est pas la bonne réponse'}</p>`)); if (good) { g.parentElement.querySelector('.qz-x').hidden = false; if (mode === 'present') fitSlide(g.closest('section')); } };
    card.onclick = pick; card.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } };
  }));
}
function fitSlide(sec) {
  let k = 1;
  for (let t = 0; t < 9; t++) {
    sec.style.setProperty('--u', su * k + 'px');
    const lim = sec.getBoundingClientRect().bottom - 150 * su;
    if (!$$(':scope > :not(.foot):not(.pg):not(aside):not(.sp)', sec).some(c => c.getBoundingClientRect().bottom > lim)) break;
    k -= .04;
  }
}
function fit() {
  if (mode !== 'present' || !cur.n) return;
  const box = $('#scroll'); su = Math.max(.2, Math.min((box.clientWidth - 24) / 1920, (box.clientHeight - 24) / 1080));
  deck.style.setProperty('--su', su + 'px'); const s = secs()[cur.i]; if (s) fitSlide(s);
}
function go(i, scroll) {
  const all = secs(); cur.i = Math.max(0, Math.min(all.length - 1, i)); store.set('i' + cur.n, cur.i);
  all.forEach((s, k) => s.classList.toggle('on', k === cur.i));
  $('#count').textContent = `${cur.i + 1} / ${all.length}`; $('#prev').disabled = cur.i === 0; $('#next').disabled = cur.i === all.length - 1;
  const parts = DATA.seances[cur.n - 1].parts; let a = 0; parts.forEach((p, k) => { if (p[0] <= cur.i) a = k; }); $$('#parts button').forEach((b, k) => b.classList.toggle('on', k === a));
  const note = $('aside', all[cur.i]); $('#notes').innerHTML = '<b>Notes de l’enseignant.</b> ' + (note ? note.innerHTML : 'Pas de note pour cette diapositive.');
  if (mode === 'present') fit(); else if (scroll) all[cur.i].scrollIntoView({ block: 'start' });
}
function setMode(m) {
  mode = m; store.set('mode', m); deck.className = m;
  $('#m-read').setAttribute('aria-pressed', m === 'read'); $('#m-present').setAttribute('aria-pressed', m === 'present');
  $('#ctl').hidden = m !== 'present'; $('#notes').hidden = !(m === 'present' && $('#bnotes').getAttribute('aria-pressed') === 'true');
  if (m === 'read') secs().forEach(s => s.style.removeProperty('--u'));
  go(cur.i, true);
}
async function route() {
  const m = location.hash.match(/^#seance-([1-4])$/);
  $('#home').hidden = !!m; $('#player').hidden = !m; $('#modes').hidden = !m;
  if (!m) { $('#where').textContent = ''; cur.n = 0; document.documentElement.scrollTop = 0; return; }
  const n = +m[1], meta = DATA.seances[n - 1];
  $('#where').textContent = `Séance ${n} : ${meta.title}`;
  deck.innerHTML = await (await fetch(`seances/s${n}.html`)).text(); cur.n = n; cur.i = +(store.get('i' + n) || 0);
  $('#parts').innerHTML = ''; meta.parts.forEach(p => { const b = H(`<button>${p[1]}</button>`); b.onclick = () => go(p[0], true); $('#parts').appendChild(b); });
  enhance(); setMode(mode); $('#scroll').scrollTop = 0; if (mode === 'read' && cur.i) go(cur.i, true);
}
async function boot() {
  DATA = await (await fetch('data.json')).json(); ROWS = DATA.rows;
  $('#list').innerHTML = DATA.seances.map((s, i) => `<a class="row" href="#seance-${s.n}"><span class="n">${s.n}</span><span><h3>${s.title}</h3><p>${DESC[i]}</p></span><span class="go">Ouvrir la séance ${s.n}</span></a>`).join('');
  spag($('#hero-chart'), { animate: true, h: 540 });
  mode = store.get('mode') || (innerWidth < 900 ? 'read' : 'present');
  $('#m-read').onclick = () => setMode('read'); $('#m-present').onclick = () => setMode('present');
  $('#prev').onclick = () => go(cur.i - 1); $('#next').onclick = () => go(cur.i + 1);
  $('#bnotes').onclick = () => { const b = $('#bnotes'), on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', on); $('#notes').hidden = !on; fit(); };
  addEventListener('keydown', e => { if (!cur.n || mode !== 'present' || /INPUT|TEXTAREA/.test(e.target.tagName)) return; if (['ArrowRight', 'PageDown'].includes(e.key)) go(cur.i + 1); else if (['ArrowLeft', 'PageUp'].includes(e.key)) go(cur.i - 1); else if (e.key.toLowerCase() === 'n') $('#bnotes').click(); });
  addEventListener('resize', fit); addEventListener('hashchange', route);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  route();
}
boot();
