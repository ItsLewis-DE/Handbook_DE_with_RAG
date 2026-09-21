const concepts = [
  {name: 'Pipeline Core', file: 'pipeline-core', meaning: 'Nguồn dữ liệu. Luồng hội tụ. Kho lưu trữ.', alt: 'Hai nguồn dữ liệu hội tụ vào database'},
  {name: 'Flow Stack', file: 'flow-stack', meaning: 'Luồng dữ liệu. Các lớp lưu trữ. Kiến trúc nền tảng.', alt: 'Luồng dữ liệu đi vào các lớp lưu trữ'},
  {name: 'DAG Frame', file: 'dag-frame', meaning: 'Phân nhánh. Điều phối. Hội tụ.', alt: 'Pipeline phân nhánh qua các tác vụ rồi hội tụ'}
];
let selectedConcept = 0;
let selectedTheme = 'dark';

function updatePreview() {
  const concept = concepts[selectedConcept];
  const number = String(selectedConcept + 1).padStart(2, '0');
  const image = document.getElementById('hero-mark');
  image.src = `${concept.file}${selectedTheme === 'dark' ? '-inverse' : ''}.svg`;
  image.alt = `${concept.name}: ${concept.alt}`;
  const selection = document.getElementById('selection');
  selection.textContent = `${number} / ${concept.name}`;
  if (selectedConcept === 0) {
    const note = document.createElement('span');
    note.textContent = ' — Đề xuất chính';
    selection.appendChild(note);
  }
  document.getElementById('hero-meaning').textContent = concept.meaning;
  document.querySelector('.identity-bottom span:last-child').textContent = `${number} — ${concept.name.toUpperCase()}`;
  document.getElementById('identity').classList.toggle('light', selectedTheme === 'light');
  document.querySelectorAll('[data-concept]').forEach(button => {
    const selected = Number(button.dataset.concept) === selectedConcept;
    button.setAttribute('aria-pressed', String(selected));
    button.classList.toggle('selected', selected);
  });
  document.querySelectorAll('[data-theme]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.theme === selectedTheme)));
}

document.querySelectorAll('[data-concept]').forEach(button => button.addEventListener('click', () => {
  selectedConcept = Number(button.dataset.concept);
  updatePreview();
}));
document.querySelectorAll('[data-theme]').forEach(button => button.addEventListener('click', () => {
  selectedTheme = button.dataset.theme;
  updatePreview();
}));
