import { getLeaderboards } from '../api.js';

// Store all students data for searching
let allStudents = [];
let dropdownVisible = false;

/**
 * Populate the top 3 leaderboard cards with data
 * @param {Array} students - Sorted array of students (highest points first)
 */
function populateLeaderboard(students) {
    if (!students || students.length === 0) {
        console.log('No students found');
        document.querySelector('.top1-name').textContent = 'No Data';
        document.querySelector('.top2 .top23-name').textContent = 'No Data';
        document.querySelector('.top3 .top23-name').textContent = 'No Data';
        return;
    }

    // Get top 3 students
    const top1 = students[0];
    const top2 = students[1];
    const top3 = students[2];

    // Update 1st place
    if (top1) {
        const name1 = document.querySelector('.top1-name');
        const points1 = document.querySelector('.top1 .points');
        if (name1) name1.textContent = `${top1.first} ${top1.last}`;
        if (points1) points1.textContent = `${top1.total_points} pts`;
        console.log('Updated 1st place:', top1.first, top1.last, top1.total_points);
    }

    // Update 2nd place
    if (top2) {
        const name2 = document.querySelector('.top2 .top23-name');
        const points2 = document.querySelector('.top2 .points');
        if (name2) name2.textContent = `${top2.first} ${top2.last}`;
        if (points2) points2.textContent = `${top2.total_points} pts`;
        console.log('Updated 2nd place:', top2.first, top2.last, top2.total_points);
    }

    // Update 3rd place
    if (top3) {
        const name3 = document.querySelector('.top3 .top23-name');
        const points3 = document.querySelector('.top3 .points');
        if (name3) name3.textContent = `${top3.first} ${top3.last}`;
        if (points3) points3.textContent = `${top3.total_points} pts`;
        console.log('Updated 3rd place:', top3.first, top3.last, top3.total_points);
    }
}

/**
 * Search students by name (client-side)
 * @param {string} query - Search query
 * @returns {Array} Filtered students
 */
function searchStudentsByName(query) {
    if (!query || query.trim() === '') {
        return allStudents;
    }
    
    const searchTerm = query.toLowerCase().trim();
    const segments = searchTerm.split(' ');
    
    return allStudents.filter(student => {
        const first = student.first.toLowerCase();
        const last = student.last.toLowerCase();
        const fullName = `${first} ${last}`;
        
        // Check if any segment matches first or last name
        return segments.some(segment => 
            first.includes(segment) || 
            last.includes(segment) || 
            fullName.includes(segment)
        );
    });
}

/**
 * Initialize leaderboard page - fetch and display data
 */
async function initLeaderboard() {
    try {
        console.log('Initializing leaderboard...');
        
        // Fetch leaderboard data from backend
        const students = await getLeaderboards();
        
        // Store all students for searching
        allStudents = students;
        
        console.log('Successfully loaded leaderboard data:', students);
        
        // Populate the UI
        populateLeaderboard(students);
        
    } catch (error) {
        console.error('Failed to load leaderboard:', error);
        // Show error to user
        const errorMsg = `Failed to load leaderboard data: ${error.message}`;
        console.error(errorMsg);
        alert(errorMsg);
    }
}

/**
 * Setup search functionality
 */
function setupSearch() {
    const searchForm = document.querySelector('.searchblock form');
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
    
    // Show dropdown on input
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
    
    // Handle form submission
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = searchInput.value.trim();
        
        console.log('Searching for:', query);
        
        // Search through all students
        const results = searchStudentsByName(query);
        
        console.log('Search results:', results);
        
        // Populate with search results (top 3)
        populateLeaderboard(results);
        
        // Hide dropdown
        dropdownContainer.style.display = 'none';
        dropdownVisible = false;
    });
    
    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchForm.contains(e.target)) {
            dropdownContainer.style.display = 'none';
            dropdownVisible = false;
        }
    });
    
    // Handle dropdown item clicks
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

/**
 * Display search dropdown with filtered results
 * @param {Array} results - Filtered student results
 * @param {HTMLElement} container - Dropdown container element
 * @param {HTMLElement} searchInput - Search input element
 */
function displaySearchDropdown(results, container, searchInput) {
    // Clear previous results
    container.innerHTML = '';
    
    if (results.length === 0) {
        container.innerHTML = '<div class="dropdown-item dropdown-no-results">No results found</div>';
        container.style.display = 'block';
        dropdownVisible = true;
        positionDropdown(container, searchInput);
        return;
    }
    
    // Limit to first 10 results for better UX
    const displayResults = results.slice(0, 10);
    
    displayResults.forEach(student => {
        const item = document.createElement('div');
        item.className = 'dropdown-item';
        item.textContent = `${student.first} ${student.last}`;
        container.appendChild(item);
    });
    
    container.style.display = 'block';
    dropdownVisible = true;
    positionDropdown(container, searchInput);
}

/**
 * Position the dropdown below the search input
 * @param {HTMLElement} dropdown - Dropdown element
 * @param {HTMLElement} input - Search input element
 */
function positionDropdown(dropdown, input) {
    const rect = input.getBoundingClientRect();
    dropdown.style.width = `${rect.width}px`;
    dropdown.style.top = `${rect.bottom + 4}px`;
    dropdown.style.left = `${rect.left}px`;
}

// Wait for DOM to be ready, then initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initLeaderboard();
        setupSearch();
    });
} else {
    initLeaderboard();
    setupSearch();
}