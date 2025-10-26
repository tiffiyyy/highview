// Get references to elements
const currentDateElem = document.querySelector('.current-date');
const calendarDaysContainer = document.getElementById('calendar-days');

function generateFourWeekCalendar() {
    const today = new Date();

    // Display current month and year
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    currentDateElem.textContent = `${monthNames[today.getMonth()]} ${today.getFullYear()}`;

    // Calculate Monday of the current week
    const dayOfWeek = today.getDay(); // Sunday=0, Monday=1 ...
    const diffToMonday = (dayOfWeek + 6) % 7; // Monday=0
    const startOfWeek1 = new Date(today);
    startOfWeek1.setDate(today.getDate() - diffToMonday);

    // Calculate the start dates for 4 weeks
    const weeks = [];
    for (let i = 0; i < 4; i++) {
        const startOfWeek = new Date(startOfWeek1);
        startOfWeek.setDate(startOfWeek1.getDate() + (i * 7));
        weeks.push({ name: `Week ${i + 1}`, start: startOfWeek });
    }

    // Clear previous calendar
    calendarDaysContainer.innerHTML = '';

    weeks.forEach(week => {
        // Create a container for the week
        const weekRow = document.createElement('div');
        weekRow.className = 'week-row'; // Use flex to align days in a row

        // Optional: Week label
        const weekLabel = document.createElement('div');
        weekLabel.className = 'week-label';
        calendarDaysContainer.appendChild(weekLabel);

        for (let i = 0; i < 7; i++) {
            const date = new Date(week.start);
            date.setDate(week.start.getDate() + i);

            // Create day box
            const dayBox = document.createElement('div');
            dayBox.className = 'calendar-box';

            // Highlight today
            if (date.toDateString() === today.toDateString()) {
                dayBox.classList.add('today');
            }

            // Add day number
            const dateNum = document.createElement('div');
            dateNum.className = 'date-num';
            dateNum.textContent = date.getDate();

            dayBox.appendChild(dateNum);
            weekRow.appendChild(dayBox);
        }

        // Append the week row to the calendar container
        calendarDaysContainer.appendChild(weekRow);
    });
}

// Generate calendar on page load
generateFourWeekCalendar();
