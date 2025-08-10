// Example: simulate ontology tags from integrity diagnostics
const exampleTags = [
  { type: 'topic', label: 'Technology' },
  { type: 'source', label: 'Multi-source' },
  { type: 'bias', label: 'Low Bias' }
];

function renderTags(tags) {
  const container = document.getElementById('tags');
  container.innerHTML = '';
  tags.forEach(tag => {
    const el = document.createElement('span');
    el.className = `tag ${tag.type}`;
    el.textContent = tag.label;
    container.appendChild(el);
  });
}

// Call after you have diagnostics/ontology
renderTags(exampleTags);