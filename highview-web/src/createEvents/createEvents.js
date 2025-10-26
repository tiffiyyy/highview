import { createEvent } from '../api.js';

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('submitBtn');
    
    // Add event listener for form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault(); // Prevent default form submission
        
        try {
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creating Event...';
            
            // Get form data
            const formData = getFormData();
            
            // Validate form data
            const validation = validateFormData(formData);
            if (!validation.isValid) {
                alert(validation.message);
                return;
            }
            
            // Create the event
            const result = await createEvent(formData);
            
            // Show success message
            alert('Event created successfully!');
            
            // Reset form
            form.reset();
            
        } catch (error) {
            console.error('Error creating event:', error);
            alert('Failed to create event. Please try again.');
        } finally {
            // Reset button state
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Event';
        }
    });
});

/**
 * Extract and format form data to match lambda function expectations
 */
function getFormData() {
    const eventName = document.getElementById('eventName').value;
    const sessionType = document.getElementById('Tags').value;
    const description = document.getElementById('description').value;
    const startDateTime = document.getElementById('startDateTime').value;
    const endDateTime = document.getElementById('endDateTime').value;
    const location = document.getElementById('location').value;
    const email = document.getElementById('email').value;
    
    // Format date and time for the lambda function
    const sessionDate = startDateTime ? new Date(startDateTime).toISOString().split('T')[0] : '';
    const sessionTime = startDateTime ? new Date(startDateTime).toTimeString().split(' ')[0].substring(0, 5) : '';
    
    return {
        session_name: eventName,
        session_type: sessionType,
        session_date: sessionDate,
        session_description: description,
        session_location: location,
        session_time: sessionTime,
        email: email
    };
}

/**
 * Validate form data before submission
 */
function validateFormData(data) {
    if (!data.session_name || data.session_name.trim() === '') {
        return { isValid: false, message: 'Event name is required' };
    }
    
    if (!data.session_type || data.session_type === '----') {
        return { isValid: false, message: 'Please select an event tag' };
    }
    
    if (!data.session_date || data.session_date === '') {
        return { isValid: false, message: 'Start date and time is required' };
    }
    
    if (!data.session_location || data.session_location.trim() === '') {
        return { isValid: false, message: 'Location is required' };
    }
    
    if (!data.email || data.email.trim() === '') {
        return { isValid: false, message: 'Mentor email is required' };
    }
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        return { isValid: false, message: 'Please enter a valid email address' };
    }
    
    return { isValid: true };
}
