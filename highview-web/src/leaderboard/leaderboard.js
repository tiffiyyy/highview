// src/leaderboard.js
import { getLeaderboards } from '/src/api.js';

// ===== State (keep EVERYTHING here) =====
let ALL = [];               // full normalized array from API
let dropdownVisible = false;

// Expose for quick debugging (optional)
window.ALL_STUDENTS = () => ALL;

// -------- Helpers --------
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const norm = (s) => (s || '').toString().trim().toLowerCase();

// -------- Populate top 3 cards --------
function populateLeaderboard(students) {
  const setCard = (rootSel, student) => {
    const root  = document.querySelector(rootSel);
    if (!root) return;
    const nameEl   = root.querySelector(rootSel === '.top1' ? '.top1-name' : '.top23-name');
    const pointsEl = root.querySelector('.points');

    if (!student) {
      if (nameEl) nameEl.textContent = 'No Data';
      if (pointsEl) pointsEl.textContent = '—';
      return;
    }

    if (nameEl)   nameEl.textContent   = `${student.first ?? ''} ${student.last ?? ''}`.trim() || '—';
    if (pointsEl) pointsEl.textContent = `${student.total_points ?? 0} pts`;

    // If you want to show attendance/bonus on cards (optional):
    // const badge = root.querySelector('.badge');
    // if (badge) badge.textContent = `${student.attendance_points ?? 0}A / ${student.bonus_points ?? 0}B`;
  };

  if (!Array.isArray(students) || students.length === 0) {
    setCard('.top1', null);
    setCard('.top2', null);
    setCard('.top3', null);
    return;
  }

  setCard('.top1', students[0] || null);
  setCard('.top2', students[1] || null);
  setCard('.top3', students[2] || null);
}

// -------- Client-side search over ALL --------
function searchStudentsByName(query) {
  const q = norm(query);
  if (!q) return [...ALL];
  const parts = q.split(/\s+/).filter(Boolean);
  return ALL.filter(st => {
    const first = norm(st.first);
    const last  = norm(st.last);
    const full  = `${first} ${last}`.trim();
    const email = norm(st.email);
    const comp  = norm(st.company);
    return parts.every(p =>
      first.includes(p) || last.includes(p) || full.includes(p) ||
      email.includes(p) || comp.includes(p)
    );
  });
}

// -------- Dropdown rendering --------
function displaySearchDropdown(results, container, searchInput) {
  container.innerHTML = '';

  if (!results.length) {
    container.innerHTML = '<div class="dropdown-item dropdown-no-results">No results found</div>';
    container.style.display = 'block';
    dropdownVisible = true;
    positionDropdown(container, searchInput);
    return;
  }

  // Show only first 10 in the dropdown for UX, but ALL remains intact in memory.
  results.slice(0, 10).forEach(student => {
    const item = document.createElement('div');
    item.className = 'dropdown-item';
    item.textContent = `${student.first} ${student.last}`;
    container.appendChild(item);
  });

  container.style.display = 'block';
  dropdownVisible = true;
  positionDropdown(container, searchInput);
}

function positionDropdown(dropdown, input) {
  const rect = input.getBoundingClientRect();
  dropdown.style.width = `${rect.width}px`;
  dropdown.style.top = `${rect.bottom + 4}px`;
  dropdown.style.left = `${rect.left}px`;
}

// -------- Setup search UI --------
function setupSearch() {
  const searchForm  = document.querySelector('.searchblock form');
  const searchInput = document.querySelector('.searchblock input[type="search"]');
  if (!searchForm || !searchInput) {
    console.error('Search elements not found');
    return;
  }

  // Create dropdown container
  const dropdownContainer = document.createElement('div');
  dropdownContainer.className = 'search-dropdown';
  dropdownContainer.style.display = 'none';
  searchForm.appendChild(dropdownContainer);

  // Input → filter & show dropdown
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    if (query.length > 0) {
      const results = searchStudentsByName(query);
      displaySearchDropdown(results, dropdownContainer, searchInput);
    } else {
      dropdownContainer.style.display = 'none';
      dropdownVisible = false;
    }
  });

  // Submit → use results to repopulate top 3 section
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    const results = searchStudentsByName(query);
    populateLeaderboard(results);
    dropdownContainer.style.display = 'none';
    dropdownVisible = false;
  });

  // Click outside → hide dropdown
  document.addEventListener('click', (e) => {
    if (!searchForm.contains(e.target)) {
      dropdownContainer.style.display = 'none';
      dropdownVisible = false;
    }
  });

  // Click on an item → populate top 3 with filtered list
  dropdownContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('dropdown-item')) {
      searchInput.value = e.target.textContent;
      const results = searchStudentsByName(searchInput.value);
      populateLeaderboard(results);
      dropdownContainer.style.display = 'none';
      dropdownVisible = false;
    }
  });
}

// -------- Initial load --------
export async function initLeaderboard() {
  try {
    console.log('Initializing leaderboard…');

    // Use API helper so fields are normalized & preserved (attendance/bonus/missed)
    const students = await getLeaderboards();

    // Keep the ENTIRE array in memory (ALL)
    ALL = Array.isArray(students) ? students : (students?.students || []);
    console.log('Loaded students (count):', ALL.length);

    // Populate the UI (top 3)
    populateLeaderboard(ALL);

    // Prepare search
    setupSearch();
  } catch (err) {
    console.error('Failed to load leaderboard:', err);
    alert(`Failed to load leaderboard data: ${err.message || err}`);
  }
}

// Auto-run if this script is loaded directly on the leaderboard page
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initLeaderboard);
} else {
  initLeaderboard();
}
