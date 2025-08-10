(function () {
  // -------- helpers
  const textOf = () => (document.body.innerText || '').replace(/\s+/g, ' ').trim();
  const nouns = (s) => (s.toLowerCase().match(/\b[a-z]{4,}\b/g) || []);
  const uniq = (arr) => [...new Set(arr)];

  // -------- raw signals
  const txt = textOf();
  const title = document.title || '';
  const links = Array.from(document.links || []);
  const hosts = uniq(links.map(a => {
    try { return new URL(a.href, location.href).host; } catch { return null; }
  }).filter(Boolean));

  const hasDates = /\b(20\d{2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b/i.test(txt);
  const hedges = (txt.match(/\b(might|could|may|reportedly|alleged|unconfirmed|sources say|appears|suggests)\b/gi) || []).length;
  const quotes = (txt.match(/[“"][^”"]+[”"]/g) || []).length;

  // title-body overlap as a drift anchor
  const titleTerms = uniq(nouns(title)).slice(0, 20);
  const bodyTerms = uniq(nouns(txt));
  const overlap = titleTerms.filter(w => bodyTerms.includes(w));
  const overlapScore = Math.min(1, overlap.length / 8);

  // source clarity
  const sourceClarity = Math.min(1, (hosts.length + Math.min(quotes, 5)) / 8);

  // recency hint
  const recencyHint = hasDates ? 0.2 : 0;

  const integrityScore = Math.round(100 * (0.55 * sourceClarity + 0.35 * overlapScore + 0.10 * recencyHint));

  // -------- lightweight ontology tagging
  const topics = [
    { key: 'ai', rx: /\b(ai|artificial intelligence|machine learning|model|neural|summarizer|openai|anthropic|google)\b/i, label: 'AI/ML' },
    { key: 'crypto', rx: /\b(crypto|bitcoin|ethereum|eth|btc|blockchain|defi|staking|l2)\b/i, label: 'Crypto' },
    { key: 'markets', rx: /\b(stocks?|equities|etf|yield|basis|funding|futures|oi|open interest|treasury|bond|dow|nasdaq|s&p)\b/i, label: 'Markets' },
    { key: 'metals', rx: /\b(silver|gold|bullion|comex|spot|miners?|slv|gld)\b/i, label: 'Metals' },
    { key: 'science', rx: /\b(physics|biology|biotech|vaccine|trial|peer-reviewed|preprint|study)\b/i, label: 'Science' },
    { key: 'politics', rx: /\b(president|congress|senate|election|policy|regulation|bill|court)\b/i, label: 'Politics' },
    { key: 'tech', rx: /\b(software|chrome|extension|api|github|kernel|browser|device)\b/i, label: 'Tech' },
    { key: 'space', rx: /\b(space|nasa|jwst|comet|asteroid|probe|interstellar)\b/i, label: 'Space' }
  ];
  const detectedTopics = topics.filter(t => t.rx.test(txt)).map(t => t.label);

  // bias/source tags
  const biasTag =
    hedges > 8 ? { type: 'bias', label: 'Heavy Hedging' } :
    hedges > 3 ? { type: 'bias', label: 'Some Hedging' } :
                 { type: 'bias', label: 'Low Hedging' };

  const sourceTag =
    hosts.length >= 5 ? { type: 'source', label: 'Multi-source' } :
    hosts.length >= 2 ? { type: 'source', label: 'Some Sources' } :
                        { type: 'source', label: 'Thin Sourcing' };

  // topic tags → 'topic' type chips (cap to 4)
  const topicTags = detectedTopics.slice(0, 4).map(label => ({ type: 'topic', label }));

  // neutral/meta tags
  const driftTag = overlapScore >= 0.75 ? { type: 'neutral', label: 'Strong Title Alignment' } :
                   overlapScore >= 0.40 ? { type: 'neutral', label: 'Moderate Alignment' } :
                                          { type: 'neutral', label: 'Possible Drift' };

  const tags = [sourceTag, biasTag, driftTag, ...topicTags];

  // expose result to popup poller
  window.__ISIG_RESULT = {
    integrityScore,
    diagnostics: {
      distinctHosts: hosts.length,
      hosts: hosts.slice(0, 10),
      quotes,
      hedges,
      titleOverlapTerms: overlap.slice(0, 12)
    },
    tags
  };
})();