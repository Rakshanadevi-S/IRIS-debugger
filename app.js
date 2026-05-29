// app.js
// UI controller — wires events, calls LLMClient, and renders results

// ─── Panel config ───────────────────────────────────────────────────────────
const PANELS = [
  {
    key:       'meaning',
    label:     'Meaning',
    className: 'panel-meaning',
    render:    (val) => `<p class="panel-content">${esc(val)}</p>`
  },
  {
    key:       'causes',
    label:     'Possible causes',
    className: 'panel-causes',
    render:    (val) => {
      const items = Array.isArray(val) ? val : [val];
      return `<ul class="causes-list">${items.map(c => `<li>${esc(c)}</li>`).join('')}</ul>`;
    }
  },
  {
    key:       'fix',
    label:     'Recommended fix',
    className: 'panel-fix',
    render:    (val) => `<p class="panel-content">${esc(val)}</p>`
  },
  {
    key:       'example',
    label:     'Code example',
    className: 'panel-example',
    render:    (val) => `<pre class="code-block">${esc(val)}</pre>`
  }
];

// ─── Helpers ────────────────────────────────────────────────────────────────
function esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function $(id) { return document.getElementById(id); }

// ─── Skeleton loader ────────────────────────────────────────────────────────
function renderSkeleton() {
  return PANELS.map(p => `
    <div class="panel ${p.className}">
      <div class="panel-header">
        <div class="panel-dot"></div>
        <span class="panel-label">${p.label}</span>
      </div>
      <div class="skeleton" style="height:13px;width:90%;margin-bottom:7px;"></div>
      <div class="skeleton" style="height:13px;width:76%;margin-bottom:7px;"></div>
      <div class="skeleton" style="height:13px;width:83%;"></div>
    </div>
  `).join('');
}

// ─── Results renderer ───────────────────────────────────────────────────────
function renderPanels(data, ms) {
  $('panels').innerHTML = PANELS.map(p =>
    `<div class="panel ${p.className}">
      <div class="panel-header">
        <div class="panel-dot"></div>
        <span class="panel-label">${p.label}</span>
      </div>
      ${p.render(data[p.key] ?? '')}
    </div>`
  ).join('');

  $('responseTime').textContent = `${ms}ms`;
}

// ─── Main analyze flow ──────────────────────────────────────────────────────
async function analyze() {
  const input = $('errorInput').value.trim();
  if (!input) {
    $('errorInput').focus();
    return;
  }

  const btn    = $('analyzeBtn');
  const outSec = $('outputSection');
  const errBan = $('errorBanner');

  // Reset
  errBan.style.display = 'none';
  outSec.style.display = 'block';
  $('panels').innerHTML = renderSkeleton();
  $('responseTime').textContent = '';

  btn.disabled = true;
  btn.innerHTML = '<div class="spinner"></div><span class="btn-text">Analyzing…</span>';

  const t0 = Date.now();

  try {
    const result = await LLMClient.getResponse(input);
    const ms     = Date.now() - t0;
    renderPanels(result, ms);
  } catch (err) {
    outSec.style.display = 'none';
    errBan.textContent   = `⚠ Error: ${err.message}`;
    errBan.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span class="btn-text">Analyze error</span><span class="btn-icon">→</span>';
  }
}

// ─── Example chips ──────────────────────────────────────────────────────────
document.querySelectorAll('.ex-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const key = chip.dataset.key;
    if (EXAMPLES[key]) {
      $('errorInput').value = EXAMPLES[key];
      $('errorInput').focus();
    }
  });
});

// ─── Button ─────────────────────────────────────────────────────────────────
$('analyzeBtn').addEventListener('click', analyze);

// Ctrl/Cmd + Enter to submit
$('errorInput').addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') analyze();
});
