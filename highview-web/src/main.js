import './style.css'
import javascriptLogo from './javascript.svg'
import viteLogo from '/vite.svg'
import { setupCounter } from './counter.js'

document.querySelector('#app').innerHTML = `
  <div>
  <div class="sidebar">
    <h2>General</h2>
    <ul>
      <li><a href="src/home/home.html">Home</a></li>
      <li><a href="src/leaderboard/leaderboard.html">Leaderboard</a></li>
      <li><a href="src/messages/messages.html">Messages</a></li>
      <li><a href="src/settings/settings.html">Settings</a></li>
    </ul>
    <h2>Academics</h2> 
    <ul>
      <li><a href="src/courses/courses.html">My Courses</a></li>
      <li><a href="src/calendar/calendar.html">My Calendar</a></li>
    </ul> 
  </div>
`

setupCounter(document.querySelector('#counter'))
