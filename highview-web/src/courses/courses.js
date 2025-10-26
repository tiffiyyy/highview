import { getEvents } from '../api.js';

const currentDate = document.querySelector(".current-date")

let date = new Date(), 
currMonth = date.getMonth(), 
currYear = date.getFullYear(), 
currDay = date.getDate(); 

const months = ["January", "February", "March", "April", "May", "June", "July", "August", 
                "September", "October", "November", "December"];

// Store events globally
let events = [];

const renderCalendar = () => {
    let firstDayOfMonth = new Date(currYear, currMonth, 1).getDay(), 
    lastDateOfMonth = new Date(currYear, currMonth + 1, 0).getDate(), 
    lastDateOfLastMonth = new Date(currYear, currMonth, 0).getDate(); 

    const startOfWeek = new Date(date); 
    startOfWeek.setDate(date.getDate() - currDay);
    const endOfWeek = startOfWeek + 14; 
    currentDate.innerText = `${months[currMonth]} ${currYear}`
}

/**
 * Parse date for sorting purposes
 * @param {string} dateString - Date string (could be ISO or simple format like "9/3")
 * @returns {Date} Date object for sorting
 */
const parseDateForSorting = (dateString) => {
    // Handle simple date format like "9/3", "10/22"
    if (dateString && dateString.includes('/') && !dateString.includes('-')) {
        const [month, day] = dateString.split('/');
        const currentYear = new Date().getFullYear();
        return new Date(currentYear, parseInt(month) - 1, parseInt(day));
    } else {
        // Handle ISO date format
        return new Date(dateString);
    }
}

/**
 * Format date for display
 * @param {string} dateString - Date string (could be ISO or simple format like "9/3")
 * @returns {Object} Formatted date object
 */
const formatDate = (dateString) => {
    let date;
    
    // Handle simple date format like "9/3", "10/22"
    if (dateString && dateString.includes('/') && !dateString.includes('-')) {
        const [month, day] = dateString.split('/');
        const currentYear = new Date().getFullYear();
        date = new Date(currentYear, parseInt(month) - 1, parseInt(day));
    } else {
        // Handle ISO date format
        date = new Date(dateString);
    }
    
    const month = months[date.getMonth()].substring(0, 3).toUpperCase();
    const day = date.getDate();
    
    // For simple dates, use a default time
    const time = dateString && dateString.includes('/') && !dateString.includes('-') 
        ? '12:00 PM' 
        : date.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    
    return { month, day, time };
}

/**
 * Get label class based on session type
 * @param {string} sessionType - Type of session
 * @returns {string} CSS class name
 */
const getLabelClass = (sessionType) => {
    switch (sessionType.toLowerCase()) {
        case 'event':
        case 'field day':
        case 'orientation':
        case 'career summit':
        case 'pd':
            return 'eventslabel';
        case 'meeting':
        case 'mentor session':
            return 'meetinglabel';
        case 'homework':
            return 'homeworklabel';
        default:
            return 'eventslabel';
    }
}

/**
 * Render events in the upcoming tasks section
 */
const renderEvents = () => {
    const tasksBlock = document.querySelector('.tasksblock');
    if (!tasksBlock) return;

    // Create or find the tasks container
    let tasksContainer = tasksBlock.querySelector('.tasks-container');
    if (!tasksContainer) {
        tasksContainer = document.createElement('div');
        tasksContainer.className = 'tasks-container';
        tasksBlock.appendChild(tasksContainer);
    }

    // Clear existing tasks
    tasksContainer.innerHTML = '';

    // Sort events by date
    const sortedEvents = events.sort((a, b) => {
        const dateA = parseDateForSorting(a.session_date);
        const dateB = parseDateForSorting(b.session_date);
        return dateA - dateB;
    });

    console.log('Sorted events:', sortedEvents);
    console.log('Number of events to render:', sortedEvents.length);

    // Create task elements for each event
    sortedEvents.forEach((event, index) => {
        console.log(`Rendering event ${index + 1}:`, event.session_name, event.session_date);
        const { month, day, time } = formatDate(event.session_date);
        const labelClass = getLabelClass(event.session_type);
        
        // Make all event types clickable
        const isClickable = true;
        
        const taskElement = document.createElement('div');
        taskElement.className = 'tasks';
        
        if (isClickable) {
            const linkElement = document.createElement('a');
            linkElement.href = `/events.html?id=${event.session_id}`;
            linkElement.style.textDecoration = 'none';
            linkElement.style.color = 'inherit';
            linkElement.style.display = 'flex';
            linkElement.style.flexDirection = 'row';
            linkElement.style.alignItems = 'flex-start';
            linkElement.style.gap = '16px';
            linkElement.style.width = '100%';
            linkElement.style.height = '100%';
            
            linkElement.innerHTML = `
                <section class="calendaricon">
                    <section class="month">
                        <h6>${month}</h6>
                    </section>
                    <section class="date">
                        <h5>${day}</h5>
                    </section>
                </section>
                <div class="task1text">
                    <h3>${event.session_name}</h3>
                    <div class="taskinfo">
                        <div class="${labelClass}">${event.session_type}</div>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M9.66667 4.16667V9.66667L13.3333 11.5M18.8333 9.66667C18.8333 14.7293 14.7293 18.8333 9.66667 18.8333C4.60406 18.8333 0.5 14.7293 0.5 9.66667C0.5 4.60406 4.60406 0.5 9.66667 0.5C14.7293 0.5 18.8333 4.60406 18.8333 9.66667Z" stroke="#757575" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        ${time}
                    </div>
                </div>
            `;
            
            taskElement.appendChild(linkElement);
        } else {
            taskElement.innerHTML = `
                <section class="calendaricon">
                    <section class="month">
                        <h6>${month}</h6>
                    </section>
                    <section class="date">
                        <h5>${day}</h5>
                    </section>
                </section>
                <div class="task1text">
                    <h3>${event.session_name}</h3>
                    <div class="taskinfo">
                        <div class="${labelClass}">${event.session_type}</div>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M9.66667 4.16667V9.66667L13.3333 11.5M18.8333 9.66667C18.8333 14.7293 14.7293 18.8333 9.66667 18.8333C4.60406 18.8333 0.5 14.7293 0.5 9.66667C0.5 4.60406 4.60406 0.5 9.66667 0.5C14.7293 0.5 18.8333 4.60406 18.8333 9.66667Z" stroke="#757575" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        ${time}
                    </div>
                </div>
            `;
        }
        
        tasksContainer.appendChild(taskElement);
        console.log(`Added event ${index + 1} to DOM:`, event.session_name);
    });
    
    console.log('Total events added to DOM:', tasksContainer.children.length);
}

/**
 * Load events from the API
 */
const loadEvents = async () => {
    try {
        console.log('Loading events...');
        events = await getEvents();
        console.log('Events loaded from API:', events);
        console.log('Number of events from database:', events.length);
        if (events.length > 0) {
            console.log('First event:', events[0]);
        }
        if (events.length === 28) {
            console.log('✅ Successfully loaded all 28 events from database!');
        } else {
            console.log(`⚠️ Expected 28 events, but got ${events.length}`);
        }
        renderEvents();
    } catch (error) {
        console.error('Failed to load events from API:', error);
        console.error('Error details:', error.message);
        // Show error message to user
        const tasksBlock = document.querySelector('.tasksblock');
        if (tasksBlock) {
            let tasksContainer = tasksBlock.querySelector('.tasks-container');
            if (!tasksContainer) {
                tasksContainer = document.createElement('div');
                tasksContainer.className = 'tasks-container';
                tasksBlock.appendChild(tasksContainer);
            }
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'tasks';
            errorDiv.innerHTML = `
                <div class="task1text">
                    <h3>Unable to load events</h3>
                    <div class="taskinfo">
                        <div class="eventslabel">Error</div>
                        <span>Please check the console for details</span>
                    </div>
                </div>
            `;
            tasksContainer.appendChild(errorDiv);
        }
    }
}

// Initialize the page
const init = () => {
    renderCalendar();
    loadEvents();
}

// Start when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
} 