/**
 * chat.js — Chat panel logic (open/close, send, history, export, TTS, copy)
 * Uses ES module syntax; import in index.html as type="module".
 */

// ── STATE ────────────────────────────────────────────────────────────────────

let isPanelOpen = false;
let activeTTSBtn = null;
let ttsKeepAliveTimer = null;
let toastTimer = null;


// ── HELPERS ───────────────────────────────────────────────────────────────────

/** Escape HTML entities and convert newlines to <br>. */
function renderText(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>');
}

/** Return HH:MM formatted current time. */
function timestamp() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/** Show a brief toast notification. */
function showToast(message) {
  const toast = document.getElementById('feedbackToast');
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
}

/** Copy text to clipboard with a fallback for non-secure contexts. */
function copyToClipboard(text, btn) {
  const onSuccess = () => {
    btn.textContent = '✅';
    btn.classList.add('copied');
    showToast('Copied to clipboard!');
    setTimeout(() => {
      btn.textContent = '📋';
      btn.classList.remove('copied');
    }, 2000);
  };

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(onSuccess).catch(() => fallbackCopy(text, onSuccess));
  } else {
    fallbackCopy(text, onSuccess);
  }
}

function fallbackCopy(text, callback) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0;';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {
    document.execCommand('copy');
    callback();
  } catch {
    showToast('Copy failed — try manually');
  }
  document.body.removeChild(ta);
}

// ── TTS HELPERS ───────────────────────────────────────────────────────────────

/** Chrome pauses SpeechSynthesis after ~15 s — resume it periodically. */
function startTTSKeepAlive() {
  ttsKeepAliveTimer = setInterval(() => {
    if (window.speechSynthesis.speaking) window.speechSynthesis.resume();
  }, 10_000);
}

function stopTTSKeepAlive() {
  clearInterval(ttsKeepAliveTimer);
  ttsKeepAliveTimer = null;
}

// ── TYPING INDICATOR ──────────────────────────────────────────────────────────

function showTyping() {
  document.getElementById('tyWrap').classList.add('show');
  const status = document.getElementById('botStatus');
  status.textContent = 'Typing…';
  status.style.color = 'rgba(245,166,35,.8)';
}

function hideTyping() {
  document.getElementById('tyWrap').classList.remove('show');
  const status = document.getElementById('botStatus');
  status.textContent = 'Online · All Courses · kessc.edu.in';
  status.style.color = '';
}

// ── DOM BUILDERS ──────────────────────────────────────────────────────────────

/**
 * Build and append a message row to the messages container.
 * @param {'user'|'bot'} role
 * @param {string} text
 * @param {string|null} intent
 * @param {string|null} source  'gemini' | 'predefined' | null
 */
function addMessage(role, text, intent, source) {
  const container = document.getElementById('msgs');

  const row = document.createElement('div');
  row.className = `msg-row${role === 'user' ? ' user-row' : ''}`;

  // Avatar
  const avatar = document.createElement('div');
  avatar.className = `msg-avatar ${role === 'user' ? 'user' : 'bot'}`;
  avatar.textContent = role === 'user' ? '🧑‍🎓' : '🤖';

  // Column wrapper
  const col = document.createElement('div');
  col.className = `msg-col${role === 'user' ? ' user-row' : ' bot-col'}`;

  // Bubble
  const bubble = document.createElement('div');
  bubble.className = `bubble ${role === 'user' ? 'user' : 'bot'}${intent === 'invalid' ? ' error' : ''}`;
  bubble.innerHTML = renderText(text);

  // Meta line
  const meta = document.createElement('div');
  meta.className = 'msg-meta';

  const timeEl = document.createElement('span');
  timeEl.className = 'msg-time';
  timeEl.textContent = timestamp();
  meta.appendChild(timeEl);

  if (role === 'bot') {
    // Source tag
    if (source === 'gemini') {
      const tag = document.createElement('span');
      tag.className = 'gemini-tag';
      tag.textContent = '✦ Gemini AI';
      meta.appendChild(tag);
    } else if (intent && intent !== 'unknown' && intent !== 'invalid') {
      const tag = document.createElement('span');
      tag.className = 'intent-tag';
      tag.textContent = '#' + intent.replace(/_/g, ' ');
      meta.appendChild(tag);
    }

    // Action buttons
    const actions = buildActionButtons(text);
    col.appendChild(bubble);
    col.appendChild(meta);
    col.appendChild(actions);

  } else {
    col.appendChild(bubble);
    col.appendChild(meta);
  }

  row.appendChild(avatar);
  row.appendChild(col);
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
}

/** Build copy / TTS / feedback action buttons for a bot message. */
function buildActionButtons(text) {
  const actions = document.createElement('div');
  actions.className = 'msg-actions';

  // Copy
  const copyBtn = document.createElement('button');
  copyBtn.className = 'action-btn';
  copyBtn.title = 'Copy response';
  copyBtn.textContent = '📋';
  copyBtn.addEventListener('click', () => copyToClipboard(text, copyBtn));

  // TTS
  const ttsBtn = document.createElement('button');
  ttsBtn.className = 'action-btn';
  ttsBtn.title = 'Read aloud';
  ttsBtn.textContent = '🔊';
  ttsBtn.addEventListener('click', () => handleTTS(text, ttsBtn));

  // Separator
  const sep = document.createElement('div');
  sep.className = 'action-sep';

  // Thumbs up
  const upBtn = document.createElement('button');
  upBtn.className = 'action-btn thumb-up';
  upBtn.title = 'Helpful';
  upBtn.textContent = '👍';

  // Thumbs down
  const downBtn = document.createElement('button');
  downBtn.className = 'action-btn thumb-down';
  downBtn.title = 'Not helpful';
  downBtn.textContent = '👎';

  upBtn.addEventListener('click', () => {
    if (upBtn.classList.contains('active')) return;
    upBtn.classList.add('active');
    downBtn.classList.remove('active');
    showToast('Thanks for the feedback! 🎉');
  });

  downBtn.addEventListener('click', () => {
    if (downBtn.classList.contains('active')) return;
    downBtn.classList.add('active');
    upBtn.classList.remove('active');
    showToast("Got it — we'll improve! 🛠️");
  });

  actions.append(copyBtn, ttsBtn, sep, upBtn, downBtn);
  return actions;
}


/** Handle TTS play/stop for a message button. */
function handleTTS(text, btn) {
  if (btn.classList.contains('tts-playing')) {
    // Stop current
    window.speechSynthesis.cancel();
    stopTTSKeepAlive();
    btn.textContent = '🔊';
    btn.classList.remove('tts-playing');
    activeTTSBtn = null;
    return;
  }

  // Stop any other playing button
  if (activeTTSBtn) {
    window.speechSynthesis.cancel();
    stopTTSKeepAlive();
    activeTTSBtn.textContent = '🔊';
    activeTTSBtn.classList.remove('tts-playing');
  }

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.95;
  utterance.pitch = 1;

  const cleanup = () => {
    stopTTSKeepAlive();
    btn.textContent = '🔊';
    btn.classList.remove('tts-playing');
    activeTTSBtn = null;
  };

  utterance.onstart = () => startTTSKeepAlive();
  utterance.onend = cleanup;
  utterance.onerror = cleanup;

  btn.textContent = '⏹️';
  btn.classList.add('tts-playing');
  activeTTSBtn = btn;

  window.speechSynthesis.cancel(); // clear queue
  window.speechSynthesis.speak(utterance);
}

// ── PANEL OPEN / CLOSE ────────────────────────────────────────────────────────

export function openChat() {
  isPanelOpen = true;
  document.getElementById('chatPanel').classList.add('on');
  document.getElementById('overlay').classList.add('on');
  document.getElementById('chatFab').classList.add('open');
  document.getElementById('fabIcon').textContent = '✕';
  setTimeout(() => document.getElementById('chatInput').focus(), 320);
}

export function closeChat() {
  isPanelOpen = false;
  document.getElementById('chatPanel').classList.remove('on');
  document.getElementById('overlay').classList.remove('on');
  document.getElementById('chatFab').classList.remove('open');
  document.getElementById('fabIcon').textContent = '🤖';
}

export function toggleChat() {
  isPanelOpen ? closeChat() : openChat();
}

// ── TABS ──────────────────────────────────────────────────────────────────────

export function switchTab(tab) {
  document.getElementById('tabChat').classList.toggle('active', tab === 'chat');
  document.getElementById('tabHist').classList.toggle('active', tab === 'hist');
  document.getElementById('paneChat').classList.toggle('show', tab === 'chat');
  document.getElementById('paneHist').classList.toggle('show', tab === 'hist');

  if (tab === 'hist') loadHistory();
}

// ── SEND / RECEIVE ────────────────────────────────────────────────────────────

/** Send message from the text input. */
export async function sendMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (!message) return;
  input.value = '';
  await sendQuery(message);
}

/**
 * Send a query string programmatically (also used by chips / follow-ups).
 * @param {string} text
 */
export async function sendQuery(text) {
  addMessage('user', text, null, null);
  showTyping();
  document.getElementById('msgs').scrollTop = 999_999;

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    const data = await response.json();
    hideTyping();
    addMessage('bot', data.reply, data.intent, data.source);
  } catch {
    hideTyping();
    addMessage('bot', 'Connection error. Ensure Flask runs on port 5000.', 'error', 'predefined');
  }
}

/**
 * Open the chat (if closed) then send a query after the open animation.
 * @param {string} text
 */
export function askTopic(text) {
  if (!isPanelOpen) {
    openChat();
    setTimeout(() => sendQuery(text), 380);
  } else {
    sendQuery(text);
  }
}

// ── HISTORY ───────────────────────────────────────────────────────────────────

async function loadHistory() {
  const list = document.getElementById('histList');
  try {
    const response = await fetch('/history');
    const data = await response.json();

    if (!data.history?.length) {
      list.innerHTML = '<div class="hist-empty">No chat history yet.<br/>Start a conversation! 💬</div>';
      return;
    }

    list.innerHTML = '';
    data.history.forEach((entry) => {
      const div = document.createElement('div');
      div.className = `hist-msg ${entry.role === 'user' ? 'user-hist' : 'bot-hist'}`;

      const sourceBadge =
        entry.source === 'gemini'
          ? '<span style="font-size:9px;font-weight:700;color:#4285f4;margin-left:4px;">✦ Gemini</span>'
          : '';

      div.innerHTML =
        `<div class="hist-role">${entry.role === 'user' ? 'You' : 'AcadBot'}${sourceBadge}</div>` +
        `<div class="hist-text">${renderText(entry.message)}</div>` +
        `<div class="hist-time">${entry.time ?? ''}</div>`;

      list.appendChild(div);
    });

    list.scrollTop = list.scrollHeight;
  } catch {
    list.innerHTML = '<div class="hist-empty">Could not load history.</div>';
  }
}

// ── CHAT CONTROLS ─────────────────────────────────────────────────────────────

export async function clearChat() {
  await fetch('/clear', { method: 'POST' });
  document.getElementById('msgs').innerHTML =
    '<div class="welcome-bubble" style="animation:fade-up .4s ease both">🗑️ Chat cleared! Ask me anything.</div>';
}

export async function exportChat() {
  const response = await fetch('/history');
  const data = await response.json();
  const text = data.history
    .map((e) => `[${e.time}] ${e.role.toUpperCase()}: ${e.message}`)
    .join('\n');

  const blob = new Blob([text], { type: 'text/plain' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'acadbot_chat.txt';
  link.click();
}

// ── INITIALISE ────────────────────────────────────────────────────────────────

export function initChat() {
  // Keyboard shortcuts
  document.getElementById('chatInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isPanelOpen) closeChat();
  });

  // Navbar scroll shadow
  window.addEventListener('scroll', () => {
    document.getElementById('nav').classList.toggle('scrolled', window.scrollY > 20);
  });

  // Scroll-reveal
  const observer = new IntersectionObserver(
    (entries) => entries.forEach((e) => { if (e.isIntersecting) e.target.classList.add('visible'); }),
    { threshold: 0.1 }
  );
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
}



