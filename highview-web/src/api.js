// API configuration - using the actual API Gateway URL
const API_BASE_URL = 'https://tkutpalvb5.execute-api.us-east-1.amazonaws.com/default';

/**
 * Fetch leaderboard data from backend
 * @returns {Promise<Array>} Array of student leaderboard data
 */
async function getLeaderboards() {
    try {
        console.log('Fetching leaderboard from:', `${API_BASE_URL}/leaderboard`);
        const response = await fetch(`${API_BASE_URL}/leaderboard`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Received leaderboard data:', data);
        
        // The API returns data wrapped in a body object, unwrap it
        if (data && typeof data === 'object' && 'body' in data) {
            const unwrapped = typeof data.body === 'string' ? JSON.parse(data.body) : data.body;
            return unwrapped;
        }
        
        return data;
    } catch (error) {
        console.error('Error fetching leaderboards:', error);
        throw error;
    }
}

/**
 * Search for students by name
 * @param {string} query - Search query
 * @returns {Promise<Array>} Array of matching students
 */
async function searchStudents(query) {
    try {
        console.log('Searching students with query:', query);
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Received search results:', data);
        
        // The API returns data wrapped in a body object, unwrap it
        if (data && typeof data === 'object' && 'body' in data) {
            const unwrapped = typeof data.body === 'string' ? JSON.parse(data.body) : data.body;
            return unwrapped;
        }
        
        return data;
    } catch (error) {
        console.error('Error searching students:', error);
        throw error;
    }
}

/**
 * Create a new event/session
 * @param {Object} eventData - Event data object
 * @returns {Promise<Object>} Created event data
 */
async function createEvent(eventData) {
    try {
        console.log('Creating event with data:', eventData);
        const response = await fetch(`${API_BASE_URL}/sessions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(eventData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Event created successfully:', data);
        
        // The API returns data wrapped in a body object, unwrap it
        if (data && typeof data === 'object' && 'body' in data) {
            const unwrapped = typeof data.body === 'string' ? JSON.parse(data.body) : data.body;
            return unwrapped;
        }
        
        return data;
    } catch (error) {
        console.error('Error creating event:', error);
        throw error;
    }
}

/**
 * Get all events/sessions from backend
 * @returns {Promise<Array>} Array of event/session data
 */
async function getEvents() {
    try {
        console.log('Fetching events from:', `${API_BASE_URL}/events`);
        const response = await fetch(`${API_BASE_URL}/events`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Received events data:', data);
        
        // The API returns data wrapped in a body object, unwrap it
        if (data && typeof data === 'object' && 'body' in data) {
            const unwrapped = typeof data.body === 'string' ? JSON.parse(data.body) : data.body;
            return unwrapped.sessions || [];
        }
        
        return data.sessions || [];
    } catch (error) {
        console.error('Error fetching events:', error);
        throw error;
    }
}

export { getLeaderboards, searchStudents, createEvent, getEvents };
