// Simple, direct approach to load and display event data
import QRCode from 'qrcode-svg';
/**
 * Get URL parameters
 */
function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return Object.fromEntries(params.entries());
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    let date;
    
    if (dateString && dateString.includes('/') && !dateString.includes('-')) {
        const [month, day] = dateString.split('/');
        const currentYear = new Date().getFullYear();
        date = new Date(currentYear, parseInt(month) - 1, parseInt(day));
    } else {
        date = new Date(dateString);
    }
    
    const months = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"];
    const month = months[date.getMonth()].substring(0, 3).toUpperCase();
    const day = date.getDate();
    
    const time = dateString && dateString.includes('/') && !dateString.includes('-') 
        ? '12:00 PM' 
        : date.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    
    return { month, day, time, fullDate: date };
}

/**
 * Get label class based on session type
 */
function getLabelClass(sessionType) {
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
 * Display QR code linking to HighView Exit Ticket form
 */
function displayQRCode(qrData, eventId) {
    const qrDisplay = document.getElementById('qr-code-display');
    if (!qrDisplay) {
        console.error('QR code display element not found');
        return;
    }
    
    try {
        // Generate QR code linking to the HighView Sessions Exit Ticket form
        const exitTicketUrl = 'https://docs.google.com/forms/d/1Lb_ojF1f2-ai_0r9DHPMtO_3zZ93__SuUA-jpZI8y9s/edit';
        const qrcode = new QRCode({
            content: exitTicketUrl,
            padding: 4,
            width: 160,
            height: 160,
            color: "#000000",
            background: "#ffffff",
            ecl: "M",
            join: true,
        });
        
        console.log('Generated QR code linking to exit ticket form for event:', eventId);
        qrDisplay.innerHTML = qrcode.svg();
        
    } catch (error) {
        console.error('Error generating QR code:', error);
        qrDisplay.innerHTML = `
            <div style="width: 160px; height: 160px; background: #f0f0f0; border: 2px dashed #ccc; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <div style="font-size: 48px; opacity: 0.5;">📱</div>
                <div style="color: #666; font-size: 12px; margin-top: 10px;">QR Code Error</div>
            </div>
        `;
    }
}

/**
 * Load and display event data
 */
async function loadEventData() {
    try {
        const params = getUrlParams();
        const eventId = params.id;
        
        console.log('Loading event with ID:', eventId);
        
        if (!eventId) {
            console.error('No event ID provided');
            return;
        }
        
        // Fetch all events and find the one with matching ID
        const response = await fetch('https://tkutpalvb5.execute-api.us-east-1.amazonaws.com/default/events');
        const data = await response.json();
        const events = data.sessions || [];
        
        const event = events.find(e => e.session_id === eventId);
        
        if (!event) {
            console.error('Event not found');
            return;
        }
        
        console.log('Found event:', event);
        
        // Update the page with event data
        const { month, day, time, fullDate } = formatDate(event.session_date);
        const labelClass = getLabelClass(event.session_type);
        
        // Update calendar icon
        const monthElement = document.querySelector('.month h6');
        const dateElement = document.querySelector('.date h5');
        if (monthElement) monthElement.textContent = month;
        if (dateElement) dateElement.textContent = day;
        
        // Update event title
        const titleElement = document.querySelector('.task1text h3');
        if (titleElement) titleElement.textContent = event.session_name;
        
        // Update event type label
        const labelElement = document.querySelector('.eventslabel');
        if (labelElement) {
            labelElement.textContent = event.session_type;
            labelElement.className = labelClass;
        }
        
        // Update time
        const timeElement = document.querySelector('.taskinfo');
        if (timeElement) {
            const timeText = timeElement.querySelector('svg').nextSibling;
            if (timeText) {
                timeText.textContent = ` ${time}`;
            }
        }
        
        // Update description
        const descriptionElement = document.querySelector('.descriptionblock');
        if (descriptionElement) {
            const description = event.session_description || 
                `This is a ${event.session_type.toLowerCase()} session scheduled for ${fullDate.toLocaleDateString()}. More details will be available closer to the event date.`;
            descriptionElement.textContent = description;
        }
        
        // Display QR code
        displayQRCode(event.qr_img, eventId);
        
    } catch (error) {
        console.error('Error loading event:', error);
    }
}

// Wait for DOM to be ready and then load event data
document.addEventListener('DOMContentLoaded', loadEventData);