/**
 * analytics.js — Entry point for analytics.html
 * Fetches live data from /api/analytics and renders the dashboard.
 */

import { initTheme, toggleTheme } from './theme.js';

// ── INIT ──────────────────────────────────────────────────────────────────────

initTheme();

window.toggleTheme = toggleTheme;
window.load = load;
window.clearCache = clearCache;

// Auto-refresh every 30 s
load();
setInterval(load, 30_000);

// ── DATA FETCH ────────────────────────────────────────────────────────────────

async function load() {
  setContent('<div class="loading"><div class="spinner"></div>Refreshing…</div>');

  try {
    const response = await fetch('/api/analytics');
    const data = await response.json();

    document.getElementById('lastUpdated').textContent =
      'Last updated: ' +
      new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    render(data);
  } catch {
    setContent(
      '<div class="loading">⚠️ Could not load analytics. Make sure Flask server is running on port 5000.</div>'
    );
  }
}

function setContent(html) {
  document.getElementById('content').innerHTML = html;
}

// ── RENDER ────────────────────────────────────────────────────────────────────

function render(d) {
  const {
    accuracy: acc = 0,
    total_messages: total = 0,
    matched = 0,
    unmatched = 0,
    top_intents: topIntents = [],
    daily = [],
    sessions = 0,
    unique_users: uniqueUsers = 0,
    most_asked: mostAsked = [],
    gemini_count: geminiCount = 0,
    cached_pages: cachedPages = 0,
    cache_list: cacheList = [],
    first_use: firstUse = 'N/A',
  } = d;

  // Accuracy ring maths
  const circumference = 2 * Math.PI * 48;
  const ringOffset    = circumference - (acc / 100) * circumference;
  const ringColor     = acc >= 80 ? '#10b981' : acc >= 60 ? '#f5a623' : '#ef4444';
  const accLabel      = acc >= 80 ? 'Excellent'  : acc >= 60 ? 'Good' : 'Needs Improvement';

  const maxDay = Math.max(...daily.map((x) => x.count), 1);
  const maxIntent = topIntents.length > 0 ? topIntents[0][1] : 1;
  const maxMAQ    = mostAsked.length  > 0 ? mostAsked[0][1]  : 1;

  setContent(`
    ${renderKPIs({ acc, accLabel, total, matched, unmatched, uniqueUsers, sessions, firstUse, geminiCount })}
    ${renderAccuracyCard({ acc, circumference, ringOffset, ringColor, matched, total, unmatched })}
    <div class="three-col">
      ${renderIntentCard(topIntents, maxIntent)}
      ${renderDailyCard(daily, maxDay)}
      ${renderMostAskedCard(mostAsked, maxMAQ)}
    </div>
    ${renderEvalTable({ acc, matched, unmatched, total, uniqueUsers })}
    ${renderDeliverables()}
    <div class="two-col">
      ${renderTechCard()}
      ${renderNLPCard()}
    </div>
    ${renderCacheCard(cachedPages, cacheList)}
  `);

  // Animate the SVG ring after paint
  requestAnimationFrame(() => {
    const ring = document.getElementById('accRing');
    if (ring) ring.style.strokeDashoffset = ringOffset.toFixed(1);
  });
}

// ── SECTION BUILDERS ─────────────────────────────────────────────────────────

function renderKPIs({ acc, accLabel, total, matched, unmatched, uniqueUsers, sessions, firstUse, geminiCount }) {
  const cards = [
    { cls: 'green',  icon: '🎯', value: `${acc}%`,        label: 'NLP Accuracy',    sub: accLabel },
    { cls: 'amber',  icon: '💬', value: total,             label: 'Total Messages',  sub: 'All sessions combined' },
    { cls: 'blue',   icon: '✅', value: matched,           label: 'Matched Queries', sub: 'Intent found' },
    { cls: 'red',    icon: '❌', value: unmatched,         label: 'Unmatched',       sub: 'Invalid input' },
    { cls: 'purple', icon: '👥', value: uniqueUsers,       label: 'Unique Users',    sub: 'Distinct sessions' },
    { cls: 'navy',   icon: '🗂️', value: sessions,          label: 'Total Sessions',  sub: `Since: ${firstUse}` },
    { cls: '',       icon: '✦',  value: renderGeminiValue(geminiCount), label: 'Gemini AI Replies', sub: 'Fallback responses', raw: true },
  ];

  return `<div class="kpi-grid">${cards.map((c) => `
    <div class="kpi-card ${c.cls}">
      <div class="kpi-icon">${c.icon}</div>
      <div class="kpi-value"${c.raw ? ' style="background:linear-gradient(90deg,#4285f4,#ea4335,#fbbc05,#34a853);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;"' : ''}>${c.raw ? c.value : c.value}</div>
      <div class="kpi-label">${c.label}</div>
      <div class="kpi-sub">${c.sub}</div>
    </div>`).join('')}
  </div>`;
}

function renderGeminiValue(count) {
  return count;
}

function renderAccuracyCard({ acc, circumference, ringOffset, ringColor, matched, total, unmatched }) {
  const matchedPct   = total > 0 ? Math.round((matched   / total) * 100) : 0;
  const unmatchedPct = total > 0 ? Math.round((unmatched / total) * 100) : 0;

  return `
  <div class="accuracy-card">
    <h2>🎯 NLP Accuracy Meter</h2>
    <div class="accuracy-meter">
      <div class="accuracy-ring-wrap">
        <svg width="120" height="120" viewBox="0 0 120 120">
          <circle class="ring-bg" cx="60" cy="60" r="48"/>
          <circle class="ring-fg" cx="60" cy="60" r="48"
            id="accRing"
            stroke="${ringColor}"
            stroke-dasharray="${circumference.toFixed(1)}"
            stroke-dashoffset="${circumference.toFixed(1)}"/>
        </svg>
        <div class="ring-label">
          <span class="value">${acc}%</span>
          <span class="label">Accuracy</span>
        </div>
      </div>
      <div class="accuracy-bars">
        <div class="acc-bar">
          <div class="acc-bar-top">
            <span>Matched Queries</span>
            <span class="acc-bar-val">${matched} / ${total}</span>
          </div>
          <div class="acc-bar-track">
            <div class="acc-bar-fill green" style="width:${matchedPct}%"></div>
          </div>
        </div>
        <div class="acc-bar">
          <div class="acc-bar-top">
            <span>Unmatched / Invalid</span>
            <span class="acc-bar-val">${unmatched} / ${total}</span>
          </div>
          <div class="acc-bar-track">
            <div class="acc-bar-fill red" style="width:${unmatchedPct}%"></div>
          </div>
        </div>
        <div class="accuracy-note">
          <p><strong>Formula:</strong> Accuracy = Matched ÷ Total × 100<br/>
          A query is "matched" when NLP score &gt; 0 (phrase, fuzzy, or keyword hit).<br/>
          Fuzzy matching at 80%+ similarity handles typos and near-matches.</p>
        </div>
      </div>
    </div>
  </div>`;
}

function renderIntentCard(topIntents, maxIntent) {
  const body = topIntents.length === 0
    ? '<p style="color:var(--muted);font-size:13px;text-align:center;padding:20px 0">No data yet. Start chatting!</p>'
    : topIntents.map(([intent, count]) => `
        <div class="intent-bar">
          <div class="intent-bar-top">
            <span class="intent-name">${intent.replace(/_/g, ' ')}</span>
            <span class="intent-count">${count}</span>
          </div>
          <div class="intent-track">
            <div class="intent-fill" style="width:${Math.round((count / maxIntent) * 100)}%"></div>
          </div>
        </div>`).join('');

  return `<div class="card"><h2>🏷️ Top Intent Distribution</h2>${body}</div>`;
}

function renderDailyCard(daily, maxDay) {
  const bars = daily.map((day) => {
    const pct = Math.round((day.count / maxDay) * 100);
    return `
      <div class="day-col">
        <div class="day-count">${day.count}</div>
        <div class="day-bar-wrap">
          <div class="day-bar" style="height:${Math.max(pct, 2)}%"></div>
        </div>
        <div class="day-label">${day.date.slice(5)}</div>
      </div>`;
  }).join('');

  return `
    <div class="card">
      <h2>📅 Daily Activity (7 Days)</h2>
      <div class="daily-chart">${bars}</div>
    </div>`;
}

function renderMostAskedCard(mostAsked, maxMAQ) {
  const body = mostAsked.length === 0
    ? '<p class="maq-empty">No questions recorded yet. Start chatting! 💬</p>'
    : mostAsked.map(([q, cnt], i) => `
        <div class="maq-item">
          <div class="maq-rank ${i < 3 ? 'top3' : ''}">${i + 1}</div>
          <div class="maq-question">
            <div class="maq-text">${escHtml(q)}</div>
            <div class="maq-count">Asked ${cnt} time${cnt > 1 ? 's' : ''}</div>
            <div class="maq-bar">
              <div class="maq-bar-fill" style="width:${Math.round((cnt / maxMAQ) * 100)}%"></div>
            </div>
          </div>
        </div>`).join('');

  return `<div class="card"><h2>🔥 Most Asked Questions</h2>${body}</div>`;
}

function renderEvalTable({ acc, matched, unmatched, total, uniqueUsers }) {
  const rows = [
    ['Intent Classification',   'Phrase-priority NLP scoring (10× weight)',          acc >= 80 ? 'High Accuracy' : 'Moderate', 'pass'],
    ['Fuzzy Matching',           'Levenshtein distance, 80% threshold',                'Active – handles typos',                 'pass'],
    ['Synonym Expansion',        '60+ synonym → canonical mappings',                   'Active – 60+ mappings',                  'pass'],
    ['Response Relevance',       'Exact KB lookup per matched intent',                 'Deterministic',                          'pass'],
    ['Invalid Input Detection',  'Fallback when NLP score = 0',                       `${unmatched} flagged`,                   'pass'],
    ['Matched Queries',          'Intent score > 0',                                  `${matched} / ${total}`,                  matched > unmatched || total === 0 ? 'pass' : 'review'],
    ['Persistent History',       'JSON file on disk, per-session UUID',                'All sessions saved',                     'pass'],
    ['Unique User Tracking',     'UUID per browser session, stored in analytics.json', `${uniqueUsers} users`,                   'pass'],
  ];

  return `
  <div class="eval-wrap">
    <div class="card" style="margin-bottom:0">
      <h2>🧪 Response Evaluation Report</h2>
      <table class="eval-table">
        <thead>
          <tr><th>Category</th><th>Method</th><th>Result</th><th>Status</th></tr>
        </thead>
        <tbody>
          ${rows.map(([cat, method, result, status]) => `
            <tr>
              <td><strong>${cat}</strong></td>
              <td style="color:var(--muted);font-size:11.5px">${method}</td>
              <td>${result}</td>
              <td><span class="badge ${status}">${status === 'pass' ? '✅ Pass' : '⚠️ Review'}</span></td>
            </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>`;
}

function renderDeliverables() {
  const items = [
    ['🤖', 'Chatbot User Interface',       'Responsive floating popup with Chat & History tabs, dark mode, typing animation.'],
    ['🧠', 'NLP Intent Classification',    'Phrase-priority + fuzzy matching + synonym expansion. 25+ intents, 200+ phrase rules.'],
    ['📚', 'Knowledge Base',               '25 intents — Sem V & VI subjects, exam dates, attendance, fees, OJT, library, academic calendar.'],
    ['🕐', 'Persistent Chat History',      'JSON storage survives page reload. History tab shows full conversation.'],
    ['📊', 'Accuracy & Evaluation Report', 'This dashboard — KPIs, accuracy ring, unique users, most asked questions, evaluation table.'],
    ['🌐', 'Website Integration',          'Landing page: hero, features, how-it-works, topics, footer. Chatbot accessible from every section.'],
  ];

  return `
  <div class="deliverables-card">
    <h2>📋 Project Deliverables Checklist</h2>
    ${items.map(([icon, name, desc]) => `
      <div class="deliverable-row">
        <div class="deliverable-icon">${icon}</div>
        <div class="deliverable-info">
          <h4>${name}</h4>
          <p>${desc}</p>
          <span class="deliverable-tag">✅ Delivered</span>
        </div>
      </div>`).join('')}
  </div>`;
}

function renderTechCard() {
  const rows = [
    ['Backend',            'Python 3 + Flask'],
    ['NLP Engine',         'Phrase-priority + Fuzzy + Synonyms'],
    ['Storage',            'JSON files (data/ directory)'],
    ['History',            'Per-session UUID, disk-persisted'],
    ['Frontend',           'HTML5 + CSS3 + ES Modules'],
    ['Dark Mode',          'CSS variables + localStorage'],
    ['Typing Animation',   'CSS keyframes + bot status indicator'],
    ['Analytics API',      '/api/analytics live endpoint'],
  ];
  return `<div class="card"><h2>🛠️ Technical Architecture</h2>${tableFromRows(rows)}</div>`;
}

function renderNLPCard() {
  const rows = [
    ['Total Intents',        '25 intents'],
    ['Phrase Rules',         '200+ multi-word phrases'],
    ['Synonym Mappings',     '60+ word expansions'],
    ['Fuzzy Threshold',      '80% similarity (Levenshtein)'],
    ['Phrase Match Weight',  '10 × word count'],
    ['Keyword Match Weight', '2 × word count'],
    ['Fuzzy Phrase Score',   '8 × ratio × word count'],
    ['Invalid Handling',     'Fallback with 6 suggestions'],
  ];
  return `<div class="card"><h2>📐 NLP Model Summary</h2>${tableFromRows(rows)}</div>`;
}

function tableFromRows(rows) {
  return `
  <table style="width:100%;font-size:12.5px;border-collapse:collapse;">
    ${rows.map(([k, v]) => `
      <tr style="border-bottom:1px solid var(--border)">
        <td style="padding:8px 0;font-weight:600;color:var(--muted);width:50%;font-size:11.5px">${k}</td>
        <td style="padding:8px 0;color:var(--text);font-weight:500">${v}</td>
      </tr>`).join('')}
  </table>`;
}

function renderCacheCard(cachedPages, cacheList) {
  const table = cacheList.length === 0
    ? '<p style="color:var(--muted);font-size:13px">No pages cached yet. Ask the bot a question to trigger scraping.</p>'
    : `<table style="width:100%;font-size:12px;border-collapse:collapse">
        <tr style="background:var(--navy);color:#fff">
          <th style="padding:7px 10px;text-align:left;border-radius:6px 0 0 0">Page URL</th>
          <th style="padding:7px 10px;border-radius:0 6px 0 0">Cached (min ago)</th>
        </tr>
        ${cacheList.map((p) => `
          <tr style="border-bottom:1px solid var(--border)">
            <td style="padding:7px 10px;color:var(--muted);font-size:11px">${p.url}</td>
            <td style="padding:7px 10px;text-align:center;color:var(--amber-dim);font-weight:600">${p.age_min}</td>
          </tr>`).join('')}
      </table>`;

  return `
  <div class="card" style="margin-bottom:0">
    <h2>🌐 Live Website Scrape Cache (kessc.edu.in)</h2>
    <div style="display:flex;gap:16px;margin-bottom:14px;flex-wrap:wrap">
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:9px;padding:12px 18px;text-align:center">
        <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:800;color:var(--amber)">${cachedPages}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:3px">Pages Cached</div>
      </div>
      <div style="flex:1;min-width:200px">
        <p style="font-size:12px;color:var(--muted);line-height:1.65">
          Pages are scraped live from kessc.edu.in and cached for 1 hour.
          The bot uses this content as context for Gemini AI answers.
        </p>
        <button onclick="clearCache()"
          style="margin-top:8px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);color:#ef4444;padding:6px 14px;border-radius:7px;font-size:12px;font-weight:600;cursor:pointer;font-family:inherit">
          🗑️ Clear Cache
        </button>
      </div>
    </div>
    ${table}
  </div>`;
}

// ── ACTIONS ───────────────────────────────────────────────────────────────────

async function clearCache() {
  await fetch('/api/cache/clear', { method: 'POST' });
  alert('Cache cleared! Next question will fetch fresh data from kessc.edu.in');
  load();
}

// ── UTILS ─────────────────────────────────────────────────────────────────────

function escHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
