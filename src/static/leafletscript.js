// Initialize map
var map = L.map('map')
    .setView([43.65, -79.38], 12); // Coordinates: 43.65, -79.38 (Toronto); zoom: 12


// Add OpenStreetMap tile layer
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


/**
 * Add a concert marker to the map.
 * When clicked, it will display details and the link to the setlist.
 * 
 * @param {*} lat latitude
 * @param {*} lng longitude
 * @param {*} artistName artist name
 * @param {*} date date of concert
 * @param {*} venue venue name
 * @param {*} url setlist url
 */
function addConcertMarker(lat, lng, artistName, date, venue, url) {

    // Create marker (pin)
    let marker = L.marker([lat, lng]).addTo(map);

    // Show details in tooltip on hover
    marker.bindTooltip(`${artistName}<br>${date}<br>${venue}`)

    // Open page on setlist.fm in new tab on click
    marker.on("click", () => window.open(url, "_blank"))
}


/**
 * Draw a line between the specified coordinates, in order.
 * 
 * @param {...any} coords all coordinates in format [lat, lng]
 */
function drawLineBetweenConcerts(...coords) {
    let line = L.polyline(coords)
        .addTo(map);

    // Zoom map to fit all concerts
    map.fitBounds(line.getBounds());
}


/**
 * Show user's current location, if available.
 */
function showCurrentLocation(event) {

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((pos) => {

            let currentPosition = [pos.coords.latitude, pos.coords.longitude];

            // Move map to current location
            map.setView(currentPosition, 12);

            // Add pin to current location
            let marker = L.marker(currentPosition).addTo(map);

            // Marker tooltip on hover
            marker.bindTooltip("Current location")
        })
    } else {
        window.alert("Not available");
    }
}
