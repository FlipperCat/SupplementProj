// Supplement Personalization Quiz

// Cookie utility functions
function setCookie(name, value, days = 365) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = "expires=" + date.toUTCString();
  document.cookie = name + "=" + encodeURIComponent(value) + ";" + expires + ";path=/";
}

function getCookie(name) {
  const nameEQ = name + "=";
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.indexOf(nameEQ) === 0) {
      return decodeURIComponent(cookie.substring(nameEQ.length));
    }
  }
  return null;
}

function deleteCookie(name) {
  setCookie(name, "", -1);
}

class SupplementQuiz {
  constructor() {
    this.currentStep = 0;
    this.responses = {};
    this.recommendations = [];
    this.initializeQuiz();
  }

  // Quiz questions structure
  questions = [
    {
      id: 'goal',
      title: 'What\'s your primary health goal?',
      type: 'single',
      options: [
        { value: 'sleep', label: 'Better Sleep', icon: '😴' },
        { value: 'energy', label: 'More Energy', icon: '⚡' },
        { value: 'focus', label: 'Mental Focus', icon: '🧠' },
        { value: 'muscle', label: 'Muscle & Strength', icon: '💪' },
        { value: 'longevity', label: 'Longevity & Anti-Aging', icon: '⏳' },
        { value: 'stress', label: 'Stress Relief', icon: '🧘' },
        { value: 'immune', label: 'Immune Support', icon: '🛡️' },
        { value: 'recovery', label: 'Athletic Recovery', icon: '🏃' }
      ]
    },
    {
      id: 'age',
      title: 'What\'s your age range?',
      type: 'single',
      options: [
        { value: '18-25', label: '18-25' },
        { value: '26-35', label: '26-35' },
        { value: '36-50', label: '36-50' },
        { value: '51-65', label: '51-65' },
        { value: '65+', label: '65+' }
      ]
    },
    {
      id: 'gender',
      title: 'How do you identify?',
      type: 'single',
      options: [
        { value: 'male', label: 'Male' },
        { value: 'female', label: 'Female' },
        { value: 'other', label: 'Other / Prefer not to say' }
      ]
    },
    {
      id: 'health_conditions',
      title: 'Any existing health conditions or concerns? (Select all that apply)',
      type: 'multi',
      options: [
        { value: 'none', label: 'None' },
        { value: 'hypertension', label: 'High Blood Pressure' },
        { value: 'diabetes', label: 'Diabetes or Blood Sugar Issues' },
        { value: 'thyroid', label: 'Thyroid Issues' },
        { value: 'arthritis', label: 'Joint/Arthritis Issues' },
        { value: 'gut', label: 'Digestive Issues' },
        { value: 'depression', label: 'Depression/Mental Health' },
        { value: 'anxiety', label: 'Anxiety' }
      ]
    },
    {
      id: 'budget',
      title: 'What\'s your supplement budget per month?',
      type: 'single',
      options: [
        { value: 'budget', label: 'Under $50' },
        { value: 'moderate', label: '$50-$150' },
        { value: 'premium', label: '$150+' }
      ]
    },
    {
      id: 'experience',
      title: 'How experienced are you with supplements?',
      type: 'single',
      options: [
        { value: 'beginner', label: 'Beginner - Just Starting' },
        { value: 'intermediate', label: 'Intermediate - Taking Some' },
        { value: 'advanced', label: 'Advanced - Optimized Regimen' }
      ]
    }
  ];

  initializeQuiz() {
    const quizModal = document.getElementById('quiz-modal');
    if (quizModal) {
      quizModal.addEventListener('click', (e) => {
        if (e.target === quizModal) this.closeQuiz();
      });
    }
  }

  showStep(stepNum) {
    const modal = document.getElementById('quiz-modal');
    const container = document.getElementById('quiz-container');

    if (!container) return;

    this.currentStep = stepNum;
    const question = this.questions[stepNum];

    // Build question HTML
    let optionsHTML = '';
    if (question.type === 'single') {
      optionsHTML = question.options.map(opt => `
        <button class="quiz-option ${this.responses[question.id] === opt.value ? 'selected' : ''}"
                data-question="${question.id}"
                data-value="${opt.value}">
          ${opt.icon ? `<span class="option-icon">${opt.icon}</span>` : ''}
          <span>${opt.label}</span>
        </button>
      `).join('');
    } else if (question.type === 'multi') {
      optionsHTML = question.options.map(opt => `
        <label class="quiz-checkbox">
          <input type="checkbox"
                 data-question="${question.id}"
                 value="${opt.value}"
                 ${this.responses[question.id]?.includes(opt.value) ? 'checked' : ''}>
          <span>${opt.label}</span>
        </label>
      `).join('');
    }

    const progressPercent = ((stepNum + 1) / this.questions.length) * 100;

    container.innerHTML = `
      <div class="quiz-header">
        <button class="quiz-close" id="quiz-close-btn">&times;</button>
        <div class="quiz-progress">
          <div class="progress-bar" style="width: ${progressPercent}%"></div>
        </div>
        <p class="progress-text">Question ${stepNum + 1} of ${this.questions.length}</p>
      </div>

      <div class="quiz-content">
        <h2>${question.title}</h2>
        <div class="quiz-options ${question.type}">
          ${optionsHTML}
        </div>
      </div>

      <div class="quiz-footer">
        <button class="btn btn-secondary" id="quiz-prev" ${stepNum === 0 ? 'disabled' : ''}>Previous</button>
        <button class="btn btn-primary" id="quiz-next" ${stepNum === this.questions.length - 1 ? 'style=display:none' : ''}>Next</button>
        <button class="btn btn-success" id="quiz-submit" ${stepNum === this.questions.length - 1 ? '' : 'style=display:none'}>Get My Stack</button>
      </div>
    `;

    // Attach event listeners
    document.querySelectorAll('.quiz-option').forEach(btn => {
      btn.addEventListener('click', (e) => this.selectOption(e, question.type));
    });

    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
      cb.addEventListener('change', (e) => this.selectOption(e, 'multi'));
    });

    document.getElementById('quiz-close-btn')?.addEventListener('click', () => this.closeQuiz());
    document.getElementById('quiz-prev')?.addEventListener('click', () => this.showStep(stepNum - 1));
    document.getElementById('quiz-next')?.addEventListener('click', () => this.showStep(stepNum + 1));
    document.getElementById('quiz-submit')?.addEventListener('click', () => this.generateRecommendations());

    modal.style.display = 'flex';
  }

  selectOption(e, type) {
    const question = e.target.closest('[data-question]')?.dataset.question;
    if (!question) return;

    if (type === 'single') {
      this.responses[question] = e.target.dataset.value || e.target.closest('button').dataset.value;
      document.querySelectorAll(`[data-question="${question}"]`).forEach(opt => {
        opt.classList.remove('selected');
      });
      e.target.closest('button')?.classList.add('selected');
    } else if (type === 'multi') {
      if (!this.responses[question]) {
        this.responses[question] = [];
      }
      const value = e.target.value;
      if (e.target.checked) {
        this.responses[question].push(value);
      } else {
        this.responses[question] = this.responses[question].filter(v => v !== value);
      }
    }
  }

  generateRecommendations() {
    // Logic to map responses to supplement recommendations
    const recommendations = this.buildSupplementStack();
    this.showResults(recommendations);
  }

  buildSupplementStack() {
    const goal = this.responses.goal;
    const gender = this.responses.gender;
    const experience = this.responses.experience;
    const budget = this.responses.budget;
    const conditions = this.responses.health_conditions || [];

    // Base stacks by goal (can expand with more sophisticated logic)
    const baseStacks = {
      sleep: {
        essential: ['magnesium', 'l-theanine', 'melatonin'],
        recommended: ['glycine', 'apigenin', 'reishi-mushroom'],
        advanced: ['5-htp', 'gaba', 'dsip']
      },
      energy: {
        essential: ['b-complex', 'iron', 'coq10'],
        recommended: ['cordyceps-mushroom', 'rhodiola', 'vitamin-d3'],
        advanced: ['nmn', 'creatine', 'pqq', 'mots-c']
      },
      focus: {
        essential: ['omega-3', 'lions-mane', 'l-theanine'],
        recommended: ['bacopa-monnieri', 'alpha-gpc', 'caffeine'],
        advanced: ['cdp-choline', 'phosphatidylserine', 'semax']
      },
      muscle: {
        essential: ['creatine', 'protein', 'vitamin-d3'],
        recommended: ['magnesium', 'zinc', 'beta-alanine'],
        advanced: ['hmb', 'citrulline', 'cjc-1295', 'ipamorelin']
      },
      longevity: {
        essential: ['vitamin-d3', 'omega-3'],
        recommended: ['coq10', 'nac', 'curcumin'],
        advanced: ['nmn', 'resveratrol', 'urolithin-a', 'epithalon', 'ghk-cu']
      },
      stress: {
        essential: ['magnesium'],
        recommended: ['ashwagandha', 'l-theanine', 'vitamin-b-complex'],
        advanced: ['rhodiola', 'holy-basil', 'selank']
      },
      immune: {
        essential: ['vitamin-d3', 'zinc', 'vitamin-c'],
        recommended: ['selenium', 'probiotics', 'reishi-mushroom'],
        advanced: ['nac', 'elderberry']
      },
      recovery: {
        essential: ['magnesium', 'omega-3', 'creatine'],
        recommended: ['cordyceps-mushroom', 'collagen', 'glutamine'],
        advanced: ['hmb', 'citrulline', 'bpc-157', 'tb-500']
      }
    };

    let stack = baseStacks[goal] || baseStacks.longevity;

    // Filter by experience level
    let supplements = [];
    if (experience === 'beginner') {
      supplements = stack.essential;
    } else if (experience === 'intermediate') {
      supplements = [...stack.essential, ...stack.recommended];
    } else {
      supplements = [...stack.essential, ...stack.recommended, ...stack.advanced];
    }

    // Filter by budget
    if (budget === 'budget') {
      supplements = supplements.slice(0, 3);
    } else if (budget === 'moderate') {
      supplements = supplements.slice(0, 6);
    }

    // Gender-specific additions
    if (gender === 'male') {
      if (!supplements.includes('zinc') && (goal === 'longevity' || goal === 'muscle')) {
        supplements.push('zinc');
      }
      if (!supplements.includes('tongkat-ali') && goal === 'energy') {
        supplements.push('tongkat-ali');
      }
    } else if (gender === 'female') {
      if (!supplements.includes('iron') && goal === 'energy') {
        supplements.push('iron');
      }
      if (!supplements.includes('vitamin-b9-folate') && goal === 'longevity') {
        supplements.push('vitamin-b9-folate');
      }
    }

    // Health condition adjustments
    if (conditions.includes('gut')) {
      if (!supplements.includes('probiotics')) supplements.push('probiotics');
      if (!supplements.includes('turkey-tail-mushroom')) supplements.push('turkey-tail-mushroom');
    }
    if (conditions.includes('anxiety')) {
      if (!supplements.includes('ashwagandha')) supplements.push('ashwagandha');
      if (!supplements.includes('l-theanine')) supplements.push('l-theanine');
    }

    return {
      goal,
      supplements: [...new Set(supplements)], // Remove duplicates
      gender,
      experience,
      budget
    };
  }

  showResults(recommendations) {
    const modal = document.getElementById('quiz-modal');
    const container = document.getElementById('quiz-container');

    // Mark quiz as completed so it doesn't show again
    setCookie('quiz-completed', 'true', 365);

    // Build supplement cards
    const peptideSlugs = ['bpc-157','tb-500','cjc-1295','ipamorelin','semax','selank',
                          'ghk-cu','epithalon','dsip','mots-c','aod-9604','pt-141'];
    const supplementCards = recommendations.supplements.map(id => {
      const section = peptideSlugs.includes(id) ? 'peptides' : 'supplements';
      return `<div class="result-supplement-card">
        <h4>${id}</h4>
        <a href="/${section}/${id}/" class="btn btn-small">Learn More</a>
      </div>`;
    }).join('');

    container.innerHTML = `
      <div class="quiz-header">
        <button class="quiz-close" id="quiz-close-btn">&times;</button>
      </div>

      <div class="quiz-results">
        <h2>Your Personalized Supplement Stack</h2>
        <p class="results-intro">Based on your goal: <strong>${recommendations.goal.toUpperCase()}</strong></p>

        <div class="supplements-grid">
          ${supplementCards}
        </div>

        <div class="results-actions">
          <button class="btn btn-primary" id="view-full-stack">View Full Stack Details</button>
          <button class="btn btn-secondary" id="restart-quiz">Take Quiz Again</button>
        </div>
      </div>
    `;

    document.getElementById('quiz-close-btn')?.addEventListener('click', () => this.closeQuiz());
    document.getElementById('view-full-stack')?.addEventListener('click', () => {
      window.location.href = `/analyzer/?goal=${recommendations.goal}&supplements=${recommendations.supplements.join(',')}`;
    });
    document.getElementById('restart-quiz')?.addEventListener('click', () => {
      this.responses = {};
      this.showStep(0);
    });
  }

  closeQuiz() {
    const modal = document.getElementById('quiz-modal');
    if (modal) {
      modal.style.display = 'none';
      setCookie('quiz-dismissed', 'true', 365);
    }
  }

  openQuiz() {
    const modal = document.getElementById('quiz-modal');
    if (modal) {
      modal.style.display = 'flex';
      deleteCookie('quiz-dismissed');
      this.showStep(0);
    }
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  const dismissed = getCookie('quiz-dismissed');
  const completed = getCookie('quiz-completed');
  const quizBtn = document.getElementById('quiz-trigger-btn');
  const quizModal = document.getElementById('quiz-modal');

  // "Find Your Stack" button always works (manual trigger)
  if (quizBtn) {
    quizBtn.addEventListener('click', () => {
      const quiz = new SupplementQuiz();
      quiz.openQuiz();
    });
  }

  // Auto-show quiz ONLY on homepage, ONLY if never completed or dismissed
  if (quizModal && !dismissed && !completed && window.location.pathname === '/') {
    const quiz = new SupplementQuiz();
    quiz.openQuiz();
  }
});
