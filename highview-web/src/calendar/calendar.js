const currentDate = document.querySelector(".current-date")

let date = new Date(), 
currMonth = date.getMonth(), 
currYear = date.getFullYear(), 
currDay = date.getDate(); 

const months = ["January", "February", "March", "April", "May", "June", "July", "August", 
                "September", "October", "November", "December"];

const renderCalendar = () => {
    let firstDayOfMonth = new Date(currYear, currMonth, 1).getDay(), 
    lastDateOfMonth = new Date(currYear, currMonth + 1, 0).getDate(), 
    lastDateOfLastMonth = new Date(currYear, currMonth, 0).getDate(); 

    const startOfWeek = new Date(date); 
    startOfWeek.setDate(date.getDate() - currDay);
    const endOfWeek = startOfWeek + 14; 
    currentDate.innerText = `${months[currMonth]} ${currYear}`
}
renderCalendar(); 