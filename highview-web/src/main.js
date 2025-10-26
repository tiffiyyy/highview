import './sidebar.css'

document.querySelector('#app').innerHTML = `
  <div id="sidebar-container"></div>
`
fetch('/src/sidebar.html')
  .then(response => response.text())
  .then(html => {
    document.getElementById('sidebar-container').innerHTML = html;
  });
