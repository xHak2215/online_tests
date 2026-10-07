import {API_URL} from '/front/libs/conf.js';
import {showToast} from '/front/libs/unit.js';

const questionsContainer = document.getElementById('questionsContainer');
const template = document.getElementById('questionTemplate');
const toast = document.getElementById('toast');

function addQuestion() {
  const clone = template.content.cloneNode(true);
  const card = clone.querySelector('.question-card');
  const imageInput = clone.querySelector('.image-input');
  const preview = clone.querySelector('.image-preview');
  const previewWrap = clone.querySelector('.image-preview-wrap');
  const removeBtn = clone.querySelector('.remove-btn');

  imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      previewWrap.style.display = 'block';
    };
    reader.readAsDataURL(file);
  });

  removeBtn.addEventListener('click', () => {
    card.remove();
    showToast('Вопрос удалён', 'success');
  });

  questionsContainer.appendChild(clone);
}

function saveTest() {
  const title = document.getElementById('testTitle').value.trim();
  const desc = document.getElementById('testDesc').value.trim();
  const questions = [...document.querySelectorAll('.question-card')].map(card => ({
    text: card.querySelector('.question-text').value.trim(),
    answers: [...card.querySelectorAll('.answer-option')].map(i => i.value.trim()),
    correct: card.querySelector('.correct-answer').value,
  }));

  if (!title) {
    showToast('Введите название теста', 'error');
    return;
  }

  if (questions.length === 0) {
    showToast('Добавьте хотя бы один вопрос', 'error');
    return;
  }

  console.log({ title, desc, questions });
  showToast('Тест сохранён (данные в console)', 'success');
}

addQuestion();
