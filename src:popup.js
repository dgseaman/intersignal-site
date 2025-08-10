// src/popup.js

const btn = document.getElementById('run');
const statusEl = document.getElementById('status');
const summaryEl = document.getElementById('summary');
const integrityEl = document.getElementById('integrity');
const scoreValEl = document.getElementById('score-val');
const tagsContainer = document.getElementById('tags');

function setStatus(msg = '') {
  statusEl.textContent = msg;
}

function renderTags(tags) {
  tagsContainer.innerHTML = '';
  (tags || []).forEach(tag => {
    const el = document.createElement('span');
    el.className = `tag ${tag.type}`;
    el.textContent = tag.label;
    tagsContainer.appendChild(el);
  });
}

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab) throw new Error('No active tab found.');
  return tab;
}

async function collectPageText(tabId) {
  const [{ result }] = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let out = '';
      while (walker.nextNode()) {
        const t = walker.currentNode.nodeValue;
        if (t && t.trim().length > 0) out += ' ' + t;
      }
      return out.replace(/\s+/g, ' ').trim().slice(0, 120000);
    }
  });
  return result || '';
}

async function summarizeLocal(text) {
  const Summarizer = self?.ai?.summarizer;
  if (!Summarizer) {
    throw new Error('Summarizer API unavailable on this Chrome build.');
  }
  const summarizer = await Summarizer.create({
    type: 'key-points',
    format: 'markdown',
    length: 'medium'
  });
  const out = await summarizer.summarize(text);
  return out?.summary || '(no summary)';
}

async function injectIntegrity(tabId) {
  await chrome.scripting.executeScript({
    target: { tabId },
    files: ['src/integrity.js']
  });
}

async function pollIntegrity(tabId, attempts = 50, intervalMs = 120) {
  let tries = 0;
  return new Promise((resolve) => {
    const iv = setInterval(async () => {
      tries++;
      const [{ result }] = await chrome.scripting.executeScript({
        target: { tabId },
        func: () => window.__ISIG_RESULT || null
      });
      if (result || tries > attempts) {
        clearInterval(iv);
        resolve(result || null);
      }
    }, intervalMs);
  });
}

async function exec() {
  try {
    setStatus('Collecting page text…');
    const tab = await getActiveTab();
    const text = await collectPageText(tab.id);

    setStatus('Summarizing on-device…');
    try {
      const summary = await summarizeLocal(text);
      summaryEl.textContent = summary;
    } catch (e) {
      summaryEl.textContent = 'Summarization failed: ' + e.message;
    }

    setStatus('Scoring integrity…');
    await injectIntegrity(tab.id);
    const res = await pollIntegrity(tab.id);

    if (res && typeof res.integrityScore === 'number') {
      integrityEl.textContent = JSON.stringify(res.diagnostics, null, 2);
      scoreValEl.textContent = String(res.integrityScore);
      renderTags(res.tags);
      setStatus('Done.');
    } else {
      integrityEl.textContent = 'No integrity result.';
      setStatus('');
    }
  } catch (err) {
    setStatus('');
    summaryEl.textContent = '';
    integrityEl.textContent = '';
    scoreValEl.textContent = '--';
    tagsContainer.innerHTML = '';
    console.error(err);
    alert('Intersignal error: ' + err.message);
  }
}

btn.addEventListener('click', exec);