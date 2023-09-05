// Initialize map
var map = L.map('map').setView([43.65, -79.38], 12); // Coordinates: 43.65, -79.38 (Toronto); zoom: 12

// Add OpenStreetMap tile layer
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);